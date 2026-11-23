# 🐍 Class website - Introduction to Python and Machine Learning (ALK)

Every page of this website is a Python file written by the students of the course, using [Streamlit](https://docs.streamlit.io).

| File / folder | What it is |
|---|---|
| `app.py` | the menu - finds every `groups/w01_groupN_page.py` and `groups/w03_groupN_page.py` by itself |
| `home.py` | the Home page |
| `ml_base.py` | data loaders + the `Analysis` parent class, shared by all pages |
| `data/` | the data sets (Online Retail summaries + London weather, cars, Titanic) |
| `groups/` | **one module + one page per group** |
| `requirements.txt` | the libraries the server installs |

**Run it on your laptop:** `pip install -r requirements.txt`, then `streamlit run app.py`.

**Add your group's page:** open the folder `groups/` → *Add file → Create new file* → name it `w01_groupN_<module>.py`
(or `..._page.py`) → paste your code → *Propose changes* → *Create pull request*. After the merge the page is online in about a minute.

🔒 The site is public: first names only.

*Data:* Online Retail - Chen, D. (2015), UCI Machine Learning Repository; weather - Open-Meteo historical archive;
Automobile - Schlimmer, J. (1987), UCI Machine Learning Repository; Titanic - via the seaborn example data sets.
