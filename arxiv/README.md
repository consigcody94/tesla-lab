# Publishing & Archiving Guide

## arXiv Submission

1. Go to [arxiv.org/submit](https://arxiv.org/submit)
2. Upload `main.tex`, `references.bib`, and the `figures/` folder as a .zip
3. Category: **physics.class-ph** (Classical Physics) or **physics.hist-ph** (History and Philosophy of Physics)
4. The PDF is pre-built at `main.pdf` for reference

## Zenodo (DOI via GitHub)

Zenodo automatically archives GitHub releases and assigns a DOI.

1. Go to [zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/)
2. Log in with your GitHub account
3. Flip the toggle for `consigcody94/tesla-lab` to **ON**
4. Create a GitHub release (v1.0.0 is already created) — Zenodo will auto-archive it
5. Your DOI badge will appear at [zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/)
6. The `.zenodo.json` in the repo root provides metadata automatically

## OSF (Open Science Framework)

OSF requires OAuth authentication for API submissions. Manual submission:

1. Go to [osf.io](https://osf.io) and create an account
2. Click "Create Project" → title: "Dual-Mode Earth-Ionosphere Excitation"
3. Upload the PDF and link the GitHub repo
4. To create a preprint: go to [osf.io/preprints](https://osf.io/preprints) → choose a preprint service (e.g., EarthArXiv, engrXiv) → upload PDF
5. OSF API docs: [developer.osf.io](https://developer.osf.io) (requires OAuth2 token)

## ResearchGate

1. Go to [researchgate.net](https://www.researchgate.net)
2. Create a researcher profile
3. Click "Add Research" → "Article" → upload the PDF
4. This makes the paper discoverable by other researchers

## Google Scholar

Google Scholar automatically indexes:
- GitHub Pages (once live at consigcody94.github.io/tesla-lab/)
- arXiv preprints
- Zenodo DOIs

Add `<meta>` citation tags to the GitHub Pages index.html for better indexing.

## SSRN / viXra

- **SSRN:** [ssrn.com](https://www.ssrn.com) — social science / interdisciplinary preprints
- **viXra:** [vixra.org](https://vixra.org) — accepts any scientific paper, no review required
