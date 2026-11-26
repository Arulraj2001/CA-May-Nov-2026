# CA May–Nov 2026 — All-in-One Study Hub

Unified offline & GitHub Pages study hub for Banking Awareness, Static GK, SBI Clerk Mains 6-Month GA, and Veranda 6-Month Current Affairs (22 packs, 2,832 items).

## Files
- `index.html` — Live GitHub Pages entry point (compiled self-contained app)
- `build_study_hub.py` — Compiler script that builds `index.html` and `All_In_One_Study_Hub.html` from `sources/`
- `sources/` — Cleanly named source HTML files (plus `sources/superseded/` for older versions)

## How to Update Questions
1. Add or update your source `.html` file inside `sources/` and register it in `PACK_SPECS` inside `build_study_hub.py` (if new).
2. Run:
   ```powershell
   python build_study_hub.py
   ```
3. Commit and push to `main` — GitHub Pages updates automatically within ~1 minute:
   ```powershell
   git add -A
   git commit -m "Update study hub questions"
   git push
   ```
