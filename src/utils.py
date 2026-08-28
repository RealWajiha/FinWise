import json


def safe_json_parse(text):
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass

        return {
            "financial_summary": "Unable to parse AI response.",
            "financial_health_score": 0,
            "spending_analysis": [],
            "risk_level": "Unknown",
            "top_priorities": [],
            "budget_recommendations": [],
            "savings_strategy": [],
            "next_month_action_plan": []
        }


def format_expenses(expenses):
    return "\n".join(
        f"{category}: {amount}"
        for category, amount in expenses.items()
    )