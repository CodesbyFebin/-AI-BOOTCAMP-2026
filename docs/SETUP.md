# Local Setup

The showcase is static HTML/CSS and needs no build step. Curriculum examples may use Python, JavaScript, notebooks, databases, containers, or hosted model APIs depending on the selected lesson.

## Basic tools

- Git and a GitHub account
- A current Python 3 release for Python examples
- Node.js for JavaScript and Next.js examples
- A code editor and terminal
- JupyterLab or another notebook interface for notebook lessons

Use each upstream project's own setup instructions and supported version ranges. This repository does not prescribe a single global dependency set for all external examples.

## Safe credentials

- Store provider keys in environment variables or a local ignored `.env` file.
- Never commit API keys, tokens, private datasets, wallet secrets, or personal information.
- Check an example's data handling and provider costs before running it.
- Prefer local or mock providers when available for first experiments.

## Preview the site

Open `site/index.html` in a browser or run a static local server from the repository root:

```bash
python -m http.server 8000 --directory site
```

Then visit `http://localhost:8000`.
