"""FastAPI Application lives here."""
import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .meal_planner_agent import MealPlannerAgent, MealPlanResponse, UserRequest

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


# Serve index.html at /
@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/meal-plan", response_model=MealPlanResponse)
def meal_planner(user_request: UserRequest) -> MealPlanResponse:
    """Generate a meal plan based on user request."""
    #     sample_meal_plan_response = MealPlanResponse(
    #     meals=[
    #         MealsForADay(
    #             day="Day 1",
    #             breakfast=Meal(
    #                 name="Vegetable Upma",
    #                 ingredients=["Semolina", "Mixed vegetables", "Onion", "Mustard seeds", "Curry leaves", "Salt", "Oil"],
    #                 instructions="Roast semolina, sauté vegetables and spices, add water and cook until fluffy.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #             lunch=Meal(
    #                 name="Paneer Tikka Masala",
    #                 ingredients=["Paneer", "Tomato", "Onion", "Spices", "Cream"],
    #                 instructions="Grill paneer, prepare masala gravy, combine and simmer.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #             dinner=Meal(
    #                 name="Dal Khichdi",
    #                 ingredients=["Rice", "Lentils", "Turmeric", "Cumin", "Ghee", "Salt"],
    #                 instructions="Cook rice and lentils with spices until soft. Temper with cumin and ghee.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #         ),
    #         MealsForADay(
    #             day="Day 2",
    #             breakfast=Meal(
    #                 name="Poha",
    #                 ingredients=["Flattened rice", "Onion", "Peanuts", "Mustard seeds", "Curry leaves", "Turmeric", "Salt"],
    #                 instructions="Sauté onions and spices, add soaked poha, cook and garnish with peanuts.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #             lunch=Meal(
    #                 name="Chole Bhature",
    #                 ingredients=["Chickpeas", "Tomato", "Onion", "Spices", "Flour", "Yogurt"],
    #                 instructions="Cook chickpeas in spicy gravy. Prepare and fry bhature dough.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #             dinner=Meal(
    #                 name="Vegetable Pulao",
    #                 ingredients=["Rice", "Mixed vegetables", "Spices", "Ghee", "Salt"],
    #                 instructions="Sauté vegetables and spices, add rice and cook together.",
    #                 dietary_restrictions="Vegetarian"
    #             ),
    #         ),
    #     ],
    #     additional_notes="Sample meal plan for 2 days. Adjust portion sizes as needed."
    # )

    #     return sample_meal_plan_response

    logger.info("Received user request for meal plan: %s", user_request)
    agent = MealPlannerAgent()
    user_preferences = agent.get_user_meal_preferences(user_request)

    logger.info("User meal preferences: %s", user_preferences)
    if not user_preferences.should_process_request:
        return MealPlanResponse(
            meals=[], additional_notes="No meal plan generated due to user preferences."
        )

    meal_plan_response = agent.generate_meal_plan(user_preferences, user_request)

    logger.info("Generated meal plan response: %s", meal_plan_response)
    if not meal_plan_response.meals:
        return MealPlanResponse(
            meals=[],
            additional_notes="No meals generated based on the provided preferences.",
        )

    return meal_plan_response
