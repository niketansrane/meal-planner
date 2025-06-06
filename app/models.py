from pydantic import BaseModel, Field


class UserMealPreferences(BaseModel):
    dietary_restrictions: str = Field(
        default="vegetarian",
        description="Any dietary restrictions or preferences the user has, e.g., vegetarian, vegan, gluten-free.",
    )
    meal_type: str = Field(
        default="full day",
        description="Type of meal plan requested, e.g., breakfast, lunch, dinner, or full day.",
    )
    number_of_days: int = Field(
        default=7,
        description="Number of days for which the meal plan is requested.",
    )
    cuisine_type: str = Field(
        default="North Indian",
        description="Preferred cuisine type for the meal plan, e.g., Italian, Mexican, Asian.",
    )


class UserRequestIntent(BaseModel):
    intent: str = Field(
        default="meal_plan",
        description="The intent of the user's request, e.g., meal_plan, recipe_suggestion.",
    )

    is_request_security_risk: bool = Field(
        default=False,
        description="Indicates if the request is considered a security risk.",
    )

    is_request_meal_related: bool = Field(
        default=True,
        description="Indicates if the request is related to meal planning or dietary preferences.",
    )
    should_process_request: bool = Field(
        default=True,
        description="Indicates if the request should be processed by the agent.",
    )

    user_meal_preferences: UserMealPreferences = Field(
        default=None,
        description="User's meal preferences including dietary restrictions, meal type, number of days, and cuisine type.",
    )


class UserRequest(BaseModel):
    system_prompt: str = Field(
        default="",
        description="System prompt to guide the agent's behavior and responses.",
    )
    user_prompt: str = Field(
        default="",
        description="User's request or question that the agent needs to respond to.",
    )


class Meal(BaseModel):
    name: str = Field(
        default="",
        description="Name of the meal, e.g., 'Vegetable Biryani'.",
    )
    ingredients: list[str] = Field(
        default=[],
        description="List of ingredients required for the meal.",
    )
    instructions: str = Field(
        default="",
        description="Cooking instructions for preparing the meal.",
    )
    dietary_restrictions: str = Field(
        default="",
        description="Any dietary restrictions or preferences applicable to the meal.",
    )


class MealsForADay(BaseModel):
    day: str = Field(
        default="",
        description="Day of the week for which the meals are planned, e.g., 'Monday'.",
    )
    breakfast: Meal = Field(
        default_factory=Meal,
        description="Breakfast meal details.",
    )
    lunch: Meal = Field(
        default_factory=Meal,
        description="Lunch meal details.",
    )
    dinner: Meal = Field(
        default_factory=Meal,
        description="Dinner meal details.",
    )


class MealPlanResponse(BaseModel):
    meals: list[MealsForADay] = Field(
        default=[],
        description="List of meals for the meal plan, including breakfast, lunch, and dinner for each day.",
    )
    additional_notes: str = Field(
        default="",
        description="Any additional notes or instructions for the meal plan.",
    )
