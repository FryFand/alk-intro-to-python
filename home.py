"""Home"""
from pathlib import Path

import streamlit as st

# ----- the instructor fills these in once, after creating the repository -----
REPO_URL = "https://github.com/kciech/alk-intro-to-python"       # <- the GitHub repository of this site
COURSE = "Introduction to Python and Machine Learning · ALK · 2026/27"

GROUPS = Path(__file__).resolve().parent / "groups"

st.title("🐍 Our class website")
st.caption(COURSE)

st.markdown(
    """
**Every page on this site was written in Python by the students of this course.**
No HTML, no JavaScript - each page is one `.py` file that uses the **Streamlit** library.

### 🛒 The project of classes 7+8: *machine learning for our online gift shop*
The board of our shop (the Online Retail data, Dec 2010 - Dec 2011, plus the London weather) asked six questions.
Each group answered one of them with a statistical test or a machine-learning model **and** built a page here,
where you can try the model yourself.

| Card | The board's question | Method |
|---|---|---|
| 1 | Can we forecast tomorrow's sales - and does the weather help? | linear regression |
| 2 | Is the "rainy days sell more" effect real? | shuffle test, t-test |
| 3 | Which customers will come back? | logistic regression |
| 4 | What kinds of customers do we have? | k-means clustering |
| 5 | Do cheaper products sell more? | log-log regression |
| 6 | A consultant's model has a tiny error. Should we buy it? | overfitting, cross-validation |

👈 **Pick a group in the menu on the left** (on a phone: the `>` at the top left).
"""
)

col1, col2 = st.columns(2)
for col, cls in zip((col1, col2), ("w01", "w03")):
    pages = sorted(GROUPS.glob(f"{cls}_group*_page.py"))
    col.metric(f"Class {cls}", f"{len(pages)} group pages")

st.divider()
with st.expander("🛠️ How is this website built? (for the students)"):
    st.markdown(
        f"""
- The code lives in a **GitHub repository**: [{REPO_URL}]({REPO_URL}).
- **Streamlit Community Cloud** (free) runs `app.py` from that repository. Every change on GitHub
  appears here after about a minute.
- `app.py` builds the menu: every file `groups/w01_groupN_page.py` / `groups/w03_groupN_page.py` becomes a page.
- Each group adds **two files** to the folder `groups/`: its module (the class) and its page.
  On GitHub: open the folder `groups/` → **Add file → Create new file** → paste → **Propose changes** →
  **Create pull request**. The instructor merges it - and the page is online.
- The data (`data/`) and the helper module `ml_base.py` are shared by all pages.
- 🔒 This website is **public**: first names only, no surnames, no e-mail addresses.
"""
    )
