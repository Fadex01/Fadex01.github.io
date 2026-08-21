/**
 * Vercel serverless function for the portfolio contact form.
 *
 * Required Vercel environment variable:
 *   RESEND_API_KEY
 *
 * Optional environment variables:
 *   CONTACT_TO   - recipient address (defaults to the portfolio owner's email)
 *   CONTACT_FROM - verified sender, e.g. "Portfolio <contact@yourdomain.com>"
 */
module.exports = async function handler(request, response) {
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return response.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, subject, message } = request.body || {};
  if (![name, email, subject, message].every(value => typeof value === 'string' && value.trim())) {
    return response.status(400).json({ error: 'All fields are required' });
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    return response.status(400).json({ error: 'Please provide a valid email address' });
  }

  if (!process.env.RESEND_API_KEY) {
    return response.status(500).json({ error: 'Email service is not configured' });
  }

  const escapeHtml = value => value.replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[character]));

  const emailResponse = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: process.env.CONTACT_FROM || 'Portfolio Contact <onboarding@resend.dev>',
      to: [process.env.CONTACT_TO || 'okorofarid07@gmail.com'],
      reply_to: email.trim(),
      subject: `Portfolio contact: ${subject.trim()}`,
      html: `
        <h2>New portfolio contact message</h2>
        <p><strong>Name:</strong> ${escapeHtml(name.trim())}</p>
        <p><strong>Email:</strong> ${escapeHtml(email.trim())}</p>
        <p><strong>Subject:</strong> ${escapeHtml(subject.trim())}</p>
        <p><strong>Message:</strong><br>${escapeHtml(message.trim()).replace(/\n/g, '<br>')}</p>
      `
    })
  });

  if (!emailResponse.ok) {
    console.error('Resend email error:', await emailResponse.text());
    return response.status(502).json({ error: 'Email delivery failed' });
  }

  return response.status(200).json({ success: true });
};
