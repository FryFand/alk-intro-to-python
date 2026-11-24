"""Group 4 - What kinds of customers do we have?"""
import matplotlib.pyplot as plt
import streamlit as st

from ml_base import load_customers
from w01_group4_segments import CustomerSegments


@st.cache_data                       # load the table only once, not on every click
def get_customers():
    return load_customers()


customers = get_customers()
model = CustomerSegments(customers, k=4, scale=True).fit()
prof = model.profile()
overall_returned = customers["returned"].mean() * 100

st.title("🧩 What kinds of customers do we have?")
st.caption("Group 4 · Card 4 · Team: Mateusz, Kacper, Władysław")

st.header("1️⃣ What we built")
st.markdown(f"""
`CustomerSegments(customers, k=4, scale=True)` - puts each of our **{len(customers):,} customers**
(who bought between Dec 2010 and Aug 2011) into one of `k` segments with **k-means**, using three numbers:
how long ago they last bought (`recency_days`), how many orders they placed (`orders`) and how much they spent (`revenue`).

`.fit()` → one segment number per customer (with `scale=True` first `log1p` + standardising, so pounds don't drown out days) ·
`.profile()` → one row per segment: size, averages and **% who came back** in Sep-Dec 2011 · `.plot()` → orders vs revenue, coloured by segment
""")

st.header("2️⃣ Our answer to the board")
best, worst = prof.iloc[0], prof.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Customers in the top segment", f"{int(best['customers']):,}",
            f"{best['customers'] / len(customers):.0%} of all customers", delta_color="off")
col2.metric("Came back: top segment", f"{best['returned_pct']:.0f}%",
            f"{best['returned_pct'] - overall_returned:+.0f} pp vs all customers")
col3.metric("Came back: biggest segment", f"{prof.loc[prof['customers'].idxmax(), 'returned_pct']:.0f}%",
            f"{prof.loc[prof['customers'].idxmax(), 'returned_pct'] - overall_returned:+.0f} pp vs all customers")
st.dataframe(prof)
st.markdown(f"""
With **k = 4** (scaled) we see four kinds of customers (sorted by revenue):
- **Champions** - few (15%) but bring **~62% of all revenue**: ~11 orders, ~£6,200 each, bought 3 weeks ago, **93%** came back.
- **Steady regulars** - ~3 orders, ~£1,200, last order ~3 months ago, 67% came back.
- **Promising newcomers** - only ~2 orders but very recent (18 days), 61% came back.
- **Sleeping one-timers** - the biggest group (~{prof['customers'].max() / len(customers):.0%}): one order ~5 months ago, ~£270, only 39% came back.

**Where to act:** keep the Champions happy (they are a large share of revenue), turn *Promising newcomers* into regulars
with a second-order offer, and try a cheap win-back for the *Sleeping one-timers* - most of them won't return by themselves.
""")

st.header("🎛️ Try it yourself")
c1, c2 = st.columns(2)
k = c1.slider("Number of segments (k)", 2, 8, 4)
scale = c2.checkbox("Scale first (log1p + standardise)", value=True)
mine = CustomerSegments(customers, k=k, scale=scale).fit()
st.dataframe(mine.profile())
fig = mine.plot().figure
st.pyplot(fig)
plt.close(fig)                       # free the memory: a new figure is drawn on every click
if not scale:
    st.info("Without scaling, revenue (up to £174,000) dominates the distance - k-means mostly splits off a "
            "handful of very big spenders and lumps almost everyone else into one segment.")

st.header("3️⃣ Is our number real? + what the AI got wrong")
st.markdown("""
- **k = 4 is our choice, not a fact.** k-means always returns exactly k segments, even if the customers don't form
  clear groups - with k = 3 or 5 the "Champions" just shrink or grow. Our segments are *useful labels*, not natural types.
- **The result depends on scaling** (tick the box off) and on the 3 columns we picked; another choice gives other segments.
- **"Came back" is not caused by the segment:** recent buyers come back more partly just because the window
  (Sep-Dec, with Christmas) starts right after their last order.
- **AI:** Claude's first answer text claimed the Champions bring "~60% of revenue" - a number it had never computed.
  We calculated it (62%) and only then kept it. Its page code also used `use_container_width=True`, which Streamlit
  warns will be removed, and never closed the chart, so every click left a figure in memory - both fixed.
""")
