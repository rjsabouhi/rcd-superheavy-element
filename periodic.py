import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app config
st.set_page_config(page_title="Elemental Genesis", layout="wide")
st.title("🧬 Elemental Genesis: RCD-Based Superheavy Element Explorer")

st.markdown("""
Welcome to the **Elemental Genesis Simulator**. This tool uses symbolic coherence modeling 
based on Recursive Cognitive Dynamics (RCD) to explore the hidden territories of the periodic table.

Each point in this 3D space represents a potential superheavy element configuration (Z = protons, N = neutrons), 
and the **γ(t)** score reflects its predicted symbolic stability.
""")

# Define symbolic stability score
def symbolic_stability_score(Z, N):
    shell_closure_bonus = int(Z in [2, 8, 20, 28, 50, 82, 114]) + int(N in [2, 8, 20, 28, 50, 82, 126, 184])
    memory_tension = np.exp(-abs(Z - N) / 10)
    clinging_resistance = 1 / (1 + np.exp((Z + N - 250) / 10))
    entropy_gradient = np.tanh((Z - 100) / 20)
    symbolic_coherence = (shell_closure_bonus + memory_tension + clinging_resistance - entropy_gradient) / 3
    return symbolic_coherence

# Sidebar range selectors
st.sidebar.header("Simulation Range Controls")
Z_min = st.sidebar.slider("Minimum Proton Number (Z)", 110, 125, 110)
Z_max = st.sidebar.slider("Maximum Proton Number (Z)", Z_min + 1, 130, 130)
N_min = st.sidebar.slider("Minimum Neutron Number (N)", 150, 190, 150)
N_max = st.sidebar.slider("Maximum Neutron Number (N)", N_min + 1, 200, 200)

# Generate data
data = []
for Z in range(Z_min, Z_max + 1):
    for N in range(N_min, N_max + 1):
        gamma = symbolic_stability_score(Z, N)
        data.append({'Z': Z, 'N': N, 'γ(t)': gamma})

df = pd.DataFrame(data)

# 3D plot
fig = px.scatter_3d(df, x='Z', y='N', z='γ(t)', color='γ(t)',
                    color_continuous_scale='Viridis', opacity=0.8,
                    labels={'Z': 'Proton Number (Z)', 'N': 'Neutron Number (N)', 'γ(t)': 'Stability γ(t)'},
                    title="Symbolic Stability Landscape of Superheavy Elements")

st.plotly_chart(fig, use_container_width=True)

# Top predictions
st.subheader("🌟 Top Predicted Stable Configurations")
top_elements = df.sort_values('γ(t)', ascending=False).head(5)
st.dataframe(top_elements, use_container_width=True)
