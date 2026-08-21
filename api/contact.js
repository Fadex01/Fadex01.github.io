/** Secure contact endpoint. Required: RESEND_API_KEY. Optional: CONTACT_TO, CONTACT_FROM, CONTACT_ALLOWED_ORIGIN. */
const MAX_LENGTHS = Object.freeze({ name: 100, email: 254, subject: 160, message: 5_000 });
const REQUEST_TIMEOUT_MS = 10_000;
const escapeHtml = value => value.replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));

function normaliseField(value, maximum) {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  return trimmed && trimmed.length <= maximum ? trimmed : null;
}

function isAllowedOrigin(request) {
  const origin = request.headers.origin;
  if (!origin) return true;
  if (process.env.CONTACT_ALLOWED_ORIGIN) return origin === process.env.CONTACT_ALLOWED_ORIGIN;
  return Boolean(request.headers.host) && origin === `https://${request.headers.host}`;
}

module.exports = async function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store, max-age=0');
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return response.status(405).json({ error: 'Method not allowed' });
  }
  if (!isAllowedOrigin(request)) return response.status(403).json({ error: 'Invalid request origin' });
  if (!(request.headers['content-type'] || '').toLowerCase().startsWith('application/json')) return response.status(415).json({ error: 'Content-Type must be application/json' });

  const body = request.body;
  if (!body || typeof body !== 'object' || Array.isArray(body)) return response.status(400).json({ error: 'Invalid request body' });
  // Honeypot: bots commonly fill this invisible field; a real sender never sees it.
  if (body.website) return response.status(200).json({ success: true });

  const name = normaliseField(body.name, MAX_LENGTHS.name);
  const email = normaliseField(body.email, MAX_LENGTHS.email);
  const subject = normaliseField(body.subject, MAX_LENGTHS.subject);
  const message = normaliseField(body.message, MAX_LENGTHS.message);
  if (!name || !email || !subject || !message) return response.status(400).json({ error: 'All fields are required and must be within the allowed length' });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return response.status(400).json({ error: 'Please provide a valid email address' });
  if (!process.env.RESEND_API_KEY) {
    console.error('Contact form is not configured: RESEND_API_KEY is missing');
    return response.status(503).json({ error: 'Email service is temporarily unavailable' });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const emailResponse = await fetch('https://api.resend.com/emails', {
      method: 'POST', signal: controller.signal,
      headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.CONTACT_FROM || 'Portfolio Contact <onboarding@resend.dev>',
        to: [process.env.CONTACT_TO || 'okorofarid07@gmail.com'], reply_to: email,
        subject: `Portfolio contact: ${subject}`,
        html: `<h2>New portfolio contact message</h2><p><strong>Name:</strong> ${escapeHtml(name)}</p><p><strong>Email:</strong> ${escapeHtml(email)}</p><p><strong>Subject:</strong> ${escapeHtml(subject)}</p><p><strong>Message:</strong><br>${escapeHtml(message).replace(/\n/g, '<br>')}</p>`
      })
    });
    if (!emailResponse.ok) {
      console.error(`Resend email request failed with status ${emailResponse.status}`);
      return response.status(502).json({ error: 'Email delivery failed' });
    }
    return response.status(200).json({ success: true });
  } catch (error) {
    console.error('Contact email request failed:', error.name);
    return response.status(503).json({ error: 'Email service is temporarily unavailable' });
  } finally { clearTimeout(timeout); }
};
