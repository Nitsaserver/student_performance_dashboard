import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main{
    background-color:#f5f7fa;
}
h1{
    color:#003366;
}
.sidebar .sidebar-content{
    background:#dceefb;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("🎓 Student Performance Analytics Dashboard")

st.write("""
This dashboard analyzes student performance using interactive filters and visualizations.
""")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data.csv")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

semester = st.sidebar.multiselect(
    "Semester",
    options=sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)

attendance = st.sidebar.slider(
    "Attendance",
    int(df["Attendance"].min()),
    int(df["Attendance"].max()),
    (
        int(df["Attendance"].min()),
        int(df["Attendance"].max())
    )
)

# -----------------------------
# Filter Data
# -----------------------------
filtered = df[
    (df["Department"].isin(department)) &
    (df["Semester"].isin(semester)) &
    (df["Attendance"]>=attendance[0]) &
    (df["Attendance"]<=attendance[1])
]

# -----------------------------
# Display Data
# -----------------------------
st.subheader("Filtered Student Data")

st.dataframe(filtered)

# -----------------------------
# Summary Statistics
# -----------------------------
st.subheader("Summary Statistics")

st.write(filtered.describe())

# -----------------------------
# Average Marks by Department
# -----------------------------
st.subheader("Average Marks by Department")

avg_marks = filtered.groupby("Department")["Marks"].mean()

fig, ax = plt.subplots()

ax.bar(avg_marks.index, avg_marks.values)

ax.set_xlabel("Department")
ax.set_ylabel("Average Marks")

st.pyplot(fig)

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("Semester Distribution")

semester_count = filtered["Semester"].value_counts()

fig2, ax2 = plt.subplots()

ax2.pie(
    semester_count,
    labels=semester_count.index,
    autopct="%1.1f%%"
)

st.pyplot(fig2)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("Marks Distribution")

fig3, ax3 = plt.subplots()

ax3.hist(filtered["Marks"], bins=10)

ax3.set_xlabel("Marks")
ax3.set_ylabel("Students")

st.pyplot(fig3)

# -----------------------------
# Scatter Plot
# -----------------------------
st.subheader("Attendance vs Marks")

fig4, ax4 = plt.subplots()

ax4.scatter(
    filtered["Attendance"],
    filtered["Marks"]
)

ax4.set_xlabel("Attendance")

ax4.set_ylabel("Marks")

st.pyplot(fig4)

# -----------------------------
# Download CSV
# -----------------------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_students.csv",
    mime="text/csv"
)