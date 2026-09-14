import streamlit as st
import requests
import base64
from pathlib import Path

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CreditLens | Credit Risk",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Background Image
# --------------------------------------------------

def get_base64_image(image_path):
    path = Path(image_path)

    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()

    return ""


image_base64 = get_base64_image(
    r"C:\Users\saumya\OneDrive\Desktop\LoanRisk\bg.jpg"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    * {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background:
            linear-gradient(
                135deg,
                rgba(5, 15, 35, 0.97),
                rgba(8, 28, 55, 0.93)
            ),
            url("data:image/jpeg;base64,{image_base64}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 0.8rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
        padding-bottom: 0.4rem;
    }}

    header {{
        visibility: hidden;
    }}

    /* Reduce Streamlit default spacing (but keep it breathable) */

    div[data-testid="stVerticalBlock"] {{
        gap: 0.3rem;
    }}

    div[data-testid="stHorizontalBlock"] {{
        gap: 0.8rem;
    }}

    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"] {{
        margin-bottom: -2px;
    }}

    /* Brand */

    .brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 2px;
    }}

    .brand-icon {{
        width: 36px;
        height: 36px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        color: white;
        font-size: 19px;
        box-shadow: 0 6px 18px rgba(56, 189, 248, 0.2);
    }}

    .brand-name {{
        color: #f8fafc;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }}

    .brand-name span {{
        color: #38bdf8;
    }}

    .tagline {{
        color: #94a3b8;
        font-size: 10px;
        margin-left: 46px;
        margin-bottom: 12px;
    }}

    /* Hero */

    .hero-title {{
        color: #f8fafc;
        font-size: 30px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.2px;
        margin-bottom: 5px;
    }}

    .hero-title span {{
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.5;
        max-width: 700px;
        margin-bottom: 14px;
    }}

    /* Input section */

    .glass-card {{
        background: rgba(15, 30, 55, 0.76);
        border: 1px solid rgba(148, 163, 184, 0.17);
        border-radius: 18px;
        padding: 16px 20px 14px 20px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }}

    .section-heading {{
        color: #f8fafc;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 1px;
    }}

    .section-description {{
        color: #94a3b8;
        font-size: 10px;
        margin-bottom: 8px;
    }}

    .section-label {{
        color: #38bdf8;
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-top: 8px;
        margin-bottom: 3px;
    }}

    /* Inputs */

    div[data-baseweb="input"],
    div[data-baseweb="select"] > div,
    textarea {{
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid #334155 !important;
        border-radius: 9px !important;
        color: #f8fafc !important;
        min-height: 35px !important;
    }}

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 1px #38bdf8 !important;
    }}

    label {{
        color: #cbd5e1 !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        margin-bottom: 1px !important;
    }}

    .stNumberInput input,
    .stSelectbox input {{
        color: #f8fafc !important;
        font-size: 11px !important;
    }}

    div[data-baseweb="select"] * {{
        color: #f8fafc !important;
        font-size: 11px !important;
    }}

    /* Button */

    .stButton {{
        margin-top: 6px;
    }}

    .stButton > button {{
        width: 100%;
        height: 40px;
        border: none;
        border-radius: 10px;
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.1px;
        box-shadow: 0 7px 20px rgba(14, 165, 233, 0.2);
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
        border: none;
    }}

    /* Risk assessment - only subtle boundary */

    .result-card {{
        background: transparent;
        border: 1px solid rgba(129, 140, 248, 0.38);
        border-radius: 18px;
        padding: 18px 22px;
        min-height: 0;
        box-shadow: none;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }}

    .result-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }}

    .result-title {{
        color: #f8fafc;
        font-size: 15px;
        font-weight: 700;
    }}

    .live-badge {{
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.28);
        color: #86efac;
        padding: 3px 7px;
        border-radius: 14px;
        font-size: 8px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}

    .empty-result {{
        min-height: 145px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }}

    .empty-icon {{
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.18);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        margin-bottom: 10px;
    }}

    .empty-title {{
        color: #e2e8f0;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 4px;
    }}

    .empty-text {{
        color: #64748b;
        font-size: 10px;
        max-width: 240px;
        line-height: 1.5;
    }}

    .probability-label {{
        color: #94a3b8;
        font-size: 11px;
        margin-bottom: 4px;
    }}

    .probability {{
        color: #f8fafc;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 9px;
    }}

    .probability span {{
        color: #64748b;
        font-size: 17px;
        letter-spacing: 0;
    }}

    .risk-pill {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 25px;
        font-size: 10px;
        font-weight: 700;
        margin-bottom: 15px;
    }}

    .low-risk {{
        color: #86efac;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.28);
    }}

    .medium-risk {{
        color: #fde68a;
        background: rgba(234, 179, 8, 0.1);
        border: 1px solid rgba(234, 179, 8, 0.28);
    }}

    .high-risk {{
        color: #fca5a5;
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.28);
    }}

    .prediction-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-top: 1px solid rgba(148, 163, 184, 0.13);
    }}

    .prediction-label {{
        color: #94a3b8;
        font-size: 10px;
    }}

    .prediction-value {{
        color: #e2e8f0;
        font-size: 11px;
        font-weight: 700;
    }}

    .footer {{
        color: #475569;
        font-size: 9px;
        text-align: center;
        margin-top: 8px;
    }}

    .stAlert {{
        border-radius: 10px !important;
        font-size: 11px !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">⌁</div>
        <div class="brand-name">Credit<span>Lens</span></div>
    </div>

    <div class="tagline">
        Intelligent credit risk assessment powered by machine learning
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-title">
        Make smarter lending<br>
        decisions with <span>confidence.</span>
    </div>

    <div class="hero-subtitle">
        Evaluate loan applications using a machine learning-powered
        credit risk model. Enter applicant details to estimate default
        probability and assess overall risk.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Layout
# --------------------------------------------------

left_column, right_column = st.columns(
    [1.12, 0.88],
    gap="medium"
)

# --------------------------------------------------
# Input Form
# --------------------------------------------------

with left_column:

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-heading">Loan application details</div>
            <div class="section-description">
                Provide the applicant's financial and personal information.
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">Loan information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        loan_amnt = st.number_input(
            "Loan amount ($)",
            min_value=500.0,
            max_value=100000.0,
            value=15000.0,
            step=500.0
        )

    with col2:
        term_months = st.selectbox(
            "Loan term",
            [36.0, 60.0],
            format_func=lambda x: f"{int(x)} months"
        )

    col3, col4 = st.columns(2)

    with col3:
        int_rate = st.number_input(
            "Interest rate (%)",
            min_value=0.0,
            max_value=40.0,
            value=12.5,
            step=0.1
        )

    with col4:
        annual_inc = st.number_input(
            "Annual income ($)",
            min_value=1000.0,
            max_value=1000000.0,
            value=60000.0,
            step=1000.0
        )

    st.markdown(
        '<div class="section-label">Financial profile</div>',
        unsafe_allow_html=True
    )

    col5, col6 = st.columns(2)

    with col5:
        dti = st.number_input(
            "Debt-to-income ratio",
            min_value=0.0,
            max_value=100.0,
            value=18.0,
            step=0.1
        )

    with col6:
        fico_avg = st.number_input(
            "Average FICO score",
            min_value=300.0,
            max_value=850.0,
            value=700.0,
            step=1.0
        )

    st.markdown(
        '<div class="section-label">Applicant profile</div>',
        unsafe_allow_html=True
    )

    col7, col8 = st.columns(2)

    with col7:
        grade = st.selectbox(
            "Credit grade",
            ["A", "B", "C", "D", "E", "F", "G"]
        )

    with col8:
        emp_length = st.selectbox(
            "Employment length",
            [
                "< 1 year",
                "1 year",
                "2 years",
                "3 years",
                "4 years",
                "5 years",
                "6 years",
                "7 years",
                "8 years",
                "9 years",
                "10+ years"
            ]
        )

    col9, col10 = st.columns(2)

    with col9:
        home_ownership = st.selectbox(
            "Home ownership",
            ["RENT", "MORTGAGE", "OWN", "OTHER"]
        )

    with col10:
        verification_status = st.selectbox(
            "Income verification",
            ["Verified", "Source Verified", "Not Verified"]
        )

    purpose = st.selectbox(
        "Loan purpose",
        [
            "debt_consolidation",
            "credit_card",
            "home_improvement",
            "major_purchase",
            "small_business",
            "medical",
            "car",
            "wedding",
            "vacation",
            "other"
        ]
    )

    predict_clicked = st.button(
        "Assess credit risk  →",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Result Panel
# --------------------------------------------------

with right_column:

    st.markdown(
        """
        <div class="result-card">
            <div class="result-top">
                <div class="result-title">Risk assessment</div>
                <div class="live-badge">● MODEL READY</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    if not predict_clicked:

        st.markdown(
            """
            <div class="empty-result">
                <div class="empty-icon">◈</div>
                <div class="empty-title">Awaiting application data</div>
                <div class="empty-text">
                    Complete the form and click “Assess credit risk”
                    to generate a prediction.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        payload = {
            "loan_amnt": loan_amnt,
            "term_months": term_months,
            "int_rate": int_rate,
            "annual_inc": annual_inc,
            "dti": dti,
            "fico_avg": fico_avg,
            "grade": grade,
            "emp_length": emp_length,
            "home_ownership": home_ownership,
            "verification_status": verification_status,
            "purpose": purpose
        }

        try:
            response = requests.post(
                "https://loanrisk-iw25.onrender.com/predic",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:

                result = response.json()

                probability = result["default_probability"] * 100
                prediction = result["default_prediction"]
                risk_level = result["risk_level"]

                if risk_level == "Low Risk":
                    risk_class = "low-risk"
                elif risk_level == "Medium Risk":
                    risk_class = "medium-risk"
                else:
                    risk_class = "high-risk"

                prediction_text = (
                    "Potential default"
                    if prediction == 1
                    else "Likely non-default"
                )

                st.markdown(
                    f"""
                    <div class="probability-label">
                        Estimated default probability
                    </div>

                    <div class="probability">
                        {probability:.2f}<span>%</span>
                    </div>

                    <div class="risk-pill {risk_class}">
                        ● &nbsp; {risk_level}
                    </div>

                    <div class="prediction-row">
                        <div class="prediction-label">Model prediction</div>
                        <div class="prediction-value">
                            {prediction_text}
                        </div>
                    </div>

                    <div class="prediction-row">
                        <div class="prediction-label">Assessment status</div>
                        <div class="prediction-value">Completed</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.error(
                    f"API error: {response.status_code} — {response.text}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the prediction API. "
                "Please make sure the FastAPI Docker container is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The prediction request timed out. Please try again."
            )

        except Exception as error:
            st.error(f"Something went wrong: {error}")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        CreditLens · Machine Learning Credit Risk Assessment ·
        For demonstration purposes
    </div>
    """,
    unsafe_allow_html=True
)
