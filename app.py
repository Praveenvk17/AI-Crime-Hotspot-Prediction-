import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Crime Prediction",
    page_icon="🚔",
    layout="wide"
)

# ==============================
# RCB-STYLE PROFESSIONAL UI
# ==============================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #080808 0%, #1a0000 55%, #2b0000 100%);
        color: #f8fafc;
    }

    h1, h2, h3 {
        color: #f5c542;
        font-weight: 800;
    }

    .stMetric {
        background: linear-gradient(135deg, #111111, #2b0000);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #f5c542;
        box-shadow: 0 0 12px rgba(245, 197, 66, 0.15);
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    .stButton button {
        background: linear-gradient(90deg, #b91c1c, #f5c542);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 9px 20px;
        font-weight: 700;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #f5c542, #b91c1c);
        color: black;
    }

    section[data-testid="stSidebar"] {
        background-color: #080808;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# LOGIN CONFIG
# ==============================
ADMIN_PASSWORD = "crime@admin"
POLICE_PASSWORD = "police@secure"

for key, value in {
    "logged_in": False,
    "role": "",
    "prediction_result": None,
    "risk_level": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==============================
# LOGIN PAGE
# ==============================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            "<h1 style='text-align:center;'>🚔 Crime Prediction Login</h1>",
            unsafe_allow_html=True
        )

        st.info("Secure Access Portal")

        role = st.selectbox(
            "Select Role",
            ["Admin", "Police Officer"]
        )

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if st.button("Login"):
            if role == "Admin" and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.role = "ADMIN"
                st.rerun()

            elif role == "Police Officer" and password == POLICE_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.role = "POLICE OFFICER"
                st.rerun()

            else:
                st.error("❌ Invalid Password")

    st.stop()

# ==============================
# LOAD MODEL + DATA
# ==============================
model = joblib.load("models/crime_model.pkl")
state_encoder = joblib.load("models/state_encoder.pkl")
district_encoder = joblib.load("models/district_encoder.pkl")

df = pd.read_csv("crime.csv")
df.columns = df.columns.str.strip()

df = df[
    ~df["DISTRICT"].str.contains(
        "TOTAL|ZZ TOTAL",
        na=False
    )
]

is_admin = st.session_state.role == "ADMIN"

# ==============================
# HEADER
# ==============================
col1, col2 = st.columns([8, 1])

with col1:
    st.title("🚔 AI Crime Hotspot Prediction System")

with col2:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.prediction_result = None
        st.session_state.risk_level = None
        st.rerun()

st.success(f"Logged in as: {st.session_state.role}")

st.write(
    "AI-powered crime prediction, hotspot analysis, risk detection and police alert system"
)

# ==============================
# ADMIN DASHBOARD + MULTI CSV
# ==============================
if is_admin:

    st.subheader("📊 Crime Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Records", len(df))

    with c2:
        st.metric("States", df["STATE/UT"].nunique())

    with c3:
        st.metric("Districts", df["DISTRICT"].nunique())

    st.divider()

    st.subheader("📁 Multi CSV Upload & Auto Analysis")

    uploaded_files = st.file_uploader(
        "Upload multiple crime CSV files",
        type=["csv"],
        accept_multiple_files=True
    )

    if uploaded_files:
        combined_data = []

        for uploaded_file in uploaded_files:
            try:
                temp_df = pd.read_csv(uploaded_file)
                temp_df.columns = temp_df.columns.str.strip()

                st.success(f"Loaded: {uploaded_file.name}")
                st.write("Columns:", temp_df.columns.tolist())

                required_columns = ["STATE/UT", "DISTRICT", "YEAR"]

                if all(col in temp_df.columns for col in required_columns):

                    numeric_cols = (
                        temp_df
                        .select_dtypes(include=["int64", "float64"])
                        .columns
                        .tolist()
                    )

                    if "YEAR" in numeric_cols:
                        numeric_cols.remove("YEAR")

                    if "TOTAL IPC CRIMES" in temp_df.columns:
                        temp_df["AUTO_TOTAL_CRIMES"] = temp_df["TOTAL IPC CRIMES"]

                    elif numeric_cols:
                        temp_df["AUTO_TOTAL_CRIMES"] = temp_df[numeric_cols].sum(axis=1)

                    else:
                        st.warning("No numeric crime columns found")
                        continue

                    combined_data.append(temp_df)
                    st.info("✅ Supported crime dataset format")

                else:
                    st.warning(
                        "Unsupported format. Required columns: STATE/UT, DISTRICT, YEAR"
                    )

            except Exception as e:
                st.error(f"Error reading {uploaded_file.name}: {e}")

        if combined_data:
            multi_df = pd.concat(combined_data, ignore_index=True)

            st.subheader("📊 Uploaded CSV Combined Analysis")

            u1, u2, u3 = st.columns(3)

            with u1:
                st.metric("Uploaded Rows", len(multi_df))

            with u2:
                st.metric("Uploaded States", multi_df["STATE/UT"].nunique())

            with u3:
                st.metric("Uploaded Districts", multi_df["DISTRICT"].nunique())

            uploaded_state_crime = (
                multi_df.groupby("STATE/UT")["AUTO_TOTAL_CRIMES"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.subheader("🚨 Uploaded Data - Top Crime States")

            fig_upload, ax_upload = plt.subplots(figsize=(5, 3))
            uploaded_state_crime.plot(kind="bar", ax=ax_upload)
            ax_upload.set_title("Top States from Uploaded CSVs", fontsize=10)
            plt.xticks(rotation=45, fontsize=7)
            plt.yticks(fontsize=7)
            st.pyplot(fig_upload, use_container_width=True)

            uploaded_year_trend = (
                multi_df.groupby("YEAR")["AUTO_TOTAL_CRIMES"]
                .sum()
                .sort_index()
            )

            st.subheader("📈 Uploaded Data - Year Wise Trend")

            fig_year, ax_year = plt.subplots(figsize=(5, 3))
            uploaded_year_trend.plot(kind="line", marker="o", ax=ax_year)
            ax_year.set_title("Uploaded CSV Crime Trend", fontsize=10)
            plt.xticks(fontsize=7)
            plt.yticks(fontsize=7)
            st.pyplot(fig_year, use_container_width=True)

            st.subheader("📄 Uploaded Data Preview")

            st.dataframe(
                multi_df.head(20),
                use_container_width=True
            )

    st.divider()

# ==============================
# CRIME PREDICTION
# ==============================
st.subheader("🔍 Crime Prediction")

states = sorted(df["STATE/UT"].unique())

selected_state = st.selectbox(
    "Select State",
    states
)

districts = sorted(
    df[
        df["STATE/UT"] == selected_state
    ]["DISTRICT"].unique()
)

selected_district = st.selectbox(
    "Select District",
    districts
)

year = st.number_input(
    "Enter Year",
    min_value=2001,
    max_value=2035,
    value=2025
)

if st.button("Predict Crime"):

    state_encoded = state_encoder.transform([selected_state])[0]
    district_encoded = district_encoder.transform([selected_district])[0]

    input_data = pd.DataFrame({
        "STATE/UT": [state_encoded],
        "DISTRICT": [district_encoded],
        "YEAR": [year]
    })

    prediction = model.predict(input_data)[0]

    st.session_state.prediction_result = int(prediction)
    st.session_state.selected_state = selected_state
    st.session_state.selected_district = selected_district
    st.session_state.selected_year = year

    if prediction > 5000:
        st.session_state.risk_level = "HIGH"

    elif prediction > 2000:
        st.session_state.risk_level = "MEDIUM"

    else:
        st.session_state.risk_level = "LOW"

# ==============================
# RESULT SECTION
# ==============================
if st.session_state.prediction_result is not None:

    st.subheader("Prediction Result")

    st.success(
        f"Predicted Total Crimes: {st.session_state.prediction_result}"
    )

    if st.session_state.risk_level == "HIGH":
        st.error("🔴 HIGH RISK AREA")

        recommendation_text = (
            "Increase police patrol frequency, deploy extra officers, "
            "activate CCTV monitoring and strengthen night monitoring."
        )

        st.warning("""
🤖 AI Recommended Actions  
• Increase police patrol frequency  
• Deploy extra officers in hotspot areas  
• Install more CCTV surveillance  
• Strengthen night-time monitoring  
• Conduct public safety awareness
        """)

    elif st.session_state.risk_level == "MEDIUM":
        st.warning("🟠 MEDIUM RISK AREA")

        recommendation_text = (
            "Regular police patrol, monitor suspicious activities "
            "and improve emergency response."
        )

        st.info("""
🤖 AI Recommended Actions  
• Regular police patrol required  
• Monitor suspicious activities  
• Increase public surveillance  
• Improve emergency response
        """)

    else:
        st.success("🟢 LOW RISK AREA")

        recommendation_text = (
            "Maintain routine police patrol, continue community monitoring "
            "and keep surveillance systems active."
        )

        st.info("""
🤖 AI Recommended Actions  
• Maintain routine police patrol  
• Continue community monitoring  
• Keep surveillance systems active
        """)

    # ==============================
    # CRIME CATEGORY
    # ==============================
    st.subheader("🧠 Crime Category Prediction")

    selected_rows = df[
        (df["STATE/UT"] == st.session_state.selected_state)
        &
        (df["DISTRICT"] == st.session_state.selected_district)
    ]

    crime_categories = [
        "MURDER",
        "RAPE",
        "KIDNAPPING & ABDUCTION",
        "ROBBERY",
        "BURGLARY",
        "THEFT",
        "AUTO THEFT",
        "RIOTS",
        "CHEATING"
    ]

    available_categories = [
        col for col in crime_categories
        if col in selected_rows.columns
    ]

    category_scores = (
        selected_rows[available_categories]
        .sum()
        .sort_values(ascending=False)
    )

    predicted_category = category_scores.index[0]

    st.info(
        f"Most likely dominant crime category: **{predicted_category}**"
    )

    category_table = (
        category_scores
        .reset_index()
        .rename(
            columns={
                "index": "Crime Category",
                0: "Crime Count"
            }
        )
    )

    st.dataframe(
        category_table,
        use_container_width=True
    )

    # ==============================
    # SMART ALERT
    # ==============================
    st.subheader("🚨 Smart Crime Alert")

    if st.session_state.risk_level == "HIGH":
        st.error("🚨 ALERT: High Crime Risk Detected!")

        st.warning(
            f"""
High crime probability detected in  
{st.session_state.selected_district}, {st.session_state.selected_state}

Recommended:
• Increase police patrol  
• Deploy extra officers  
• Activate CCTV monitoring
            """
        )

    elif st.session_state.risk_level == "MEDIUM":
        st.warning("⚠️ Moderate Risk Alert")

        st.info(
            f"""
Moderate crime risk predicted in  
{st.session_state.selected_district}, {st.session_state.selected_state}

Recommended:
• Regular patrol  
• Monitor suspicious activity
            """
        )

    else:
        st.success("✅ Area Currently Stable")

        st.info(
            f"""
Low crime probability in  
{st.session_state.selected_district}, {st.session_state.selected_state}

Routine monitoring recommended.
            """
        )

    # ==============================
    # PDF REPORT
    # ==============================
    st.subheader("📄 Download Crime Report")

    if st.button("Generate Police Report PDF"):

        file_name = "crime_report.pdf"

        doc = SimpleDocTemplate(file_name)
        styles = getSampleStyleSheet()
        story = []

        story.append(
            Paragraph(
                "AI Crime Prediction Report",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Police Intelligence Report</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                "Case ID: CR-2025-001",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Generated Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Officer Role: {st.session_state.role}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))

        report_items = [
            ("State", st.session_state.selected_state),
            ("District", st.session_state.selected_district),
            ("Prediction Year", st.session_state.selected_year),
            ("Predicted Crimes", st.session_state.prediction_result),
            ("Risk Level", st.session_state.risk_level),
            ("Likely Crime Category", predicted_category)
        ]

        for title, value in report_items:
            story.append(
                Paragraph(
                    f"<b>{title}:</b> {value}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 15))

        story.append(
            Paragraph(
                "AI Recommendation",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                recommendation_text,
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Generated by AI Crime Hotspot Prediction "
                "& Police Patrol Optimization System",
                styles["Italic"]
            )
        )

        doc.build(story)

        with open(file_name, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_file,
                file_name="Crime_Report.pdf",
                mime="application/pdf"
            )

        st.success("✅ PDF Generated Successfully")

# ==============================
# ADMIN FEATURES
# ==============================
if is_admin:

    st.divider()

    st.subheader("🚨 Top Dangerous Districts")

    selected_state_for_danger = st.selectbox(
        "Select State for Analysis",
        sorted(df["STATE/UT"].unique())
    )

    state_df = df[
        df["STATE/UT"] == selected_state_for_danger
    ]

    dangerous_districts = (
        state_df
        .groupby("DISTRICT")["TOTAL IPC CRIMES"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    st.dataframe(
        dangerous_districts,
        use_container_width=True
    )

    st.subheader("🏆 District Ranking System")

    ranking_df = (
        state_df
        .groupby("DISTRICT")["TOTAL IPC CRIMES"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    ranking_df["Risk Rank"] = (
        ranking_df["TOTAL IPC CRIMES"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )

    ranking_df["Risk Level"] = ranking_df[
        "TOTAL IPC CRIMES"
    ].apply(
        lambda x:
        "HIGH" if x > 5000
        else "MEDIUM" if x > 2000
        else "LOW"
    )

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

    safest_district = (
        ranking_df.tail(1)
        .iloc[0]["DISTRICT"]
    )

    st.success(f"Safest District: {safest_district}")

    st.divider()

    st.subheader("🗺️ Crime Heatmap")

    crime_locations = [
        ["Delhi", 28.6139, 77.2090],
        ["Mumbai", 19.0760, 72.8777],
        ["Chennai", 13.0827, 80.2707],
        ["Bangalore", 12.9716, 77.5946],
        ["Hyderabad", 17.3850, 78.4867],
        ["Kolkata", 22.5726, 88.3639],
        ["Bhopal", 23.2599, 77.4126],
        ["Indore", 22.7196, 75.8577]
    ]

    crime_map = folium.Map(
        location=[22.9734, 78.6569],
        zoom_start=5,
        tiles="OpenStreetMap"
    )

    for city, lat, lon in crime_locations:
        folium.Marker(
            [lat, lon],
            popup=f"Crime Hotspot: {city}",
            tooltip=city,
            icon=folium.Icon(
                color="red",
                icon="info-sign"
            )
        ).add_to(crime_map)

    st_folium(
        crime_map,
        use_container_width=True,
        height=450
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Top Dangerous States")

        state_crime = (
            df.groupby("STATE/UT")["TOTAL IPC CRIMES"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(5, 3))
        state_crime.plot(kind="bar", ax=ax)

        ax.set_title("Top 10 States", fontsize=10)
        plt.xticks(rotation=45, fontsize=7)
        plt.yticks(fontsize=7)

        st.pyplot(
            fig,
            use_container_width=True
        )

    with col2:
        st.subheader("📈 Crime Trend")

        year_crime = (
            df.groupby("YEAR")["TOTAL IPC CRIMES"]
            .sum()
        )

        trend_data = year_crime.to_dict()

        growth_rate = 0.04
        last_value = trend_data[2012]

        for future_year in range(2013, 2026):
            predicted_value = last_value * (1 + growth_rate)
            trend_data[future_year] = predicted_value
            last_value = predicted_value

        year_trend = pd.Series(
            trend_data
        ).sort_index()

        fig2, ax2 = plt.subplots(figsize=(5, 3))

        year_trend.plot(
            kind="line",
            marker="o",
            ax=ax2
        )

        ax2.set_title(
            "Crime Trend (2001–2025)",
            fontsize=10
        )

        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)

        st.pyplot(
            fig2,
            use_container_width=True
        )
