# ============================================================
# FinWise AI
# API Key Screen -> Financial Guidance Interface
# ============================================================

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="FinWise AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------

if "api_key" not in st.session_state:
    st.session_state.api_key = None


# ============================================================
# API KEY SCREEN
# ============================================================

if not st.session_state.api_key:

    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>💰 FinWise AI</h1>
            <p style="font-size:20px; color:gray;">
                AI-Powered Personal Financial Guidance Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Enter OpenAI API Key")

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-..."
        )

        st.caption(
            "Your API key is used only for this session."
        )

        if st.button(
            "Continue →",
            type="primary",
            use_container_width=True
        ):

            if not api_key.strip():

                st.error("Please enter your API key.")

            elif not api_key.startswith("sk-"):

                st.error("Please enter a valid OpenAI API key.")

            else:

                st.session_state.api_key = api_key
                st.rerun()

    st.stop()


# ============================================================
# FINWISE INTERFACE
# ============================================================

st.title("💰 FinWise AI")

st.markdown(
    """
    **AI-Powered Personal Financial Guidance Assistant**

    FinWise AI analyzes your financial information and provides
    educational guidance about budgeting, risk, savings and
    financial planning.
    """
)

st.warning(
    "⚠️ FinWise AI provides educational financial guidance only. "
    "It is not professional financial, investment, tax or legal advice."
)


# ------------------------------------------------------------
# Initialize LLM
# ------------------------------------------------------------

try:

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=st.session_state.api_key
    )

except Exception:

    st.error("Unable to initialize the AI model.")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Financial Profile")

    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    monthly_expenses = st.number_input(
        "Monthly Expenses",
        min_value=0.0,
        value=30000.0,
        step=1000.0
    )

    savings = st.number_input(
        "Current Savings",
        min_value=0.0,
        value=100000.0,
        step=5000.0
    )

    debt = st.number_input(
        "Total Debt",
        min_value=0.0,
        value=0.0,
        step=5000.0
    )

    st.divider()

    st.subheader("🎯 Financial Goal")

    goal = st.selectbox(
        "Primary Goal",
        [
            "Build Emergency Fund",
            "Save Money",
            "Reduce Debt",
            "Create a Budget",
            "Plan for a Major Purchase",
            "General Financial Planning"
        ]
    )

    goal_amount = st.number_input(
        "Target Amount",
        min_value=0.0,
        value=100000.0,
        step=5000.0
    )

    st.divider()

    st.subheader("⚠️ Risk Preference")

    risk_level = st.select_slider(
        "Risk Tolerance",
        options=[
            "Very Low",
            "Low",
            "Moderate",
            "High",
            "Very High"
        ],
        value="Moderate"
    )

    st.divider()

    if st.button(
        "🔑 Change API Key",
        use_container_width=True
    ):

        st.session_state.api_key = None
        st.rerun()


# ============================================================
# MAIN DASHBOARD
# ============================================================

st.header("📊 Financial Overview")

income_col, expense_col, savings_col, debt_col = st.columns(4)

with income_col:

    st.metric(
        "Monthly Income",
        f"{monthly_income:,.0f}"
    )

with expense_col:

    st.metric(
        "Monthly Expenses",
        f"{monthly_expenses:,.0f}"
    )

with savings_col:

    st.metric(
        "Current Savings",
        f"{savings:,.0f}"
    )

with debt_col:

    st.metric(
        "Total Debt",
        f"{debt:,.0f}"
    )


# ------------------------------------------------------------
# Monthly Balance
# ------------------------------------------------------------

monthly_balance = monthly_income - monthly_expenses

st.write("")

if monthly_balance >= 0:

    st.success(
        f"💵 Estimated Monthly Balance: "
        f"{monthly_balance:,.0f}"
    )

else:

    st.error(
        f"⚠️ Estimated Monthly Deficit: "
        f"{abs(monthly_balance):,.0f}"
    )


# ============================================================
# ADDITIONAL INFORMATION
# ============================================================

st.header("📝 Additional Financial Information")

additional_info = st.text_area(
    "Tell FinWise anything else about your financial situation",
    placeholder=(
        "Example: I want to save for a laptop within 6 months "
        "and also build an emergency fund..."
    ),
    height=120
)


# ============================================================
# GENERATE FINANCIAL PLAN
# ============================================================

if st.button(
    "💡 Generate Financial Plan",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "🧠 FinWise is analyzing your financial profile..."
    ):

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are FinWise AI, an educational financial
                    planning assistant.

                    Analyze the user's financial information and
                    provide practical, easy-to-understand guidance.

                    Do NOT claim to be a licensed financial advisor.
                    Do NOT guarantee financial returns.
                    Do NOT provide personalized instructions to buy
                    or sell specific securities.

                    Structure the response using these sections:

                    ## Financial Summary

                    ## Budget Analysis

                    ## Risk Assessment

                    ## Savings Strategy

                    ## Action Plan

                    ## Important Considerations

                    Give realistic and responsible guidance.
                    """
                ),

                (
                    "human",
                    """
                    Financial Profile:

                    Monthly Income:
                    {monthly_income}

                    Monthly Expenses:
                    {monthly_expenses}

                    Current Savings:
                    {savings}

                    Total Debt:
                    {debt}

                    Monthly Balance:
                    {monthly_balance}

                    Financial Goal:
                    {goal}

                    Target Amount:
                    {goal_amount}

                    Risk Tolerance:
                    {risk_level}

                    Additional Information:
                    {additional_info}
                    """
                )
            ]
        )

        chain = prompt | llm

        try:

            response = chain.invoke(
                {
                    "monthly_income": monthly_income,
                    "monthly_expenses": monthly_expenses,
                    "savings": savings,
                    "debt": debt,
                    "monthly_balance": monthly_balance,
                    "goal": goal,
                    "goal_amount": goal_amount,
                    "risk_level": risk_level,
                    "additional_info": additional_info
                }
            )

            st.success(
                "✅ Financial plan generated successfully!"
            )

            st.divider()

            st.header("📋 Your FinWise Plan")

            st.markdown(response.content)

        except Exception as e:

            st.error(
                "❌ Unable to generate the financial plan."
            )

            st.caption(
                "Please check your API key and try again."
            )

            with st.expander("Technical Details"):

                st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FinWise AI | Educational Prototype | "
    "Python • Streamlit • LangChain • OpenAI"
)