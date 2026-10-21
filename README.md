# Nudimane (ನುಡಿಮನೆ) — Your home for Kannada
Redesigned NammaVerse: same working features (OCR, Q&A search, learning, voice, heritage, travel, library, quality), new name, logo, flow and a Pinterest-style **Blush & Sage** look.

Palette: cream `#FBF6F1` · dusty rose `#E8B4B8` · sage `#A8BFA3` · deep plum `#3B2A3A` (tints: `#F6DDE0`, `#DCE7D8`, `#6F8F6A`).

## Structure
- `app.py` — the whole app (top nav, landing page, all tools)
- `assets/` — `hero.png` (project image), `logo_mark.png/.svg`, `logo_full.png`, `t_*.png` (card art)
- `.streamlit/config.toml` — theme (this must live inside the `.streamlit` folder)
- `requirements.txt`, `packages.txt` — Python deps and Tesseract + Kannada data

## Deploy on Streamlit Community Cloud
Upload everything (keep the `assets` and `.streamlit` folders) to GitHub, create the app, set main file `app.py`.

## Local run
`sudo apt-get install tesseract-ocr tesseract-ocr-kan` (or your OS equivalent), then
`pip install -r requirements.txt && streamlit run app.py`

Notes: OCR is a draft; Q&A is keyword search; library is session-only; heritage entries are starter examples needing community review.
