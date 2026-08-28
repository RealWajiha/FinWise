import os

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

# Load non-secret configuration from .env if available.
#
# IMPORTANT:
# No OpenAI API key is loaded from the environment.
# The user supplies their own API key at runtime through
# the Streamlit interface.
load_dotenv()


# ============================================================
# OPENAI MODEL CONFIGURATION
# ============================================================

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)


# ============================================================
# CURRENCIES
# ============================================================

CURRENCIES = [
    "USD",
    "PKR",
    "EUR",
    "GBP",
]


# ============================================================
# FINANCIAL GOALS
# ============================================================

FINANCIAL_GOALS = [
    "Save money",
    "Emergency fund",
    "Pay off debt",
    "Vacation",
    "Start a business",
    "Improve budgeting",
]


# ============================================================
# EXPENSE CATEGORIES
# ============================================================

EXPENSE_CATEGORIES = [
    "housing/rent",
    "food",
    "transportation",
    "utilities",
    "education",
    "healthcare",
    "entertainment",
    "loan/debt",
    "other",
]