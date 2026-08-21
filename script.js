const nav = document.getElementById('navlinks');
const menu = document.getElementById('menu');
const cvLink = document.querySelector('.hero-actions a[download]');

if (cvLink) {
  cvLink.href = new URL('assets/cv.pdf', document.baseURI).href;
  cvLink.removeAttribute('download');
  cvLink.target = '_blank';
  cvLink.rel = 'noopener';
  cvLink.textContent = 'View CV ↗';
  cvLink.setAttribute('aria-label', 'My CV');
  cvLink.title = 'View my CV';
}

menu?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menu.setAttribute('aria-expanded', open);
});

nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => nav.classList.remove('open')));

const roles = ['Web2 & Web3 Social Media Manager', 'Community Manager', 'Discord & Telegram Moderator'];
let role = 0;
let character = 0;
let deleting = false;
const typing = document.getElementById('typing');

function typeRole() {
  const word = roles[role];
  typing.textContent = word.slice(0, character);
  if (!deleting && character < word.length) {
    character++;
    setTimeout(typeRole, 48);
  } else if (deleting && character > 0) {
    character--;
    setTimeout(typeRole, 27);
  } else {
    deleting = !deleting;
    if (!deleting) role = (role + 1) % roles.length;
    setTimeout(typeRole, deleting ? 1500 : 260);
  }
}
typeRole();

const revealObserver = 'IntersectionObserver' in window && new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.13 });
document.querySelectorAll('.reveal, .skill').forEach(element => {
  if (revealObserver) revealObserver.observe(element);
  else element.classList.add('show');
});

const counterObserver = 'IntersectionObserver' in window && new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    document.querySelectorAll('.count').forEach(element => {
      const target = Number(element.dataset.count);
      const suffix = element.dataset.suffix;
      let value = 0;
      const animate = () => {
        value += Math.ceil(target / 48);
        if (value >= target) {
          element.textContent = target + suffix;
          return;
        }
        element.textContent = value;
        requestAnimationFrame(animate);
      };
      animate();
    });
    counterObserver.disconnect();
  });
}, { threshold: 0.45 });
document.querySelectorAll('.achievements').forEach(element => {
  if (counterObserver) counterObserver.observe(element);
});

const navItems = [...document.querySelectorAll('.navlinks a')];
const sections = [...document.querySelectorAll('main section[id]')];
const toTop = document.getElementById('toTop');
window.addEventListener('scroll', () => {
  let current = 'home';
  sections.forEach(section => {
    if (window.scrollY >= section.offsetTop - 120) current = section.id;
  });
  navItems.forEach(item => item.classList.toggle('active', item.getAttribute('href') === `#${current}`));
  toTop.classList.toggle('show', window.scrollY > 500);
});
toTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  [['name', 100], ['email', 254], ['subject', 160], ['message', 5000]].forEach(([field, limit]) => {
    contactForm.elements[field]?.setAttribute('maxlength', String(limit));
  });
  const honeypot = document.createElement('input');
  honeypot.name = 'website';
  honeypot.autocomplete = 'off';
  honeypot.tabIndex = -1;
  honeypot.className = 'honeypot';
  honeypot.setAttribute('aria-hidden', 'true');
  contactForm.append(honeypot);
}
document.getElementById('contactForm')?.addEventListener('submit', async event => {
  event.preventDefault();
  const formElement = event.currentTarget;
  const submitButton = formElement.querySelector('button[type="submit"]');
  const note = document.getElementById('formNote');

  submitButton.disabled = true;
  submitButton.textContent = 'Sending...';
  note.style.display = 'none';

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12_000);
  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
      body: JSON.stringify(Object.fromEntries(new FormData(formElement)))
    });

    if (!response.ok) throw new Error('Unable to send the message.');

    formElement.reset();
    note.textContent = 'Thank you! Your message has been sent.';
    note.style.display = 'inline';
  } catch (error) {
    note.textContent = 'Sorry, your message could not be sent. Please try again later.';
    note.style.color = '#ff9db5';
    note.style.display = 'inline';
  } finally {
    clearTimeout(timeout);
    submitButton.disabled = false;
    submitButton.textContent = 'Send Message ↗';
  }
});
