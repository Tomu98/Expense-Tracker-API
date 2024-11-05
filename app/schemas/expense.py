from pydantic import BaseModel, Field, field_validator
from datetime import date as DateType


ALLOWED_CATEGORIES = ["Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"]


class AddExpense(BaseModel):
    amount: float = Field(
        title="Amount",
        description="The amount of money allocated to this expense.",
        gt=0
    )
    category: str = Field(
        title="Category",
        description="The category to which this expense belongs. Can be one of the following: 'Groceries', 'Leisure', 'Electronics', 'Utilities', 'Clothing', 'Health', 'Others'.",
        max_length=50
    )
    description: str = Field(
        title="Description",
        description="A brief description of the expense.",
        max_length=200,
        default=None
    )
    date: DateType = Field(
        default_factory=DateType.today,
        title="Date",
        description="Date on which the expense was incurred in 'YYYY-MM-DD' format."
    )

    # Check category validator
    @field_validator("category")
    def check_category(cls, value):
        value = value.title()
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(F"Invalid category. Allowed categories are: {', '.join(ALLOWED_CATEGORIES)}")
        return value



class UpdateExpense(BaseModel):
    amount: float = Field(
        title="Amount",
        description="The new amount for the expense.",
        gt=0,
        default=None
    )
    category: str = Field(
        title="Category",
        description="The new category for the expense. Can be one of the following: 'Groceries', 'Leisure', 'Electronics', 'Utilities', 'Clothing', 'Health', 'Others'.",
        max_length=50,
        default=None
    )
    description: str = Field(
        title="Description",
        description="A new brief description of the expense.",
        max_length=200,
        default=None
    )
    date: DateType = Field(
        title="Date",
        description="The new date for the expense in 'YYYY-MM-DD' format.",
        default=None
    )

    # Check category validator
    @field_validator("category")
    def check_category(cls, value):
        if value is None:
            return value

        value = value.title()
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(f"Invalid category. Allowed categories are: {', '.join(ALLOWED_CATEGORIES)}")
        return value
