"""FastAPI Application lives here."""

import logging
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import Config
from app.database import MealsPlannerDatabase
from app.meal_planner_agent import MealPlannerAgent, MealPlanResponse, UserRequest

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_homepage():
    return FileResponse(os.path.join("static", "index.html"))


@app.post("/api/meal-plan", response_model=MealPlanResponse)
def meal_planner(user_request: UserRequest) -> MealPlanResponse:
    """Generate a meal plan based on user request."""
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

    meal_planer_db = MealsPlannerDatabase(
        connection_string=Config.MONGODB_CONNECTION_STRING
    )
    # Generate random user ID for demonstration purposes
    user_id = "random_user_id_12345"
    meal_planer_db.add_meal_plan_for_user(user_id, meal_plan_response)
    logger.info("Meal plan saved to database for user ID: %s", user_id)
    return meal_plan_response
