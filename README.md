# Engineering Production AI

Personal engineering publication for Lokesh Jain. Built with Astro and Markdown content collections.

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:4321.

## Build

```bash
npm run build
npm run preview
```

## Publish

1. Create a GitHub repository and push this folder.
2. Deploy with Cloudflare Pages or another static host. Build command: `npm run build`; output directory: `dist`.
3. Replace `https://example.com` in `astro.config.mjs` with your real domain **before deployment** (important for RSS/canonical links).
4. Point your custom domain to the host following its DNS instructions.
5. Review the article and all professional details before making the site public.

## Write an article

Add a `.md` file to `src/content/articles/` with frontmatter:

```yaml
---
title: "Your title"
description: "Short summary"
pubDate: 2026-10-22
category: "Distributed Systems"
readingTime: "8 min read"
featured: false
---
```

Then write Markdown below the frontmatter. Articles automatically appear in the index, home page, and RSS feed.

## Customization

- Brand, navigation, footer, typography, and colors: `src/layouts/Base.astro`
- Home page: `src/pages/index.astro`
- About and Projects: `src/pages/about.astro`, `src/pages/projects.astro`
- Articles: `src/content/articles/`

## Privacy

No analytics or tracking scripts are included. The site loads fonts from Google Fonts; self-host fonts if you prefer to avoid third-party font requests. Avoid publishing confidential employer architecture, internal metrics, or proprietary code.
