from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date as DateType


class AddExpense(BaseModel):
    amount: float = Field(
        title="Amount",
        description="The amount of money allocated to this expense.",
        gt=0
    )
    category: str = Field(
        title="Category",
        description="The category to which this expense belongs.",
        max_length=50
    )
    description: str = Field(
        title="Description",
        description="A brief description of the expense.",
        max_length=200,
        default=None
    )
    date: DateType = Field(
        title="Date",
        description="Date on which the expense was incurred in 'DD-MM-YYYY' format."
    )

    # Date format validator
    @field_validator("date")
    def validate_date_format(cls, value):
        try:
            return datetime.strptime(value.strftime("%d-%m-%Y"), "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("The date format should be 'DD-MM-YYYY'")



class UpdateExpense(BaseModel):
    amount: float = Field(
        title="Amount",
        description="The new amount for the expense.",
        gt=0,
        default=None
    )
    category: str = Field(
        title="Category",
        description="The new category for the expense.",
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
        description="The new date for the expense in 'DD-MM-YYYY' format.",
        default=None
    )

    # Date format validator
    @field_validator("date")
    def validate_date_format(cls, value):
        try:
            return datetime.strptime(value.strftime("%d-%m-%Y"), "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("The date format should be 'DD-MM-YYYY'")
