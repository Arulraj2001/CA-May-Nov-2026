# Banking Awareness, Static GK & Current Affairs 2026 — All-in-One Study Hub (SBI & IBPS Mains)

**Live Study Hub:** https://arulraj2001.github.io/CA-May-Nov-2026/

An offline-ready, single-hub MCQ & Flashcard study platform containing **2,832 curated questions** (**2,753 unique**) across **22 packs** for **SBI Clerk Mains, SBI PO, IBPS PO/Clerk, RRB, and RBI** General Awareness preparation (May–November 2026).

## Direct Subject Archives (Searchable & Printable)
- **Interactive All-in-One Hub:** https://arulraj2001.github.io/CA-May-Nov-2026/
- **Static GK (794 items):** https://arulraj2001.github.io/CA-May-Nov-2026/static-gk.html
- **Banking Awareness (788 items):** https://arulraj2001.github.io/CA-May-Nov-2026/banking-awareness.html
- **SBI Clerk Mains 6-Month GA (266 items):** https://arulraj2001.github.io/CA-May-Nov-2026/sbi-clerk-mains-ga.html
- **Veranda 6-Month Current Affairs Parts 1–6 (984 items):** https://arulraj2001.github.io/CA-May-Nov-2026/veranda-6m-ca.html

## Included Study Packs (22 Active Packs)
| Subject Group | Packs Included | Total Items |
| :--- | :--- | :---: |
| **Static GK** | Master Verified Sheet (Flashcards v2), General Static GK, August, September, October 2026 | 794 |
| **Banking Awareness** | Pages 1–10 Fact-Checked MCQs, Banking Awareness PDF (New & Repeated) | 788 |
| **SBI Clerk Mains 6M GA** | 6-Month General Awareness (New & Repeated) | 266 |
| **Veranda 6M CA Rapid Revision** | Parts 1–6 (Slides #1–#1000, New & Repeated) | 984 |

## Key Features
- **Learn Mode:** View answers, options, and exam notes with a one-click **Hide Answers** blur toggle for self-testing.
- **Practice Mode:** Interactive MCQ grading and flashcard self-assessment with live accuracy tracking.
- **Quick Quiz Mode:** Shuffled 25 / 50 / 100-question tests from any pack, category, or your Mistake Notebook.
- **Smart Lists & Filters:** Filter by **Fact-Check Updated (2026)**, **Bookmarked**, **Mistake Notebook**, **Unattempted**, or **Unique Only** (tags cross-pack duplicates).
- **Progress Persistence & Backup:** Saves progress in `localStorage` with one-click JSON Backup/Restore across devices.
- **White & Dark Themes + Print/PDF support.**

## How to Update Questions
1. Place new or updated source `.html` files inside `sources/` and register new files in `PACK_SPECS` inside `build_study_hub.py`.
2. Rebuild all hub & SEO pages (`index.html`, static subject pages, `sitemap.xml`, `robots.txt`):
   ```powershell
   python build_study_hub.py
   ```
3. Commit and push to `main`:
   ```powershell
   git add -A
   git commit -m "Update study hub questions"
   git push
   ```
