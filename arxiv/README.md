# arXiv Submission Instructions

## Paper Details
- **Title:** Dual-Mode Earth-Ionosphere Excitation: Reconciling Tesla's Colorado Springs Observations with Modern Electromagnetic Theory
- **Author:** Cody Churchwell (Sentinel Owl Technologies, Rockville, MD)
- **Primary category:** physics.class-ph (Classical Physics)
- **Cross-list:** physics.hist-ph (History and Philosophy of Physics)

## Files to Submit
- `main.tex` — Main paper
- `references.bib` — Bibliography
- `figures/` — All figure PNGs (8 files)

## How to Submit

### 1. Create an arXiv Account
- Go to https://arxiv.org/user/register
- Use institutional or professional email
- You'll need to wait for account approval (can take 1-3 days for new accounts)

### 2. Get Endorsement (if needed)
- First-time submitters to physics.class-ph may need an endorsement
- arXiv will tell you after account creation if endorsement is required
- Find an endorser at https://arxiv.org/auth/endorse — any author who has published in physics.class-ph can endorse you

### 3. Compile Locally First
```bash
cd arxiv/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
Verify the PDF looks correct.

### 4. Submit
1. Go to https://arxiv.org/submit
2. Choose **New Submission**
3. Select primary category: **physics.class-ph**
4. Add cross-list: **physics.hist-ph**
5. Upload files: select all files in this directory (main.tex, references.bib, figures/*)
6. arXiv will compile it server-side — review the preview PDF
7. Fill in metadata (title, abstract, authors) — copy from the paper
8. Submit!

### 5. After Submission
- Paper appears on arXiv within 1-2 business days
- You'll get an arXiv ID (e.g., 2602.XXXXX)
- You can update/replace the paper anytime via the arXiv dashboard

## Notes
- arXiv uses TeX Live for compilation — revtex4-2 is included by default
- PNG figures are fine (no need to convert to PDF/EPS)
- The paper uses `revtex4-2` document class which is standard for physics preprints
