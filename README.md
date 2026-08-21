# Abdul-Quadri Akewusola — Portfolio

A responsive personal portfolio for Abdul-Quadri Akewusola, a Web3 Community Manager and Project Lead. It highlights community growth, launch support, skills, selected work, experience, and ways to get in touch.

## Features

- Responsive single-page layout
- Hero, about, skills, services, portfolio, experience, and contact sections
- Downloadable CV at `assets/cv.pdf`
- Animated section reveals, skill bars, counters, and active navigation
- Contact form backed by a Vercel serverless function and Resend

## Project structure

```text
├── api/
│   └── contact.js          # Vercel contact-form endpoint
├── assets/
│   ├── cv.pdf              # Downloadable CV
│   └── metaim.jpeg         # Profile image
├── index.html              # Page markup
├── styles.css              # Visual styles and responsive layout
├── script.js               # Interactions and form submission
└── README.md
```

## Run locally

This is a static site. Open `index.html` in a browser, or serve the folder with any local web server. For example, using VS Code, install the **Live Server** extension and select **Open with Live Server**.

The contact form needs a deployed Vercel environment to send emails; the rest of the site, including the CV, works locally.

## Update content

- **Text and sections:** edit `index.html`.
- **Styles and spacing:** edit `styles.css`.
- **Interactions:** edit `script.js`.
- **Profile image:** replace `assets/metaim.jpeg`.
- **CV:** replace `assets/cv.pdf`, retaining that filename.

## Deploy on Vercel

1. Push this folder to a GitHub repository.
2. Import the repository in [Vercel](https://vercel.com/).
3. Keep the default settings; no build command is required.
4. Add the environment variables below.
5. Redeploy the project.

## Contact form setup

The contact form sends messages through the Vercel function at `api/contact.js` using [Resend](https://resend.com/).

1. Create a Resend account and generate an API key.
2. In Vercel, go to **Project Settings → Environment Variables**.
3. Add `RESEND_API_KEY` with your Resend API key. Apply it to Production, Preview, and Development.
4. Redeploy the site.

For production, verify a sending domain in Resend and add:

```env
CONTACT_FROM=Abdul-Quadri Akewusola <contact@yourdomain.com>
```

The form recipient defaults to the address configured in `api/contact.js`. To override it without editing code, add:

```env
CONTACT_TO=your-email@example.com
```

For a custom domain, also set the origin permitted to submit the contact form:

```env
CONTACT_ALLOWED_ORIGIN=https://yourdomain.com
```

## Notes

- Do not commit your `RESEND_API_KEY` to the repository.
- Keep `CONTACT_TO`, `CONTACT_FROM`, and `CONTACT_ALLOWED_ORIGIN` as Vercel environment variables; never expose credentials in client-side files.
- After replacing the CV, redeploy the site so the new PDF is available to visitors.
