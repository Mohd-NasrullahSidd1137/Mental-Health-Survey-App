import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Mental Health in Tech | Analytics Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Header */
    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        color: #f9fafb;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    /* Section title */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #f3f4f6;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* KPI cards */
    .metric-card {
        background: linear-gradient(145deg, #111827, #172033);
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 22px;
        min-height: 130px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    }

    .metric-label {
        color: #9ca3af;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f9fafb;
        font-size: 30px;
        font-weight: 800;
    }

    .metric-description {
        color: #6b7280;
        font-size: 12px;
        margin-top: 5px;
    }

    /* Insight cards */
    .insight-card {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-weight: 700;
        color: #f9fafb;
        font-size: 15px;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #9ca3af;
        font-size: 13px;
        line-height: 1.6;
    }

    /* Sidebar branding */
    .sidebar-brand {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .sidebar-brand-icon {
        font-size: 42px;
    }

    .sidebar-brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #f9fafb;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #9ca3af;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        padding-top: 35px;
        border-top: 1px solid #1f2937;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    data = pd.read_csv("survey.csv")

    # Timestamp
    data["Timestamp"] = pd.to_datetime(
        data["Timestamp"],
        errors="coerce"
    )

    # Age cleaning
    data.loc[
        (data["Age"] < 18) | (data["Age"] > 100),
        "Age"
    ] = np.nan

    data["Age"] = data["Age"].fillna(data["Age"].median())

    # Gender cleaning
    def clean_gender(gender):

        gender = str(gender).strip().lower()

        if gender in [
            "m", "male", "man", "make", "mal", "maile", "mail",
            "male-ish", "male (cis)", "cis male", "cis man",
            "msle", "malr", "guy (-ish) ^_^",
            "male leaning androgynous",
            "something kinda male?",
            "ostensibly male, unsure what that really means"
        ]:
            return "Male"

        elif gender in [
            "f", "female", "woman", "femake", "femail",
            "cis female", "female (cis)", "cis-female/femme"
        ]:
            return "Female"

        elif gender in [
            "trans-female",
            "trans woman",
            "female (trans)"
        ]:
            return "Female"

        else:
            return "Other"

    data["Gender"] = data["Gender"].apply(clean_gender)

    # Missing categorical values
    data["self_employed"] = data["self_employed"].fillna("Unknown")
    data["state"] = data["state"].fillna("Unknown")
    data["work_interfere"] = data["work_interfere"].fillna("Unknown")

    return data


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🧠</div>
        <div class="sidebar-brand-title">Mental Health Analytics</div>
        <div class="sidebar-brand-subtitle">
            Technology Workplace Survey
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🎛️ Dashboard Filters")

    selected_gender = st.multiselect(
        "Gender",
        options=sorted(df["Gender"].unique()),
        default=sorted(df["Gender"].unique())
    )

    selected_country = st.multiselect(
        "Country",
        options=sorted(df["Country"].unique()),
        default=[]
    )

    selected_treatment = st.multiselect(
        "Treatment",
        options=sorted(df["treatment"].unique()),
        default=sorted(df["treatment"].unique())
    )

    selected_remote = st.multiselect(
        "Remote Work",
        options=sorted(df["remote_work"].unique()),
        default=sorted(df["remote_work"].unique())
    )

    st.markdown("---")

    st.markdown("### 📌 About")

    st.caption(
        "This interactive dashboard explores mental health "
        "experiences and workplace attitudes in the technology sector."
    )

    st.caption(
        "Dataset: Mental Health in Tech Survey"
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    df["Gender"].isin(selected_gender)
    & df["treatment"].isin(selected_treatment)
    & df["remote_work"].isin(selected_remote)
].copy()


if selected_country:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_country)
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">🧠 Mental Health in Tech</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive analytics dashboard exploring mental health, '
    'treatment-seeking behavior, and workplace support.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_respondents = len(filtered_df)

if total_respondents > 0:

    treatment_rate = (
        filtered_df["treatment"].eq("Yes").mean() * 100
    )

    family_history_rate = (
        filtered_df["family_history"].eq("Yes").mean() * 100
    )

    remote_rate = (
        filtered_df["remote_work"].eq("Yes").mean() * 100
    )

else:

    treatment_rate = 0
    family_history_rate = 0
    remote_rate = 0


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Key metrics based on the currently selected filters.'
    '</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL RESPONDENTS</div>
        <div class="metric-value">{total_respondents:,}</div>
        <div class="metric-description">Filtered survey responses</div>
    </div>
    """, unsafe_allow_html=True)


with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TREATMENT SOUGHT</div>
        <div class="metric-value">{treatment_rate:.1f}%</div>
        <div class="metric-description">Respondents who sought treatment</div>
    </div>
    """, unsafe_allow_html=True)


