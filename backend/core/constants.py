ADMIN = "ADMIN"
ANALYST = "ANALYST"
VIEWER = "VIEWER"

ROLE_CHOICES = (
    (ADMIN, "Admin"),
    (ANALYST, "Analyst"),
    (VIEWER, "Viewer"),
)

INCOME = "income"
EXPENSE = "expense"
TRANSACTION_TYPE_CHOICES = (
    (INCOME, "Income"),
    (EXPENSE, "Expense"),
)
