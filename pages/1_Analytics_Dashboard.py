import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics Dashboard")

st.title("📊 Mental Health Analytics Dashboard")
st.write("Visual insights from survey responses.")

import os

file_path = "mental_health_responses.csv"

if not os.path.exists(file_path):
    st.warning("No submitted responses yet.")
    st.stop()

df = pd.read_csv(file_path)

# Convert numeric columns safely
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Stress Score"] = pd.to_numeric(df["Stress Score"], errors="coerce")

# Remove invalid rows
df = df.dropna()

if df.empty:
    st.warning("No valid submitted responses yet.")
    st.stop()

# Show raw data
st.subheader("📄 Survey Data")
st.dataframe(df)

st.write("---")

# ----------------------------
# AGE DISTRIBUTION PLOT
# ----------------------------
st.subheader("👥 Age Distribution")

fig, ax = plt.subplots()
ax.hist(df["Age"])
ax.set_xlabel("Age")
ax.set_ylabel("Count")
st.pyplot(fig)

st.write("---")

# ----------------------------
# STRESS SCORE DISTRIBUTION
# ----------------------------
st.subheader("🧠 Stress Score Distribution")

fig2, ax2 = plt.subplots()
ax2.hist(df["Stress Score"])
ax2.set_xlabel("Stress Score")
ax2.set_ylabel("Number of Participants")
st.pyplot(fig2)

st.write("---")

# ----------------------------
# GENDER BREAKDOWN
# ----------------------------
st.subheader("🚻 Gender Breakdown")

gender_counts = df["Gender"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%")
st.pyplot(fig3)

st.write("---")

# ----------------------------
# STRESS LEVEL BAR CHART
# ----------------------------
st.subheader("📉 Stress Levels")

level_counts = df["Stress Level"].value_counts()

fig4, ax4 = plt.subplots()
ax4.bar(level_counts.index, level_counts.values)
ax4.set_xlabel("Stress Category")
ax4.set_ylabel("Count")
plt.xticks(rotation=30)
st.pyplot(fig4)
