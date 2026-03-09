import streamlit as st
import pandas as pd

# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(
    page_title="LinkedIn Job Recommender",
    page_icon="💼",
    layout="wide"
)

st.title("💼 LinkedIn India — Skill-Based Job Recommender")
st.caption("Based on 653 real LinkedIn India job postings")
st.markdown("---")

# ── SKILL GROUPS ──────────────────────────────
GROUPS = {
    "Programming & Query Languages": ["Python", "SQL", "R", "Java", "Scala", "MATLAB"],
    "Data & BI Tools":               ["Power BI", "Tableau", "Excel", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Looker"],
    "ML / AI / Statistics":          ["Machine Learning", "Deep Learning", "Statistics", "NLP", "Computer Vision",
                                      "Scikit-learn", "TensorFlow", "PyTorch", "XGBoost"],
    "Cloud & Big Data":              ["PySpark", "Azure", "AWS", "GCP", "Databricks", "Hadoop", "Kafka", "Airflow"],
}

# ── ROLE → SKILLS MAPPING ─────────────────────
ROLE_SKILLS = {
    "Data Analyst":           {"must": ["SQL", "Python", "Excel"],
                               "good": ["Power BI", "Tableau", "Pandas", "Statistics", "R"]},
    "Data Scientist":         {"must": ["Python", "Machine Learning"],
                               "good": ["SQL", "Statistics", "Deep Learning", "NLP", "Scikit-learn", "TensorFlow", "Pandas"]},
    "Business Analyst":       {"must": ["SQL", "Excel"],
                               "good": ["Power BI", "Tableau", "Statistics", "R", "Python"]},
    "ML Engineer":            {"must": ["Python", "Machine Learning"],
                               "good": ["Deep Learning", "TensorFlow", "NLP", "PySpark", "AWS", "Azure", "Scikit-learn"]},
    "Data Engineer":          {"must": ["Python", "SQL"],
                               "good": ["PySpark", "Azure", "AWS", "Databricks", "Airflow", "Scala", "Kafka"]},
    "Product Analyst/Manager":{"must": ["SQL", "Excel"],
                               "good": ["Tableau", "Power BI", "Statistics", "Python", "Looker"]},
}

ROLE_COLORS = {
    "Data Analyst":            "#6c63ff",
    "Data Scientist":          "#43e97b",
    "Business Analyst":        "#f7c59f",
    "ML Engineer":             "#38f9d7",
    "Data Engineer":           "#ff6584",
    "Product Analyst/Manager": "#c471ed",
}

# ── JOB DATASET ───────────────────────────────
JOBS = [
    # Data Analyst
    {"title":"Junior Data Analyst","company":"Super Scholar","city":"Delhi","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"JioSaavn","city":"Mumbai","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Nykaa","city":"Bengaluru","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Renault Nissan","city":"Chennai","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"LTIMindtree","city":"Pune","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Talent Disruptors","city":"Remote","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst - Operations","company":"apna","city":"Bengaluru","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Airtel Digital","city":"Gurugram","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Mastercard","city":"Gurugram","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Birlasoft","city":"Pune","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Saint-Gobain India","city":"Chennai","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst - Remote","company":"VGreenTek","city":"Bengaluru","level":"Entry","cat":"Data Analyst","emp":"Contract"},
    {"title":"Graduate Data Analyst","company":"Arcadis","city":"Bengaluru","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"WinZO","city":"Delhi","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Zeno Health","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"InfiHire","city":"Gurugram","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Rezo.ai","city":"Noida","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Chubb","city":"Bengaluru","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Freshworks","city":"Chennai","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Lead Data Analyst","company":"HiveMinds","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst - Python & Power BI","company":"Heubach","city":"Vadodara","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Phenom","city":"Hyderabad","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Wipro","city":"Bengaluru","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Ascendion","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Sr. Data Analyst","company":"Vonage","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Microsoft","city":"Bengaluru","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Financial Data Analyst","company":"Moody's Corporation","city":"Bengaluru","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"People Data Analyst","company":"bp","city":"Pune","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst - Compliance","company":"Standard Chartered","city":"Bengaluru","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Cimpress India","city":"Bengaluru","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"S&P Global","city":"Hyderabad","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst-PySpark","company":"Idyllic Services","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"ICE","city":"Hyderabad","level":"Not Specified","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Assistant Manager Data Analyst","company":"Unilever","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst III","company":"Bristol Myers Squibb","city":"Hyderabad","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"TELUS International","city":"Remote","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Annalect India","city":"Bengaluru","level":"Associate","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Senior Data Analyst","company":"Robosoft Technologies","city":"Bengaluru","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst with Python","company":"Arting Digital","city":"Mumbai","level":"Mid-Senior","cat":"Data Analyst","emp":"Full-time"},
    {"title":"Data Analyst","company":"Alp Consulting","city":"Bengaluru","level":"Entry","cat":"Data Analyst","emp":"Full-time"},
    # Data Scientist
    {"title":"Data Scientist","company":"IndusInd Bank","city":"Gurugram","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"LTIMindtree","city":"Mumbai","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Amgen","city":"Bengaluru","level":"Associate","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"NIRA","city":"Bengaluru","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Google","city":"Bengaluru","level":"Not Specified","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Mondelez International","city":"Mumbai","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Joveo","city":"Bengaluru","level":"Associate","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Spinny","city":"Gurugram","level":"Associate","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"LTIMindtree","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Science Intern","company":"NextGen AI","city":"Remote","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"FanCode","city":"Mumbai","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Sr. Data Scientist","company":"Quantified HR","city":"Gurugram","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"EXL","city":"Gurugram","level":"Associate","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Air India Express","city":"Gurugram","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Medtronic LABS","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Quantzig","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Senior Data Scientist","company":"Foundation AI","city":"Hyderabad","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Qualys","city":"Pune","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"HARMAN International","city":"Bengaluru","level":"Associate","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Sanofi","city":"Hyderabad","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Clearwater Analytics","city":"Noida","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Science Manager","company":"Eli Lilly","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Applied Data Scientist","company":"Microsoft","city":"Bengaluru","level":"Not Specified","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Tata Consultancy Services","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Navi","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Lead Data Scientist","company":"Anko GCC","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist","company":"Piramal Capital","city":"Bengaluru","level":"Mid-Senior","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Director Data Science","company":"Lowe's India","city":"Bengaluru","level":"Director","cat":"Data Scientist","emp":"Full-time"},
    {"title":"Data Scientist - Digital Marketing","company":"IndiGo","city":"Gurugram","level":"Entry","cat":"Data Scientist","emp":"Full-time"},
    # Business Analyst
    {"title":"Business Analyst","company":"Hike","city":"Delhi","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"Junglee Games","city":"Gurugram","level":"Entry","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"Visit Health","city":"Gurugram","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"Botminds AI","city":"Chennai","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"Pranathi Software","city":"Hyderabad","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Lead Business Analyst","company":"KPMG India","city":"Bengaluru","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"EXL","city":"Gurugram","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst - Analytics","company":"Citi","city":"Bengaluru","level":"Not Specified","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst - ESG","company":"Wipro","city":"Bengaluru","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Business Analyst","company":"Birlasoft","city":"Noida","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    {"title":"Senior Business Analyst","company":"Caidya","city":"Remote","level":"Mid-Senior","cat":"Business Analyst","emp":"Full-time"},
    # ML Engineer
    {"title":"Machine Learning Analyst","company":"Google","city":"Hyderabad","level":"Not Specified","cat":"ML Engineer","emp":"Full-time"},
    {"title":"Machine Learning Analyst","company":"Google","city":"Bengaluru","level":"Not Specified","cat":"ML Engineer","emp":"Full-time"},
    {"title":"Machine Learning Engineer","company":"IQVIA","city":"Bengaluru","level":"Associate","cat":"ML Engineer","emp":"Full-time"},
    {"title":"AI / ML Specialist","company":"Norconsulting","city":"Remote","level":"Mid-Senior","cat":"ML Engineer","emp":"Contract"},
    {"title":"NLP/ML Engineer","company":"Acme Services","city":"Pune","level":"Mid-Senior","cat":"ML Engineer","emp":"Full-time"},
    {"title":"ML Engineer","company":"CodersBrain","city":"Bengaluru","level":"Mid-Senior","cat":"ML Engineer","emp":"Full-time"},
    {"title":"Machine Learning Engineer","company":"InVitro Capital","city":"Remote","level":"Mid-Senior","cat":"ML Engineer","emp":"Contract"},
    {"title":"Director of Data & ML","company":"Suki","city":"Bengaluru","level":"Director","cat":"ML Engineer","emp":"Full-time"},
    # Data Engineer
    {"title":"Data Engineer","company":"Allica Bank","city":"Bengaluru","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"Aidetic","city":"Bengaluru","level":"Entry","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer - Cyber Security","company":"_VOIS","city":"Pune","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer - Python/ETL","company":"EXL","city":"Noida","level":"Associate","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"i-Qode Digital","city":"Mumbai","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Director Data Engineering","company":"Walmart","city":"Bengaluru","level":"Director","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"RandomTrees","city":"Remote","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineering (Azure)","company":"RecruitingSniper","city":"Pune","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"Ascendion","city":"Bengaluru","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Business Intelligence Developer","company":"Ford Motor Company","city":"Chennai","level":"Not Specified","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"Lera Technologies","city":"Pune","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    {"title":"Data Engineer","company":"Lera Technologies","city":"Hyderabad","level":"Mid-Senior","cat":"Data Engineer","emp":"Full-time"},
    # Product Analyst
    {"title":"Product Analyst","company":"EarnIn","city":"Bengaluru","level":"Mid-Senior","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Product Manager","company":"PhonePe","city":"Bengaluru","level":"Associate","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Product Analyst","company":"Visa","city":"Bengaluru","level":"Mid-Senior","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Associate Product Manager","company":"Keka HR","city":"Hyderabad","level":"Entry","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Product Manager Personalization","company":"Google","city":"Bengaluru","level":"Not Specified","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Principal Product Manager","company":"Opendoor","city":"Hyderabad","level":"Mid-Senior","cat":"Product Analyst/Manager","emp":"Full-time"},
    {"title":"Lead Product Analyst","company":"Freshworks","city":"Bengaluru","level":"Mid-Senior","cat":"Product Analyst/Manager","emp":"Full-time"},
]

df_jobs = pd.DataFrame(JOBS)

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
    city_filter = st.selectbox("City", ["All"] + sorted(df_jobs["city"].unique().tolist()))
with col2:
    level_filter = st.selectbox("Level", ["All", "Entry", "Associate", "Mid-Senior", "Director", "Not Specified"])
with col3:
    emp_filter = st.selectbox("Employment Type", ["All", "Full-time", "Contract", "Internship"])

st.markdown("---")

# ── RECOMMEND BUTTON ──────────────────────────
if st.button("▶ Find My Jobs", type="primary", use_container_width=True):

    if len(selected_skills) == 0:
        st.warning("Please select at least one skill from the sidebar!")

    else:
        selected_set = set(selected_skills)

        # Score each role
        role_scores = []
        for role, mapping in ROLE_SKILLS.items():
            must         = mapping["must"]
            good         = mapping["good"]
            must_matched = [s for s in must if s in selected_set]
            good_matched = [s for s in good if s in selected_set]
            must_missing = [s for s in must if s not in selected_set]

            if len(must_matched) == 0:
                continue  # skip role entirely

            must_score  = len(must_matched) / len(must)
            good_score  = len(good_matched) / len(good) if good else 0
            total_score = must_score * 0.65 + good_score * 0.35

            role_scores.append({
                "role":         role,
                "score":        round(total_score * 100),
                "must_matched": must_matched,
                "good_matched": good_matched,
                "must_missing": must_missing,
                "total_must":   len(must),
                "total_good":   len(good),
            })

        role_scores = sorted(role_scores, key=lambda x: x["score"], reverse=True)

        if not role_scores:
            st.error("No roles matched. Try adding core skills like Python, SQL, or Excel.")
        else:
            # ── ROLE CARDS ────────────────────────────────
            st.subheader("🎯 Best Matching Roles")
            cols = st.columns(min(len(role_scores), 3))
            for i, r in enumerate(role_scores):
                col = cols[i % 3]
                with col:
                    st.metric(label=r["role"], value=f"{r['score']}% fit")
                    st.progress(r["score"] / 100)
                    st.caption(f"✅ Core matched: {', '.join(r['must_matched']) or 'None'}")
                    if r["good_matched"]:
                        st.caption(f"➕ Bonus: {', '.join(r['good_matched'])}")
                    if r["must_missing"]:
                        st.caption(f"❌ Missing core: {', '.join(r['must_missing'])}")
                    total_jobs = df_jobs[df_jobs["cat"] == r["role"]].shape[0]
                    st.caption(f"📋 {total_jobs} openings in dataset")
                    st.markdown("")

            # ── JOB LISTINGS ──────────────────────────────
            st.markdown("---")
            st.subheader("📋 Matching Job Listings")

            matched_roles = set(r["role"] for r in role_scores)
            filtered = df_jobs[df_jobs["cat"].isin(matched_roles)].copy()

            if city_filter  != "All": filtered = filtered[filtered["city"]  == city_filter]
            if level_filter != "All": filtered = filtered[filtered["level"] == level_filter]
            if emp_filter   != "All": filtered = filtered[filtered["emp"]   == emp_filter]

            st.markdown(f"**{len(filtered)} jobs found**")

            if filtered.empty:
                st.info("No jobs match current filters. Try relaxing city or level.")
            else:
                for _, row in filtered.iterrows():
                    with st.expander(f"**{row['title']}** — {row['company']}"):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.markdown(f"📍 **City:** {row['city']}")
                        c2.markdown(f"🏷️ **Level:** {row['level']}")
                        c3.markdown(f"💼 **Role:** {row['cat']}")
                        c4.markdown(f"🕐 **Type:** {row['emp']}")

elif len(selected_skills) > 0:
    st.info(f"✅ {len(selected_skills)} skills selected — click **Find My Jobs** to see recommendations!")
else:
    st.info("👈 Select your skills from the sidebar, then click **Find My Jobs**")
