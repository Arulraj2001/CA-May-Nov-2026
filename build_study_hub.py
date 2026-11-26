"""
Compile all HTML study files in ./sources into a single self-contained
All_In_One_Study_Hub.html file with unified search, Learn/Practice/Quick Quiz
modes, progress persistence (localStorage), and duplicate tagging.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES_DIR = ROOT / "sources"
OUTPUT_FILE = ROOT / "All_In_One_Study_Hub.html"
PAGES_INDEX_FILE = ROOT / "index.html"

# Ordered pack definitions mapped to renamed files in sources/
PACK_SPECS = [
    # Static GK
    {
        "id": "static-gk-flashcards-v2",
        "file": "02_Static_GK_Master_Verified_Flashcards_v2.html",
        "group": "Static GK",
        "name": "Master Verified Sheet (Flashcards v2)",
        "subType": "Flashcards",
        "parser": "sections",
        "priority": 1,
    },
    {
        "id": "static-gk-general",
        "file": "03_Static_GK_General_MCQs.html",
        "group": "Static GK",
        "name": "General Static GK",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "static-gk-aug",
        "file": "04_Static_GK_2026-08_Aug_MCQs.html",
        "group": "Static GK",
        "name": "August Static GK",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "static-gk-sep",
        "file": "05_Static_GK_2026-09_Sep_MCQs.html",
        "group": "Static GK",
        "name": "September Static GK",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "static-gk-oct",
        "file": "06_Static_GK_2026-10_Oct_MCQs.html",
        "group": "Static GK",
        "name": "October Static GK",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    # Banking Awareness
    {
        "id": "banking-pages-1-10",
        "file": "01_Banking_GK_Pages1-10_FactChecked_MCQs.html",
        "group": "Banking Awareness",
        "name": "Pages 1–10 Fact-Checked MCQs",
        "subType": "Fact-Checked",
        "parser": "raw_data",
        "priority": 1,
    },
    {
        "id": "banking-pdf-new",
        "file": "07_Banking_Awareness_PDF_New_MCQs.html",
        "group": "Banking Awareness",
        "name": "Banking Awareness PDF (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "banking-pdf-rep",
        "file": "08_Banking_Awareness_PDF_Repeated_MCQs.html",
        "group": "Banking Awareness",
        "name": "Banking Awareness PDF (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    # SBI Clerk Mains 6M GA
    {
        "id": "sbi-6m-ga-new",
        "file": "09_SBI_Clerk_Mains_6M_GA_New_MCQs.html",
        "group": "SBI Clerk Mains 6M GA",
        "name": "SBI Clerk Mains 6M GA (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "sbi-6m-ga-rep",
        "file": "10_SBI_Clerk_Mains_6M_GA_Repeated_MCQs.html",
        "group": "SBI Clerk Mains 6M GA",
        "name": "SBI Clerk Mains 6M GA (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    # Veranda 6-Month CA Rapid Revision
    {
        "id": "veranda-p1-new",
        "file": "11_Veranda_6M_CA_Part1_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 1 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p1-rep",
        "file": "12_Veranda_6M_CA_Part1_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 1 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    {
        "id": "veranda-p2-new",
        "file": "13_Veranda_6M_CA_Part2_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 2: Slides #101–#330 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p2-rep",
        "file": "14_Veranda_6M_CA_Part2_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 2: Slides #101–#330 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    {
        "id": "veranda-p3-new",
        "file": "15_Veranda_6M_CA_Part3_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 3: Slides #330–#445 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p3-rep",
        "file": "16_Veranda_6M_CA_Part3_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 3: Slides #330–#445 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    {
        "id": "veranda-p4-new",
        "file": "17_Veranda_6M_CA_Part4_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 4: Slides #451–#600 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p4-rep",
        "file": "18_Veranda_6M_CA_Part4_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 4: Slides #451–#600 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    {
        "id": "veranda-p5-new",
        "file": "19_Veranda_6M_CA_Part5_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 5: Slides #601–#798 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p5-rep",
        "file": "20_Veranda_6M_CA_Part5_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 5: Slides #601–#798 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
    {
        "id": "veranda-p6-new",
        "file": "21_Veranda_6M_CA_Part6_New_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 6: Slides #801–#1000 (New)",
        "subType": "New",
        "parser": "questions",
        "priority": 2,
    },
    {
        "id": "veranda-p6-rep",
        "file": "22_Veranda_6M_CA_Part6_Repeated_MCQs.html",
        "group": "Veranda 6M CA Rapid Revision",
        "name": "Part 6: Slides #801–#1000 (Repeated)",
        "subType": "Repeated",
        "parser": "questions",
        "priority": 4,
    },
]


def norm_text(text: str) -> str:
    """Normalize question text for cross-pack duplicate detection."""
    s = re.sub(r"\s+", " ", text.strip().lower())
    s = re.sub(r"[^\w\s]", "", s)
    return s


def parse_questions_file(path: Path, spec: dict) -> list[dict]:
    """Parse standard *_White_Theme.html files containing const QUESTIONS = [...];"""
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"const QUESTIONS = (\[.*?\]);", txt, re.S)
    if not m:
        raise ValueError(f"Could not find QUESTIONS in {path}")
    raw = json.loads(m.group(1))
    items = []
    for idx, x in enumerate(raw, start=1):
        refs = []
        if "pdf_num" in x and x["pdf_num"] is not None:
            refs.append(f"PDF #{x['pdf_num']}")
        if "slide_q" in x and x["slide_q"] is not None:
            refs.append(f"Slide #{x['slide_q']}")
        if "video_q" in x and x["video_q"] is not None:
            refs.append(f"Video #{x['video_q']}")
        items.append(
            {
                "uid": f"{spec['id']}::{x.get('id', idx)}",
                "num": x.get("id", idx),
                "pack": spec["id"],
                "cat": x.get("cat", "General"),
                "type": "mcq",
                "q": x["q"],
                "opts": x["opts"],
                "ans": x["ans"],
                "p1": x.get("p1", ""),
                "p2": x.get("p2", ""),
                "factUpdated": False,
                "ref": " | ".join(refs),
            }
        )
    return items


def parse_raw_data_file(path: Path, spec: dict) -> list[dict]:
    """Parse 01_Banking_GK_Pages1-10_FactChecked_MCQs.html (const RAW_DATA = [...])."""
    txt = path.read_text(encoding="utf-8")
    page_labels = dict(
        re.findall(r'<option value="(\d+)">([^<]+)</option>', txt)
    )
    m = re.search(r"const RAW_DATA = \[(.*?)\];\s*\n", txt, re.S)
    if not m:
        raise ValueError(f"Could not find RAW_DATA in {path}")
    body = re.sub(r"^\s*//.*$", "", m.group(1), flags=re.M)
    body = re.sub(r",\s*$", "", body.strip())
    rows = json.loads("[" + body + "]")
    items = []
    for row in rows:
        q_num, page, q_text, opts, ans_idx, is_updated, explanation = row
        cat = page_labels.get(str(page), f"Page {page}")
        items.append(
            {
                "uid": f"{spec['id']}::{q_num}",
                "num": q_num,
                "pack": spec["id"],
                "cat": cat,
                "type": "mcq",
                "q": q_text,
                "opts": opts,
                "ans": ans_idx,
                "p1": explanation,
                "p2": "",
                "factUpdated": bool(is_updated),
                "ref": f"Page {page} | Q#{q_num}",
            }
        )
    return items


def parse_sections_file(path: Path, spec: dict) -> list[dict]:
    """Parse 02_Static_GK_Master_Verified_Flashcards_v2.html (const sections = [...])."""
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"const sections = (\[.*?\]);\s*\n", txt, re.S)
    if not m:
        raise ValueError(f"Could not find sections in {path}")
    js = m.group(1)
    js = re.sub(r'(\{|,|\s)(id|title|items|q|a|updated)\s*:', r'\1"\2":', js)
    sections = json.loads(js)
    items = []
    counter = 0
    for sec in sections:
        cat = sec["title"]
        for it in sec["items"]:
            counter += 1
            items.append(
                {
                    "uid": f"{spec['id']}::{counter}",
                    "num": counter,
                    "pack": spec["id"],
                    "cat": cat,
                    "type": "flashcard",
                    "q": it["q"],
                    "a": it["a"],
                    "p1": "",
                    "p2": "",
                    "factUpdated": bool(it.get("updated", False)),
                    "ref": f"Master Sheet #{counter}",
                }
            )
    return items


PARSERS = {
    "questions": parse_questions_file,
    "raw_data": parse_raw_data_file,
    "sections": parse_sections_file,
}


def build_dataset() -> tuple[list[dict], list[dict]]:
    all_items: list[dict] = []
    packs_meta: list[dict] = []
    priority_map = {s["id"]: s["priority"] for s in PACK_SPECS}

    for spec in PACK_SPECS:
        path = SOURCES_DIR / spec["file"]
        if not path.exists():
            raise FileNotFoundError(f"Missing source file: {path}")
        items = PARSERS[spec["parser"]](path, spec)
        all_items.extend(items)
        packs_meta.append(
            {
                "id": spec["id"],
                "group": spec["group"],
                "name": spec["name"],
                "subType": spec["subType"],
                "count": len(items),
                "sourceFile": spec["file"],
            }
        )

    # Detect cross-pack duplicates while keeping all items intact
    by_norm: dict[str, list[int]] = {}
    for idx, item in enumerate(all_items):
        key = norm_text(item["q"])
        by_norm.setdefault(key, []).append(idx)

    for indices in by_norm.values():
        if len(indices) <= 1:
            idx = indices[0]
            all_items[idx]["dupCount"] = 1
            all_items[idx]["isDupCopy"] = False
            continue
        # Pick primary occurrence: lowest priority number (Fact-Checked > New > Repeated), then first seen
        best_idx = min(
            indices,
            key=lambda i: (priority_map.get(all_items[i]["pack"], 9), i),
        )
        for i in indices:
            all_items[i]["dupCount"] = len(indices)
            all_items[i]["isDupCopy"] = i != best_idx

    return packs_meta, all_items


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>All-in-One Study Hub — Banking, Static GK &amp; Current Affairs</title>
<style>
  :root {
    --bg-page: #f8fafc;
    --bg-surface: #ffffff;
    --bg-panel: #f1f5f9;
    --bg-hover: #eef2ff;
    --border-light: #e2e8f0;
    --border-strong: #cbd5e1;
    --text-main: #0f172a;
    --text-sub: #334155;
    --text-muted: #64748b;
    --primary: #1d4ed8;
    --primary-hover: #1e40af;
    --primary-soft: #eff6ff;
    --primary-border: #bfdbfe;
    --green-bg: #f0fdf4;
    --green-border: #22c55e;
    --green-text: #15803d;
    --red-bg: #fef2f2;
    --red-border: #ef4444;
    --red-text: #b91c1c;
    --amber-bg: #fffbeb;
    --amber-border: #f59e0b;
    --amber-text: #92400e;
    --purple-bg: #f5f3ff;
    --purple-border: #c4b5fd;
    --purple-text: #6d28d9;
    --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
    --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  }

  body.dark {
    --bg-page: #0b1120;
    --bg-surface: #111827;
    --bg-panel: #1e293b;
    --bg-hover: #1e293b;
    --border-light: #1f2937;
    --border-strong: #334155;
    --text-main: #f1f5f9;
    --text-sub: #cbd5e1;
    --text-muted: #94a3b8;
    --primary: #38bdf8;
    --primary-hover: #0ea5e9;
    --primary-soft: rgba(56, 189, 248, 0.12);
    --primary-border: rgba(56, 189, 248, 0.35);
    --green-bg: rgba(34, 197, 94, 0.14);
    --green-border: #22c55e;
    --green-text: #4ade80;
    --red-bg: rgba(239, 68, 68, 0.14);
    --red-border: #ef4444;
    --red-text: #f87171;
    --amber-bg: rgba(245, 158, 11, 0.14);
    --amber-border: #f59e0b;
    --amber-text: #fbbf24;
    --purple-bg: rgba(139, 92, 246, 0.15);
    --purple-border: #7c3aed;
    --purple-text: #c4b5fd;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.45);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background-color: var(--bg-page);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Arial, sans-serif;
    line-height: 1.55;
    min-height: 100vh;
  }

  /* Top Header */
  header {
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border-light);
    position: sticky;
    top: 0;
    z-index: 200;
    padding: 10px 18px;
    box-shadow: var(--shadow-sm);
  }

  .header-inner {
    max-width: 1440px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  .brand-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .sidebar-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-strong);
    background: var(--bg-surface);
    color: var(--text-main);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 0.9rem;
    cursor: pointer;
  }

  .brand-title h1 {
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.2;
  }

  .brand-title p {
    font-size: 0.76rem;
    color: var(--text-muted);
  }

  .header-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
  }

  .mode-tabs {
    display: inline-flex;
    background: var(--bg-panel);
    border: 1px solid var(--border-light);
    border-radius: 9px;
    padding: 3px;
    gap: 3px;
  }

  .tab-btn {
    border: none;
    background: transparent;
    color: var(--text-sub);
    font-size: 0.84rem;
    font-weight: 600;
    padding: 6px 13px;
    border-radius: 6px;
    cursor: pointer;
    transition: 0.15s ease;
  }

  .tab-btn.active {
    background: var(--bg-surface);
    color: var(--primary);
    box-shadow: var(--shadow-sm);
  }

  .icon-btn {
    border: 1px solid var(--border-strong);
    background: var(--bg-surface);
    color: var(--text-sub);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 11px;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.15s ease;
  }

  .icon-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
  }

  .icon-btn.active-toggle {
    background: var(--primary-soft);
    border-color: var(--primary);
    color: var(--primary);
  }

  /* Layout */
  .app-shell {
    max-width: 1440px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 290px 1fr;
    gap: 18px;
    padding: 16px 18px 48px;
    align-items: start;
  }

  .app-shell.sidebar-collapsed {
    grid-template-columns: 1fr;
  }

  .app-shell.sidebar-collapsed .sidebar {
    display: none;
  }

  /* Sidebar */
  .sidebar {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 12px;
    position: sticky;
    top: 72px;
    max-height: calc(100vh - 90px);
    overflow-y: auto;
    box-shadow: var(--shadow-sm);
  }

  .side-section-label {
    font-size: 0.71rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    padding: 8px 8px 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav-item {
    width: 100%;
    text-align: left;
    border: 1px solid transparent;
    background: transparent;
    color: var(--text-sub);
    padding: 7px 9px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 2px;
    transition: 0.12s ease;
  }

  .nav-item:hover {
    background: var(--bg-panel);
    color: var(--text-main);
  }

  .nav-item.active {
    background: var(--primary-soft);
    border-color: var(--primary-border);
    color: var(--primary);
    font-weight: 700;
  }

  .nav-label {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }

  .nav-badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 999px;
    background: var(--bg-panel);
    color: var(--text-muted);
    flex-shrink: 0;
  }

  .nav-item.active .nav-badge {
    background: var(--primary);
    color: #fff;
  }

  body.dark .nav-item.active .nav-badge {
    color: #0b1120;
  }

  .group-header {
    width: 100%;
    border: none;
    background: transparent;
    color: var(--text-main);
    font-size: 0.8rem;
    font-weight: 700;
    padding: 8px 8px 4px;
    margin-top: 6px;
    border-top: 1px solid var(--border-light);
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
  }

  .group-items.collapsed {
    display: none;
  }

  /* Main Area */
  .main-content {
    min-width: 0;
  }

  .controls-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .controls-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  .filter-inputs {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    flex: 1;
  }

  select, input[type="text"] {
    border: 1px solid var(--border-strong);
    background: var(--bg-surface);
    color: var(--text-main);
    border-radius: 8px;
    padding: 7px 11px;
    font-size: 0.85rem;
    outline: none;
  }

  select:focus, input[type="text"]:focus {
    border-color: var(--primary);
  }

  #searchBox {
    flex: 1;
    min-width: 220px;
  }

  #catSelect {
    max-width: 280px;
  }

  .check-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-sub);
    background: var(--bg-panel);
    border: 1px solid var(--border-light);
    padding: 5px 10px;
    border-radius: 8px;
    cursor: pointer;
    user-select: none;
  }

  .stats-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border-light);
  }

  .pill-group {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }

  .stat-pill {
    font-size: 0.78rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    background: var(--bg-panel);
    color: var(--text-sub);
    border: 1px solid var(--border-light);
  }

  .stat-pill.green { background: var(--green-bg); border-color: var(--green-border); color: var(--green-text); }
  .stat-pill.red { background: var(--red-bg); border-color: var(--red-border); color: var(--red-text); }
  .stat-pill.amber { background: var(--amber-bg); border-color: var(--amber-border); color: var(--amber-text); }

  /* Quick Quiz Banner */
  .quiz-banner {
    display: none;
    background: var(--primary-soft);
    border: 1px solid var(--primary-border);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 14px;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  .quiz-banner.visible { display: flex; }

  .quiz-controls {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
  }

  .primary-btn {
    border: none;
    background: var(--primary);
    color: #fff;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 7px 14px;
    border-radius: 8px;
    cursor: pointer;
  }

  body.dark .primary-btn { color: #0b1120; }
  .primary-btn:hover { background: var(--primary-hover); }

  /* Pagination */
  .pagination-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin: 10px 0 14px;
    font-size: 0.82rem;
    color: var(--text-muted);
  }

  .page-btns {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  /* Question Cards */
  .cards-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .q-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.15s ease;
  }

  .q-card.fact-updated {
    border-left: 4px solid var(--amber-border);
  }

  .q-top {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 8px;
  }

  .q-tags {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }

  .tag {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 6px;
    background: var(--bg-panel);
    color: var(--text-sub);
    border: 1px solid var(--border-light);
  }

  .tag.pack { background: var(--primary-soft); border-color: var(--primary-border); color: var(--primary); }
  .tag.fact { background: var(--amber-bg); border-color: var(--amber-border); color: var(--amber-text); }
  .tag.dup { background: var(--purple-bg); border-color: var(--purple-border); color: var(--purple-text); }
  .tag.flash { background: var(--green-bg); border-color: var(--green-border); color: var(--green-text); }

  .bookmark-btn {
    border: 1px solid var(--border-light);
    background: transparent;
    color: var(--text-muted);
    border-radius: 7px;
    padding: 3px 9px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
  }

  .bookmark-btn.saved {
    background: var(--amber-bg);
    border-color: var(--amber-border);
    color: var(--amber-text);
  }

  .q-text {
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 12px;
  }

  /* Learn Mode */
  .learn-answer {
    background: var(--green-bg);
    border: 1px solid var(--green-border);
    border-radius: 9px;
    padding: 10px 13px;
    margin-bottom: 10px;
    transition: filter 0.15s ease;
  }

  .learn-answer.blurred {
    filter: blur(6px);
    user-select: none;
    cursor: pointer;
  }

  .learn-answer-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--green-text);
    margin-bottom: 2px;
  }

  .learn-answer-text {
    font-size: 0.94rem;
    font-weight: 700;
    color: var(--text-main);
  }

  .learn-opts-preview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 6px;
    margin-bottom: 10px;
  }

  .opt-chip {
    font-size: 0.82rem;
    padding: 6px 10px;
    border-radius: 7px;
    border: 1px solid var(--border-light);
    background: var(--bg-panel);
    color: var(--text-sub);
  }

  .opt-chip.correct-chip {
    background: var(--green-bg);
    border-color: var(--green-border);
    color: var(--green-text);
    font-weight: 700;
  }

  .learn-opts-preview.blurred .opt-chip.correct-chip {
    background: var(--bg-panel);
    border-color: var(--border-light);
    color: var(--text-sub);
    font-weight: 400;
  }

  .notes-box {
    background: var(--bg-panel);
    border-left: 3px solid var(--primary);
    border-radius: 0 8px 8px 0;
    padding: 9px 12px;
    font-size: 0.84rem;
    color: var(--text-sub);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .notes-box.fact-note {
    border-left-color: var(--amber-border);
    background: var(--amber-bg);
    color: var(--amber-text);
  }

  .notes-box.blurred {
    filter: blur(5px);
    user-select: none;
    cursor: pointer;
  }

  /* Practice Mode */
  .options-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .option-btn {
    text-align: left;
    border: 1.5px solid var(--border-strong);
    background: var(--bg-surface);
    color: var(--text-main);
    border-radius: 9px;
    padding: 10px 12px;
    font-size: 0.88rem;
    cursor: pointer;
    display: flex;
    align-items: flex-start;
    gap: 9px;
    transition: 0.12s ease;
  }

  .option-btn:hover:not(:disabled) {
    border-color: var(--primary);
    background: var(--primary-soft);
  }

  .option-btn:disabled { cursor: default; }

  .opt-letter {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px solid var(--border-strong);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 1px;
  }

  .option-btn.correct {
    background: var(--green-bg);
    border-color: var(--green-border);
    color: var(--green-text);
    font-weight: 700;
  }

  .option-btn.correct .opt-letter {
    background: var(--green-border);
    border-color: var(--green-border);
    color: #fff;
  }

  .option-btn.wrong {
    background: var(--red-bg);
    border-color: var(--red-border);
    color: var(--red-text);
  }

  .option-btn.wrong .opt-letter {
    background: var(--red-border);
    border-color: var(--red-border);
    color: #fff;
  }

  .flash-practice-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .flash-grade-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }

  .practice-feedback {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .empty-state {
    background: var(--bg-surface);
    border: 1px dashed var(--border-strong);
    border-radius: 12px;
    padding: 42px 20px;
    text-align: center;
    color: var(--text-muted);
  }

  @media (max-width: 960px) {
    .app-shell {
      grid-template-columns: 1fr;
    }
    .sidebar {
      position: static;
      max-height: none;
    }
  }

  @media (max-width: 640px) {
    .options-grid { grid-template-columns: 1fr; }
    #searchBox { min-width: 100%; }
  }

  @media print {
    header, .sidebar, .controls-card, .quiz-banner, .pagination-bar, .bookmark-btn {
      display: none !important;
    }
    .app-shell { display: block; padding: 0; }
    .q-card { break-inside: avoid; border: 1px solid #ccc; margin-bottom: 10px; }
    .learn-answer, .notes-box { filter: none !important; }
  }
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="brand-row">
      <button class="sidebar-toggle" id="sidebarToggleBtn" title="Toggle Sidebar">☰ Packs</button>
      <div class="brand-title">
        <h1>All-in-One Study Hub</h1>
        <p id="activePackSubtitle">Loading packs...</p>
      </div>
    </div>

    <div class="header-actions">
      <div class="mode-tabs">
        <button class="tab-btn active" id="modeLearnBtn" onclick="setMode('learn')">📖 Learn</button>
        <button class="tab-btn" id="modePracticeBtn" onclick="setMode('practice')">✍️ Practice</button>
        <button class="tab-btn" id="modeQuizBtn" onclick="setMode('quiz')">⚡ Quick Quiz</button>
      </div>
      <button class="icon-btn" id="blurToggleBtn" onclick="toggleBlur()">👁️ Hide Answers</button>
      <button class="icon-btn" id="themeBtn" onclick="toggleTheme()">🌙 Dark</button>
      <button class="icon-btn" onclick="exportProgress()" title="Download progress JSON">💾 Backup</button>
      <button class="icon-btn" onclick="document.getElementById('importFile').click()" title="Restore progress JSON">📂 Restore</button>
      <input type="file" id="importFile" accept=".json" style="display:none" onchange="importProgress(event)">
    </div>
  </div>
</header>

<div class="app-shell" id="appShell">
  <aside class="sidebar" id="sidebar"></aside>

  <main class="main-content">
    <div class="quiz-banner" id="quizBanner">
      <div>
        <strong id="quizTitle">⚡ Quick Quiz Generator</strong>
        <div style="font-size:0.8rem;color:var(--text-sub)" id="quizSubtitle">
          Generates a shuffled practice test from your current pack &amp; filters.
        </div>
      </div>
      <div class="quiz-controls">
        <select id="quizSizeSelect">
          <option value="25">25 Questions</option>
          <option value="50" selected>50 Questions</option>
          <option value="100">100 Questions</option>
        </select>
        <button class="primary-btn" onclick="startQuickQuiz()">🎲 New Shuffled Quiz</button>
        <button class="icon-btn" onclick="setMode('practice')">Exit Quiz</button>
      </div>
    </div>

    <div class="controls-card">
      <div class="controls-row">
        <div class="filter-inputs">
          <select id="catSelect" onchange="onFilterChange()">
            <option value="ALL">All Categories</option>
          </select>
          <input type="text" id="searchBox" placeholder="Search question, answer, options, or notes... (Press /)" oninput="onSearchInput()">
          <label class="check-pill" title="Hide duplicate copies of questions that appear in multiple packs">
            <input type="checkbox" id="hideDupChk" onchange="onFilterChange()">
            Unique Only
          </label>
          <label class="check-pill" title="Show only items with 2026 fact-check corrections">
            <input type="checkbox" id="factOnlyChk" onchange="onFilterChange()">
            Fact-Checked Only
          </label>
        </div>
      </div>

      <div class="stats-row">
        <div class="pill-group" id="statsPills"></div>
        <div class="pill-group">
          <button class="icon-btn" onclick="resetCurrentScope()">Reset Scope</button>
          <button class="icon-btn" onclick="window.print()">🖨️ Print</button>
        </div>
      </div>
    </div>

    <div class="pagination-bar" id="topPagination"></div>
    <div class="cards-list" id="cardsContainer"></div>
    <div class="pagination-bar" id="bottomPagination"></div>
  </main>
</div>

<script id="packs-data" type="application/json">__PACKS_JSON__</script>
<script id="items-data" type="application/json">__ITEMS_JSON__</script>
<script>
const PACKS = JSON.parse(document.getElementById("packs-data").textContent);
const ITEMS = JSON.parse(document.getElementById("items-data").textContent);
const PACK_MAP = Object.fromEntries(PACKS.map(p => [p.id, p]));

const STORAGE_KEY = "study_hub_progress_v1";
const PREFS_KEY = "study_hub_prefs_v1";

let state = {
  answers: {},     // uid -> { chosen: number|string, correct: boolean }
  bookmarks: {},   // uid -> true
};

let prefs = {
  dark: false,
  mode: "learn",   // learn | practice | quiz
  view: "ALL",     // ALL | SMART:FACT | SMART:BOOKMARKS | SMART:WRONG | SMART:UNATTEMPTED | packId
  blur: false,
  pageSize: 50,
  collapsedGroups: {},
};

let currentPage = 1;
let quizIds = [];
let quizSessionAnswers = {};
let searchTimer = null;

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      state.answers = parsed.answers || {};
      state.bookmarks = parsed.bookmarks || {};
    }
  } catch (e) {}

  try {
    const rawP = localStorage.getItem(PREFS_KEY);
    if (rawP) {
      prefs = { ...prefs, ...JSON.parse(rawP) };
    }
  } catch (e) {}

  if (prefs.dark) document.body.classList.add("dark");
  updateThemeBtn();
  updateModeUI();
}

function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
}

function savePrefs() {
  try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefs)); } catch (e) {}
}

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function getBaseScopedItems() {
  const v = prefs.view;
  if (v === "ALL") return ITEMS;
  if (v === "SMART:FACT") return ITEMS.filter(it => it.factUpdated);
  if (v === "SMART:BOOKMARKS") return ITEMS.filter(it => !!state.bookmarks[it.uid]);
  if (v === "SMART:WRONG") return ITEMS.filter(it => state.answers[it.uid] && !state.answers[it.uid].correct);
  if (v === "SMART:UNATTEMPTED") return ITEMS.filter(it => !state.answers[it.uid]);
  if (v.startsWith("GROUP:")) {
    const g = v.slice(6);
    const ids = new Set(PACKS.filter(p => p.group === g).map(p => p.id));
    return ITEMS.filter(it => ids.has(it.pack));
  }
  return ITEMS.filter(it => it.pack === v);
}

function getFilteredItems() {
  if (prefs.mode === "quiz") {
    const map = new Map(ITEMS.map(it => [it.uid, it]));
    return quizIds.map(id => map.get(id)).filter(Boolean);
  }

  let list = getBaseScopedItems();
  const cat = document.getElementById("catSelect").value;
  const q = document.getElementById("searchBox").value.trim().toLowerCase();
  const hideDup = document.getElementById("hideDupChk").checked;
  const factOnly = document.getElementById("factOnlyChk").checked;

  if (cat !== "ALL") list = list.filter(it => it.cat === cat);
  if (hideDup) list = list.filter(it => !it.isDupCopy);
  if (factOnly) list = list.filter(it => it.factUpdated);

  if (q) {
    list = list.filter(it => {
      if (it.q.toLowerCase().includes(q)) return true;
      if (it.cat.toLowerCase().includes(q)) return true;
      if (it.p1 && it.p1.toLowerCase().includes(q)) return true;
      if (it.p2 && it.p2.toLowerCase().includes(q)) return true;
      if (it.a && it.a.toLowerCase().includes(q)) return true;
      if (it.opts && it.opts.some(o => o.toLowerCase().includes(q))) return true;
      return false;
    });
  }
  return list;
}

function rebuildCategoryDropdown() {
  const sel = document.getElementById("catSelect");
  const prev = sel.value;
  const base = getBaseScopedItems();
  const counts = new Map();
  base.forEach(it => counts.set(it.cat, (counts.get(it.cat) || 0) + 1));

  sel.innerHTML = `<option value="ALL">All Categories (${base.length})</option>`;
  Array.from(counts.entries())
    .sort((a, b) => a[0].localeCompare(b[0]))
    .forEach(([cat, cnt]) => {
      const opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = `${cat} (${cnt})`;
      sel.appendChild(opt);
    });

  if ([...sel.options].some(o => o.value === prev)) {
    sel.value = prev;
  } else {
    sel.value = "ALL";
  }
}

function renderSidebar() {
  const sb = document.getElementById("sidebar");
  const factCnt = ITEMS.filter(i => i.factUpdated).length;
  const bmCnt = Object.keys(state.bookmarks).length;
  const wrongCnt = Object.values(state.answers).filter(a => !a.correct).length;
  const unattemptedCnt = ITEMS.length - Object.keys(state.answers).length;

  let html = `
    <div class="side-section-label"><span>Overview &amp; Smart Lists</span></div>
    ${sideBtn("ALL", "📚 All Study Items", ITEMS.length)}
    ${sideBtn("SMART:FACT", "🟡 Fact-Check Updated", factCnt)}
    ${sideBtn("SMART:BOOKMARKS", "⭐ Bookmarked", bmCnt)}
    ${sideBtn("SMART:WRONG", "❌ Mistake Notebook", wrongCnt)}
    ${sideBtn("SMART:UNATTEMPTED", "🆕 Unattempted", unattemptedCnt)}
  `;

  const groups = [];
  const seenG = new Set();
  PACKS.forEach(p => {
    if (!seenG.has(p.group)) {
      seenG.add(p.group);
      groups.push(p.group);
    }
  });

  groups.forEach(g => {
    const gPacks = PACKS.filter(p => p.group === g);
    const gTotal = gPacks.reduce((s, p) => s + p.count, 0);
    const isCollapsed = !!prefs.collapsedGroups[g];
    html += `
      <button class="group-header" onclick="toggleGroup('${escapeHtml(g)}')">
        <span>${isCollapsed ? "▸" : "▾"} ${escapeHtml(g)}</span>
        <span class="nav-badge">${gTotal}</span>
      </button>
      <div class="group-items ${isCollapsed ? "collapsed" : ""}">
        ${sideBtn("GROUP:" + g, "All in " + g, gTotal)}
    `;
    gPacks.forEach(p => {
      const done = ITEMS.filter(it => it.pack === p.id && state.answers[it.uid]).length;
      const badge = done > 0 ? `${done}/${p.count}` : `${p.count}`;
      html += sideBtn(p.id, p.name, badge);
    });
    html += `</div>`;
  });

  sb.innerHTML = html;
}

function sideBtn(id, label, badge) {
  const active = prefs.view === id ? "active" : "";
  return `<button class="nav-item ${active}" onclick="selectView('${escapeHtml(id)}')">
    <span class="nav-label" title="${escapeHtml(label)}">${escapeHtml(label)}</span>
    <span class="nav-badge">${escapeHtml(badge)}</span>
  </button>`;
}

function toggleGroup(g) {
  prefs.collapsedGroups[g] = !prefs.collapsedGroups[g];
  savePrefs();
  renderSidebar();
}

function selectView(viewId) {
  prefs.view = viewId;
  currentPage = 1;
  savePrefs();
  rebuildCategoryDropdown();
  if (prefs.mode === "quiz") startQuickQuiz();
  else render();
}

function updateSubtitle() {
  const el = document.getElementById("activePackSubtitle");
  const v = prefs.view;
  if (v === "ALL") el.textContent = `All 22 Packs Combined • ${ITEMS.length} Total Items`;
  else if (v === "SMART:FACT") el.textContent = "Smart View • Fact-Check Updated (2026 Corrections)";
  else if (v === "SMART:BOOKMARKS") el.textContent = "Smart View • Bookmarked Questions";
  else if (v === "SMART:WRONG") el.textContent = "Smart View • Mistake Notebook";
  else if (v === "SMART:UNATTEMPTED") el.textContent = "Smart View • Unattempted Questions";
  else if (v.startsWith("GROUP:")) el.textContent = `Subject Group • ${v.slice(6)}`;
  else {
    const p = PACK_MAP[v];
    el.textContent = p ? `${p.group} › ${p.name} (${p.count} items)` : v;
  }
}

function updateModeUI() {
  document.getElementById("modeLearnBtn").classList.toggle("active", prefs.mode === "learn");
  document.getElementById("modePracticeBtn").classList.toggle("active", prefs.mode === "practice");
  document.getElementById("modeQuizBtn").classList.toggle("active", prefs.mode === "quiz");
  document.getElementById("blurToggleBtn").style.display = prefs.mode === "learn" ? "" : "none";
  document.getElementById("blurToggleBtn").classList.toggle("active-toggle", prefs.blur);
  document.getElementById("blurToggleBtn").textContent = prefs.blur ? "👁️ Show Answers" : "👁️ Hide Answers";
  document.getElementById("quizBanner").classList.toggle("visible", prefs.mode === "quiz");
}

function setMode(mode) {
  prefs.mode = mode;
  currentPage = 1;
  savePrefs();
  updateModeUI();
  if (mode === "quiz") {
    startQuickQuiz();
  } else {
    render();
  }
}

function toggleBlur() {
  prefs.blur = !prefs.blur;
  savePrefs();
  updateModeUI();
  render();
}

function updateThemeBtn() {
  document.getElementById("themeBtn").textContent = prefs.dark ? "☀️ White" : "🌙 Dark";
}

function toggleTheme() {
  prefs.dark = !prefs.dark;
  document.body.classList.toggle("dark", prefs.dark);
  savePrefs();
  updateThemeBtn();
}

function startQuickQuiz() {
  const prevMode = prefs.mode;
  prefs.mode = "quiz";
  // Pull from current view + filters
  const cat = document.getElementById("catSelect").value;
  const q = document.getElementById("searchBox").value.trim().toLowerCase();
  const hideDup = document.getElementById("hideDupChk").checked;
  const factOnly = document.getElementById("factOnlyChk").checked;

  let pool = getBaseScopedItems();
  if (cat !== "ALL") pool = pool.filter(it => it.cat === cat);
  if (hideDup) pool = pool.filter(it => !it.isDupCopy);
  if (factOnly) pool = pool.filter(it => it.factUpdated);
  if (q) {
    pool = pool.filter(it => it.q.toLowerCase().includes(q) || it.cat.toLowerCase().includes(q));
  }

  const size = parseInt(document.getElementById("quizSizeSelect").value, 10) || 50;
  const shuffled = [...pool];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  quizIds = shuffled.slice(0, size).map(it => it.uid);
  quizSessionAnswers = {};
  currentPage = 1;
  updateModeUI();
  render();
}

function onSearchInput() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    currentPage = 1;
    render();
  }, 150);
}

function onFilterChange() {
  currentPage = 1;
  if (prefs.mode === "quiz") startQuickQuiz();
  else render();
}

function renderPagination(elId, totalItems, totalPages) {
  const el = document.getElementById(elId);
  if (totalItems === 0) {
    el.innerHTML = "";
    return;
  }
  const start = (currentPage - 1) * prefs.pageSize + 1;
  const end = Math.min(currentPage * prefs.pageSize, totalItems);
  el.innerHTML = `
    <div>Showing <strong>${start}–${end}</strong> of <strong>${totalItems}</strong> items</div>
    <div class="page-btns">
      <select onchange="changePageSize(this.value)" title="Items per page">
        <option value="25" ${prefs.pageSize === 25 ? "selected" : ""}>25 / page</option>
        <option value="50" ${prefs.pageSize === 50 ? "selected" : ""}>50 / page</option>
        <option value="100" ${prefs.pageSize === 100 ? "selected" : ""}>100 / page</option>
        <option value="500" ${prefs.pageSize === 500 ? "selected" : ""}>500 / page</option>
      </select>
      <button class="icon-btn" ${currentPage <= 1 ? "disabled" : ""} onclick="goPage(${currentPage - 1})">◀ Prev</button>
      <span>Page <strong>${currentPage}</strong> / ${totalPages}</span>
      <button class="icon-btn" ${currentPage >= totalPages ? "disabled" : ""} onclick="goPage(${currentPage + 1})">Next ▶</button>
    </div>
  `;
}

function changePageSize(val) {
  prefs.pageSize = parseInt(val, 10) || 50;
  currentPage = 1;
  savePrefs();
  render();
}

function goPage(p) {
  currentPage = p;
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderStats(list) {
  const ansSource = prefs.mode === "quiz" ? quizSessionAnswers : state.answers;
  let attempted = 0, correct = 0, wrong = 0;
  list.forEach(it => {
    const rec = ansSource[it.uid];
    if (rec) {
      attempted++;
      if (rec.correct) correct++;
      else wrong++;
    }
  });
  const acc = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;
  document.getElementById("statsPills").innerHTML = `
    <span class="stat-pill">Items: ${list.length}</span>
    <span class="stat-pill">Attempted: ${attempted}/${list.length}</span>
    <span class="stat-pill green">Correct: ${correct}</span>
    <span class="stat-pill red">Wrong: ${wrong}</span>
    <span class="stat-pill amber">Accuracy: ${acc}%</span>
  `;
}

function render() {
  updateSubtitle();
  renderSidebar();
  const list = getFilteredItems();
  renderStats(list);

  const totalPages = Math.max(1, Math.ceil(list.length / prefs.pageSize));
  if (currentPage > totalPages) currentPage = totalPages;

  renderPagination("topPagination", list.length, totalPages);
  renderPagination("bottomPagination", list.length, totalPages);

  const container = document.getElementById("cardsContainer");
  if (list.length === 0) {
    container.innerHTML = `<div class="empty-state">No study items match this filter/view. Try clearing search or switching packs.</div>`;
    return;
  }

  const startIdx = (currentPage - 1) * prefs.pageSize;
  const pageItems = list.slice(startIdx, startIdx + prefs.pageSize);
  const letters = ["A", "B", "C", "D", "E"];
  const ansSource = prefs.mode === "quiz" ? quizSessionAnswers : state.answers;

  container.innerHTML = pageItems.map(it => {
    const pack = PACK_MAP[it.pack];
    const isBookmarked = !!state.bookmarks[it.uid];
    const rec = ansSource[it.uid];

    const tagsHtml = `
      <span class="tag pack">${escapeHtml(pack ? pack.name : it.pack)}</span>
      <span class="tag">${escapeHtml(it.cat)}</span>
      ${it.type === "flashcard" ? `<span class="tag flash">Flashcard</span>` : ""}
      ${it.factUpdated ? `<span class="tag fact">Fact-Check Updated</span>` : ""}
      ${it.dupCount > 1 ? `<span class="tag dup" title="Appears across ${it.dupCount} packs">Repeated ×${it.dupCount}</span>` : ""}
      ${it.ref ? `<span class="tag">${escapeHtml(it.ref)}</span>` : ""}
    `;

    let bodyHtml = "";
    if (prefs.mode === "learn") {
      const blurCls = prefs.blur ? "blurred" : "";
      if (it.type === "mcq") {
        const ansText = it.opts[it.ans] ?? "";
        bodyHtml = `
          <div class="learn-answer ${blurCls}" onclick="this.classList.toggle('blurred')">
            <div class="learn-answer-label">Correct Answer (${letters[it.ans] || ""})</div>
            <div class="learn-answer-text">${escapeHtml(ansText)}</div>
          </div>
          <div class="learn-opts-preview ${blurCls}">
            ${it.opts.map((o, idx) => `<div class="opt-chip ${idx === it.ans ? "correct-chip" : ""}"><strong>${letters[idx]}.</strong> ${escapeHtml(o)}</div>`).join("")}
          </div>
        `;
      } else {
        bodyHtml = `
          <div class="learn-answer ${blurCls}" onclick="this.classList.toggle('blurred')">
            <div class="learn-answer-label">Verified Answer</div>
            <div class="learn-answer-text">${escapeHtml(it.a)}</div>
          </div>
        `;
      }
      if (it.p1 || it.p2) {
        bodyHtml += `
          <div class="notes-box ${it.factUpdated ? "fact-note" : ""} ${blurCls}" onclick="this.classList.toggle('blurred')">
            ${it.p1 ? `<div>${escapeHtml(it.p1)}</div>` : ""}
            ${it.p2 ? `<div>${escapeHtml(it.p2)}</div>` : ""}
          </div>
        `;
      }
    } else {
      // Practice or Quick Quiz
      if (it.type === "mcq") {
        const answered = !!rec;
        bodyHtml = `<div class="options-grid">
          ${it.opts.map((o, idx) => {
            let cls = "";
            if (answered) {
              if (idx === it.ans) cls = "correct";
              else if (idx === rec.chosen) cls = "wrong";
            }
            return `<button class="option-btn ${cls}" ${answered ? "disabled" : ""} onclick="answerMcq('${escapeHtml(it.uid)}', ${idx})">
              <span class="opt-letter">${letters[idx]}</span>
              <span>${escapeHtml(o)}</span>
            </button>`;
          }).join("")}
        </div>`;

        if (answered) {
          bodyHtml += `<div class="practice-feedback">
            <div class="learn-answer">
              <div class="learn-answer-label">${rec.correct ? "✅ Correct!" : "❌ Incorrect — Correct Answer: " + letters[it.ans]}</div>
              <div class="learn-answer-text">${escapeHtml(it.opts[it.ans])}</div>
            </div>
            ${(it.p1 || it.p2) ? `<div class="notes-box ${it.factUpdated ? "fact-note" : ""}">
              ${it.p1 ? `<div>${escapeHtml(it.p1)}</div>` : ""}
              ${it.p2 ? `<div>${escapeHtml(it.p2)}</div>` : ""}
            </div>` : ""}
          </div>`;
        }
      } else {
        // Flashcard in Practice / Quiz mode
        const answered = !!rec;
        const revealed = answered || rec === "REVEALED";
        bodyHtml = `<div class="flash-practice-box" id="flash-${escapeHtml(it.uid)}">
          ${!answered ? `<div class="flash-grade-row">
            <button class="primary-btn" onclick="revealFlash('${escapeHtml(it.uid)}')">Reveal Answer</button>
          </div>` : ""}
          <div class="learn-answer" id="flash-ans-${escapeHtml(it.uid)}" style="display:${answered ? "block" : "none"}">
            <div class="learn-answer-label">${answered ? (rec.correct ? "✅ Marked Known" : "❌ Marked Missed") : "Answer"}</div>
            <div class="learn-answer-text">${escapeHtml(it.a)}</div>
          </div>
          <div class="flash-grade-row" id="flash-grade-${escapeHtml(it.uid)}" style="display:none">
            <button class="icon-btn" style="border-color:var(--green-border);color:var(--green-text)" onclick="gradeFlash('${escapeHtml(it.uid)}', true)">✅ I knew this</button>
            <button class="icon-btn" style="border-color:var(--red-border);color:var(--red-text)" onclick="gradeFlash('${escapeHtml(it.uid)}', false)">❌ Review again</button>
          </div>
        </div>`;
      }
    }

    return `
      <article class="q-card ${it.factUpdated ? "fact-updated" : ""}">
        <div class="q-top">
          <div class="q-tags">${tagsHtml}</div>
          <button class="bookmark-btn ${isBookmarked ? "saved" : ""}" onclick="toggleBookmark('${escapeHtml(it.uid)}')">
            ${isBookmarked ? "⭐ Saved" : "☆ Save"}
          </button>
        </div>
        <div class="q-text">#${it.num}. ${escapeHtml(it.q)}</div>
        ${bodyHtml}
      </article>
    `;
  }).join("");
}

function answerMcq(uid, chosenIdx) {
  const item = ITEMS.find(i => i.uid === uid);
  if (!item) return;
  const record = { chosen: chosenIdx, correct: chosenIdx === item.ans };
  if (prefs.mode === "quiz") {
    quizSessionAnswers[uid] = record;
  }
  state.answers[uid] = record;
  saveState();
  render();
}

function revealFlash(uid) {
  const ans = document.getElementById("flash-ans-" + uid);
  const grade = document.getElementById("flash-grade-" + uid);
  if (ans) ans.style.display = "block";
  if (grade) grade.style.display = "flex";
}

function gradeFlash(uid, isCorrect) {
  const record = { chosen: isCorrect ? "known" : "missed", correct: isCorrect };
  if (prefs.mode === "quiz") {
    quizSessionAnswers[uid] = record;
  }
  state.answers[uid] = record;
  saveState();
  render();
}

function toggleBookmark(uid) {
  if (state.bookmarks[uid]) delete state.bookmarks[uid];
  else state.bookmarks[uid] = true;
  saveState();
  render();
}

function resetCurrentScope() {
  const list = getFilteredItems();
  if (!confirm(`Reset saved practice answers for the ${list.length} items in this view?`)) return;
  list.forEach(it => {
    delete state.answers[it.uid];
    delete quizSessionAnswers[it.uid];
  });
  saveState();
  render();
}

function exportProgress() {
  const payload = { exportedAt: new Date().toISOString(), state, prefs };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "study_hub_progress_backup.json";
  a.click();
  URL.revokeObjectURL(a.href);
}

function importProgress(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      if (data.state) {
        state.answers = data.state.answers || {};
        state.bookmarks = data.state.bookmarks || {};
        saveState();
      }
      render();
      alert("Progress restored successfully.");
    } catch (err) {
      alert("Invalid backup JSON file.");
    }
  };
  reader.readAsText(file);
  event.target.value = "";
}

document.getElementById("sidebarToggleBtn").addEventListener("click", () => {
  document.getElementById("appShell").classList.toggle("sidebar-collapsed");
});

document.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
    e.preventDefault();
    document.getElementById("searchBox").focus();
  }
});

loadState();
rebuildCategoryDropdown();
render();
</script>
</body>
</html>
"""


def main() -> None:
    packs_meta, all_items = build_dataset()
    packs_json = json.dumps(packs_meta, ensure_ascii=False).replace("</", "<\\/")
    items_json = json.dumps(all_items, ensure_ascii=False).replace("</", "<\\/")

    html = HTML_TEMPLATE.replace("__PACKS_JSON__", packs_json).replace(
        "__ITEMS_JSON__", items_json
    )
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    PAGES_INDEX_FILE.write_text(html, encoding="utf-8")

    dup_copies = sum(1 for it in all_items if it["isDupCopy"])
    fact_count = sum(1 for it in all_items if it["factUpdated"])
    print(f"Built {OUTPUT_FILE.name} & {PAGES_INDEX_FILE.name}")
    print(f"  Packs: {len(packs_meta)}")
    print(f"  Total items: {len(all_items)}")
    print(f"  Unique questions: {len(all_items) - dup_copies} (cross-pack duplicate copies: {dup_copies})")
    print(f"  Fact-check updated items: {fact_count}")
    print(f"  Output size: {OUTPUT_FILE.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
