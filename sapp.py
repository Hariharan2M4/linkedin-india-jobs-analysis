import streamlit as st
import pandas as pd

# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(
    page_title="LinkedIn Job Recommender",
    page_icon="💼",
    layout="wide"
)

# ── LOAD REAL DATA ────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("linkedin_cleaned.csv")
    df = df.rename(columns={
        "job_title":             "title",
        "level_clean":           "level",
        "job_category":          "cat",
        "employment_type_clean": "emp"
    })
    df = df[["title", "company", "city", "level", "cat", "emp"]].dropna()
    return df

df_jobs = load_data()

# ── SKILL GROUPS ──────────────────────────────
GROUPS = {
    "Programming & Query Languages": [
        "Python", "SQL", "R", "Java", "Scala", "MATLAB"
    ],
    "Data & BI Tools": [
        "Power BI", "Tableau", "Excel", "Pandas",
        "NumPy", "Matplotlib", "Seaborn", "Looker"
    ],
    "ML / AI / Statistics": [
        "Machine Learning", "Deep Learning", "Statistics",
        "NLP", "Computer Vision", "Scikit-learn",
        "TensorFlow", "PyTorch", "XGBoost"
    ],
    "Cloud & Big Data": [
        "PySpark", "Azure", "AWS", "GCP",
        "Databricks", "Hadoop", "Kafka", "Airflow"
    ],
}

# ── ROLE → SKILLS MAPPING ─────────────────────
ROLE_SKILLS = {
    "Data Analyst": {
        "must": ["SQL", "Python", "Excel"],
        "good": ["Power BI", "Tableau", "Pandas", "Statistics", "R"]
    },
    "Data Scientist": {
        "must": ["Python", "Machine Learning"],
        "good": ["SQL", "Statistics", "Deep Learning", "NLP",
                 "Scikit-learn", "TensorFlow", "Pandas"]
    },
    "Business Analyst": {
        "must": ["SQL", "Excel"],
        "good": ["Power BI", "Tableau", "Statistics", "R", "Python"]
    },
    "ML Engineer": {
        "must": ["Python", "Machine Learning"],
        "good": ["Deep Learning", "TensorFlow", "NLP",
                 "PySpark", "AWS", "Azure", "Scikit-learn"]
    },
    "Data Engineer": {
        "must": ["Python", "SQL"],
        "good": ["PySpark", "Azure", "AWS", "Databricks",
                 "Airflow", "Scala", "Kafka"]
    },
    "Product Analyst/Manager": {
        "must": ["SQL", "Excel"],
        "good": ["Tableau", "Power BI", "Statistics", "Python", "Looker"]
    },
}

# ── HEADER ────────────────────────────────────
st.title("💼 LinkedIn India — Skill-Based Job Recommender")
st.caption(f"Based on {len(df_jobs)} real LinkedIn India job postings")
st.markdown("---")

# ── SIDEBAR — SKILL SELECTION ─────────────────
st.sidebar.header("🛠️ Select Your Skills")
st.sidebar.caption("Pick everything you know")

selected_skills = []
for group_name, skills in GROUPS.items():
    st.sidebar.markdown(f"**{group_name}**")
    for skill in skills:
        if st.sidebar.checkbox(skill, key=skill):
            selected_skills.append(skill)
    st.sidebar.markdown("")

st.sidebar.markdown("---")
st.sidebar.markdown(f"✅ **{len(selected_skills)} skills selected**")

# ── FILTERS ───────────────────────────────────
st.subheader("🔍 Filters")
col1, col2, col3 = st.columns(3)

with col1:
    city_options = ["All"] + sorted(df_jobs["city"].dropna().unique().tolist())
    city_filter = st.selectbox("City", city_options)

with col2:
    level_options = ["All"] + sorted(df_jobs["level"].dropna().unique().tolist())
    level_filter = st.selectbox("Level", level_options)

with col3:
    emp_options = ["All"] + sorted(df_jobs["emp"].dropna().unique().tolist())
    emp_filter = st.selectbox("Employment Type", emp_options)

st.markdown("---")

# ── FIND JOBS BUTTON ──────────────────────────
if st.button("▶  Find My Jobs", type="primary", use_container_width=True):

    if len(selected_skills) == 0:
        st.warning("⚠️ Please select at least one skill from the sidebar!")

    else:
        selected_set = set(selected_skills)

        # ── SCORE EACH ROLE ───────────────────
        role_scores = []
        for role, mapping in ROLE_SKILLS.items():
            must = mapping["must"]
            good = mapping["good"]

            must_matched = [s for s in must if s in selected_set]
            good_matched = [s for s in good if s in selected_set]
            must_missing = [s for s in must if s not in selected_set]

            # Skip role if no must-have skill matched
            if len(must_matched) == 0:
                continue

            must_score  = len(must_matched) / len(must)
            good_score  = len(good_matched) / len(good) if good else 0
            total_score = must_score * 0.65 + good_score * 0.35

            role_scores.append({
                "role":         role,
                "score":        round(total_score * 100),
                "must_matched": must_matched,
                "good_matched": good_matched,
                "must_missing": must_missing,
            })

        role_scores = sorted(role_scores, key=lambda x: x["score"], reverse=True)

        # ── NO MATCH ──────────────────────────
        if not role_scores:
            st.error("❌ No roles matched. Try adding core skills like Python, SQL, or Excel.")

        else:
            # ── ROLE CARDS ────────────────────
            st.subheader("🎯 Best Matching Roles")

            cols = st.columns(min(len(role_scores), 3))
            for i, r in enumerate(role_scores):
                with cols[i % 3]:
                    total_jobs = df_jobs[df_jobs["cat"] == r["role"]].shape[0]
                    st.metric(label=r["role"], value=f"{r['score']}% fit")
                    st.progress(r["score"] / 100)
                    st.caption(f"✅ Core matched : {', '.join(r['must_matched']) if r['must_matched'] else 'None'}")
                    if r["good_matched"]:
                        st.caption(f"➕ Bonus skills : {', '.join(r['good_matched'])}")
                    if r["must_missing"]:
                        st.caption(f"❌ Missing core : {', '.join(r['must_missing'])}")
                    st.caption(f"📋 {total_jobs} openings in dataset")
                    st.markdown("")

            # ── JOB LISTINGS ──────────────────
            st.markdown("---")
            st.subheader("📋 Matching Job Listings")

            matched_roles = set(r["role"] for r in role_scores)
            filtered = df_jobs[df_jobs["cat"].isin(matched_roles)].copy()

            # Apply filters
            if city_filter  != "All":
                filtered = filtered[filtered["city"]  == city_filter]
            if level_filter != "All":
                filtered = filtered[filtered["level"] == level_filter]
            if emp_filter   != "All":
                filtered = filtered[filtered["emp"]   == emp_filter]

            st.markdown(f"**{len(filtered)} jobs found**")

            if filtered.empty:
                st.info("No jobs match the current filters. Try changing City or Level.")
            else:
                for _, row in filtered.iterrows():
                    with st.expander(f"**{row['title']}**  —  {row['company']}"):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.markdown(f"📍 **City**\n\n{row['city']}")
                        c2.markdown(f"🏷️ **Level**\n\n{row['level']}")
                        c3.markdown(f"💼 **Role**\n\n{row['cat']}")
                        c4.markdown(f"🕐 **Type**\n\n{row['emp']}")

# ── DEFAULT STATE ─────────────────────────────
elif len(selected_skills) > 0:
    st.info(f"✅ {len(selected_skills)} skills selected — click **Find My Jobs** to see results!")
else:
    st.info("👈 Select your skills from the sidebar, then click **Find My Jobs**")