with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">FAMILY HISTORY</div>
        <div class="metric-value">{family_history_rate:.1f}%</div>
        <div class="metric-description">Reported family history</div>
    </div>
    """, unsafe_allow_html=True)


with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">REMOTE WORK</div>
        <div class="metric-value">{remote_rate:.1f}%</div>
        <div class="metric-description">Respondents working remotely</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please adjust the filters."
    )

    st.stop()


# =========================================================
# SECTION 1 — TREATMENT ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Mental Health & Treatment Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore treatment-seeking patterns across demographic and workplace factors.'
    '</div>',
    unsafe_allow_html=True
)


c1, c2 = st.columns(2)


with c1:

    treatment_counts = (
        filtered_df["treatment"]
        .value_counts()
        .reset_index()
    )

    treatment_counts.columns = ["Treatment", "Count"]

    fig = px.bar(
        treatment_counts,
        x="Treatment",
        y="Count",
        text="Count",
        title="Mental Health Treatment Distribution",
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with c2:

    gender_treatment = (
        filtered_df
        .groupby(["Gender", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        gender_treatment,
        x="Gender",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment-Seeking by Gender",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 2 — WORK INTERFERENCE
# =========================================================

c3, c4 = st.columns(2)


with c3:

    work_order = [
        "Never",
        "Rarely",
        "Sometimes",
        "Often",
        "Unknown"
    ]

    work_df = (
        filtered_df["work_interfere"]
        .value_counts()
        .reindex(work_order)
        .fillna(0)
        .reset_index()
    )

    work_df.columns = [
        "Work Interference",
        "Count"
    ]

    fig = px.bar(
        work_df,
        x="Work Interference",
        y="Count",
        title="Mental Health Interference with Work",
        text="Count",
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with c4:

    work_treatment = (
        filtered_df
        .groupby(["work_interfere", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        work_treatment,
        x="work_interfere",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Work Interference",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 3 — WORKPLACE SUPPORT
# =========================================================

st.markdown(
    '<div class="section-title">🏢 Workplace Support & Culture</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Analyze how workplace policies and support relate to mental health.'
    '</div>',
    unsafe_allow_html=True
)


c5, c6 = st.columns(2)


with c5:

    benefits_df = (
        filtered_df
        .groupby(["benefits", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        benefits_df,
        x="benefits",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Mental Health Benefits",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with c6:

    care_df = (
        filtered_df
        .groupby(["care_options", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        care_df,
        x="care_options",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Awareness of Care Options",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 4 — COMPANY & REMOTE WORK
# =========================================================

c7, c8 = st.columns(2)


with c7:

    company_df = (
        filtered_df
        .groupby(["no_employees", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    company_order = [
        "1-5",
        "6-25",
        "26-100",
        "100-500",
        "500-1000",
        "More than 1000"
    ]

    company_df["no_employees"] = pd.Categorical(
        company_df["no_employees"],
        categories=company_order,
        ordered=True
    )

    company_df = company_df.sort_values("no_employees")

    fig = px.bar(
        company_df,
        x="no_employees",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Company Size",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with c8:

    remote_df = (
        filtered_df
        .groupby(["remote_work", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        remote_df,
        x="remote_work",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Remote Work",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 5 — ANONYMITY & LEAVE
# =========================================================

c9, c10 = st.columns(2)


with c9:

    anonymity_df = (
        filtered_df
        .groupby(["anonymity", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        anonymity_df,
        x="anonymity",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Anonymity",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with c10:

    leave_df = (
        filtered_df
        .groupby(["leave", "treatment"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        leave_df,
        x="leave",
        y="Count",
        color="treatment",
        barmode="group",
        title="Treatment by Ease of Taking Mental Health Leave",
        template="plotly_dark"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 6 — GEOGRAPHIC ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">🌎 Geographic Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore respondent distribution across countries and states.'
    '</div>',
    unsafe_allow_html=True
)


geo1, geo2 = st.columns(2)


with geo1:

    country_df = (
        filtered_df["Country"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    country_df.columns = [
        "Country",
        "Respondents"
    ]

    fig = px.bar(
        country_df.sort_values("Respondents"),
        x="Respondents",
        y="Country",
        orientation="h",
        title="Top 15 Countries by Respondents",
        template="plotly_dark"
    )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with geo2:

    state_df = (
        filtered_df[
            filtered_df["state"] != "Unknown"
        ]["state"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    state_df.columns = [
        "State",
        "Respondents"
    ]

    fig = px.bar(
        state_df.sort_values("Respondents"),
        x="Respondents",
        y="State",
        orientation="h",
        title="Top 15 States by Respondents",
        template="plotly_dark"
    )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# SECTION 7 — FAMILY HISTORY
# =========================================================

st.markdown(
    '<div class="section-title">🧬 Family History Analysis</div>',
    unsafe_allow_html=True
)


family_df = (
    filtered_df
    .groupby(["family_history", "treatment"])
    .size()
    .reset_index(name="Count")
)


fig = px.bar(
    family_df,
    x="family_history",
    y="Count",
    color="treatment",
    barmode="group",
    title="Treatment by Family History of Mental Illness",
    template="plotly_dark"
)

fig.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# SECTION 8 — INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Analytical Highlights</div>',
    unsafe_allow_html=True
)

treatment_yes = (
    filtered_df["treatment"].eq("Yes").sum()
)

treatment_no = (
    filtered_df["treatment"].eq("No").sum()
)

if treatment_yes > treatment_no:
    treatment_message = (
        "Within the current filter selection, more respondents "
        "reported seeking treatment than not seeking treatment."
    )
else:
    treatment_message = (
        "Within the current filter selection, more respondents "
        "reported not seeking treatment than seeking treatment."
    )


most_common_gender = (
    filtered_df["Gender"].value_counts().idxmax()
)

most_common_work = (
    filtered_df["work_interfere"].value_counts().idxmax()
)


st.markdown(f"""
<div class="insight-card">
    <div class="insight-title">Treatment Pattern</div>
    <div class="insight-text">
        {treatment_message}
    </div>
</div>

<div class="insight-card">
    <div class="insight-title">Demographic Pattern</div>
    <div class="insight-text">
        The most represented gender category under the current filters is
        <b>{most_common_gender}</b>.
    </div>
</div>

<div class="insight-card">
    <div class="insight-title">Workplace Impact</div>
    <div class="insight-text">
        The most frequently reported work-interference category under the
        current filters is <b>{most_common_work}</b>.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DOWNLOAD DATA
# =========================================================

st.markdown(
    '<div class="section-title">📥 Export Filtered Data</div>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_mental_health_survey.csv",
    mime="text/csv"
)


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("🔎 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    Mental Health in Tech Survey Analytics Dashboard<br>
    Built with Python • Pandas • Plotly • Streamlit
</div>
""", unsafe_allow_html=True)