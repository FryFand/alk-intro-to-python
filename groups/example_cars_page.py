"""Example - What should this car cost?

The EXAMPLE page of the class website, built in class (Part 4). Every group page follows the same plan:
1 What we built  ·  2 Our answer + the proof  ·  Try it yourself  ·  3 Is our number real?
"""
import pandas as pd
import streamlit as st
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from ml_base import DATA

FEATURES = ["horsepower", "engine-size", "curb-weight"]


@st.cache_data                     # load + clean only once, not on every click
def load_cars():
    cars = pd.read_csv(DATA / "cars.csv")
    for col in ["horsepower", "price"]:
        cars[col] = pd.to_numeric(cars[col], errors="coerce")      # "?" -> NaN (not 0!)
    return cars.dropna(subset=FEATURES + ["price"])


cars = load_cars()
train, test = train_test_split(cars, test_size=0.25, random_state=0)
model = LinearRegression().fit(train[FEATURES], train["price"])
baseline = DummyRegressor().fit(train[FEATURES], train["price"])       # always predicts the mean price
mae = (test["price"] - model.predict(test[FEATURES])).abs().mean()
mae_baseline = (test["price"] - baseline.predict(test[FEATURES])).abs().mean()

st.title("🚗 What should this car cost?")
st.caption("Example page · built live in class · Team: the instructor")

st.header("1️⃣ What we built")
st.markdown(
    f"""
A **linear regression** that predicts the price of a car (USD, 1985) from
`{FEATURES[0]}`, `{FEATURES[1]}` and `{FEATURES[2]}`.
Trained on {len(train)} cars, tested on {len(test)} cars it had **never seen**.
"""
)

st.header("2️⃣ Our answer")
col1, col2, col3 = st.columns(3)
col1.metric("Typical error (MAE)", f"${mae:,.0f}")
col2.metric("Baseline: always the mean price", f"${mae_baseline:,.0f}")
col3.metric("Improvement", f"{1 - mae / mae_baseline:.0%}")      # :.0% = as a percentage, no decimals
st.write("Each extra unit adds this many dollars (the coefficients):")
st.dataframe(pd.Series(model.coef_, index=FEATURES, name="USD per unit").round(1))

st.header("🎛️ Try it yourself")
hp = st.slider("Horsepower", 50, 260, 100)
size = st.slider("Engine size (cubic inches)", 60, 330, 120)
weight = st.slider("Curb weight (lbs)", 1500, 4100, 2400)
car = pd.DataFrame([[hp, size, weight]], columns=FEATURES)        # one row, the SAME columns as in training
st.metric("Predicted price", f"${model.predict(car)[0]:,.0f}")
st.scatter_chart(cars, x="horsepower", y="price", color="engine-size")

st.header("3️⃣ Is our number real?")
st.markdown(
    """
- Only **199 cars**, all from **1985** - this is not a price list for today.
- Horsepower, engine size and weight go together (big cars have big engines), so a single
  coefficient is **not** "the effect of one more horsepower" - try a tiny engine with 250 HP: the model still answers.
- **What the AI got wrong:** Copilot replaced `"?"` with `0`, so two cars had **0 horsepower**. Fixed with `pd.to_numeric(errors="coerce")`.
"""
)
