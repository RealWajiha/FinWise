def calculate_financials(
    monthly_income,
    expenses,
    current_savings
):
    total_expenses = sum(expenses.values())

    remaining_income = monthly_income - total_expenses

    if monthly_income > 0:
        savings_ratio = (current_savings / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100
    else:
        savings_ratio = 0
        expense_ratio = 0

    preliminary_score = calculate_preliminary_score(
        monthly_income,
        total_expenses,
        remaining_income,
        savings_ratio,
        expenses.get("loan/debt", 0)
    )

    return {
        "total_expenses": round(total_expenses, 2),
        "remaining_income": round(remaining_income, 2),
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "preliminary_score": preliminary_score
    }


def calculate_preliminary_score(
    income,
    expenses,
    remaining,
    savings_ratio,
    debt
):
    if income <= 0:
        return 0

    score = 0

    # Savings component
    if savings_ratio >= 20:
        score += 30
    elif savings_ratio >= 10:
        score += 20
    elif savings_ratio > 0:
        score += 10

    # Remaining income component
    if remaining > 0:
        score += 25
    elif remaining == 0:
        score += 10

    # Expense ratio component
    expense_ratio = (expenses / income) * 100

    if expense_ratio <= 50:
        score += 25
    elif expense_ratio <= 70:
        score += 20
    elif expense_ratio <= 90:
        score += 10

    # Debt component
    debt_ratio = (debt / income) * 100

    if debt_ratio <= 10:
        score += 20
    elif debt_ratio <= 30:
        score += 10

    return min(score, 100)