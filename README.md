# Abdul-Quadri Akewusola — Portfolio

A responsive personal portfolio for Abdul-Quadri Akewusola, a Web3 Community Manager and Project Lead. It highlights community growth, launch support, skills, selected work, experience, and ways to get in touch.

## Features

- Responsive single-page layout
- Hero, about, skills, services, portfolio, experience, and contact sections
- Downloadable CV at `assets/CVE.pdf`
- Animated section reveals, skill bars, counters, and active navigation
- Contact form backed by a Vercel serverless function and Resend

## Project structure

```text
├── api/
│   └── contact.js          # Vercel contact-form endpoint
├── assets/
│   ├── CVE.pdf             # Downloadable CV
│   └── metaim.jpeg         # Profile image
├── index.html              # Page markup
├── styles.css              # Visual styles and responsive layout
├── script.js               # Interactions and form submission
└── README.md
```

## Run locally

This is a static site. Open `index.html` in a browser, or serve the folder with any local web server. For example, using VS Code, install the **Live Server** extension and select **Open with Live Server**.

The contact form needs a deployed Vercel environment to send emails; the rest of the site, including the CV, works locally.

