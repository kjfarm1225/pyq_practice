import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

def sample():
    rng = np.random.default_rng()
    return pd.DataFrame(rng.integers(0, 10, (6, 3)),
           columns=["A", "B", "C"])

df = sample()
fig, ax = plt.subplots()
df.plot(kind="line", ax=ax)
st.pyplot(fig)