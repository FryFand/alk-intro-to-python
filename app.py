"""Our class website - Introduction to Python and Machine Learning (ALK).

Run it on your laptop:   streamlit run app.py      (or preview() in a notebook)
On the internet it runs on Streamlit Community Cloud, straight from the GitHub repository.

You never need to edit this file. It finds the pages by itself:
every file  groups/w01_groupN_page.py  or  groups/w03_groupN_page.py  becomes one page in the menu.
The FIRST LINE of the page's docstring is its name in the menu.
"""
import ast
import re
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
GROUPS = ROOT / "groups"
CLASSES = ["w01", "w03"]                          # one menu section per student group

# the group pages import their own modules from groups/ and ml_base.py from the main folder
for folder in (ROOT, GROUPS):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

# forget the groups' modules on every run, so a new version uploaded to GitHub is used at once
for name in list(sys.modules):
    if name.startswith(tuple(f"{c}_" for c in CLASSES)) or name.startswith("example_"):
        del sys.modules[name]


def page_title(path, fallback):
    """First line of the file's docstring - read WITHOUT running the file (a broken page can't break the menu)."""
    try:
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
    except (SyntaxError, UnicodeDecodeError):
        return f"{fallback} ⚠️ syntax error"
    return doc.strip().splitlines()[0][:60] if doc else fallback


def group_number(path):
    match = re.search(r"group(\d+)", path.stem)
    return int(match.group(1)) if match else 999


st.set_page_config(page_title="ALK · Python & ML", page_icon="🐍", layout="wide")

menu = {
    "": [st.Page("home.py", title="Home", icon="🏠", default=True)],
    "Start here": [st.Page("groups/example_cars_page.py", title="Example: car prices", icon="🚗")],
}
for cls in CLASSES:
    files = sorted(GROUPS.glob(f"{cls}_group*_page.py"), key=group_number)
    pages = [st.Page(f"groups/{f.name}", title=page_title(f, f"Group {group_number(f)}"),
                     url_path=f.stem.removesuffix("_page"))
             for f in files]
    if pages:
        menu[f"Class {cls}"] = pages

st.navigation(menu).run()
