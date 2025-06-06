import os
from textwrap import dedent

from openai import AzureOpenAI

from .config import Config
from .models import (
    MealPlanResponse,
    UserMealPreferences,
    UserRequest,
    UserRequestIntent,
)


class MealPlannerAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version=Config.AZURE_API_VERSION,
            azure_endpoint=Config.AZURE_ENDPOINT,
            api_key=Config.AZURE_SUBSCRIPTION_KEY,
        )
        self.meal_plan_system_prompt = self.get_meal_plan_system_prompt()

    def get_meal_plan_system_prompt(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "prompts", "meal-plan.txt"), "r") as file:
            return file.read()

    def generate_meal_plan(
        self, user_meal_preferences: UserMealPreferences, user_request: UserRequest
    ) -> MealPlanResponse:
        if not user_meal_preferences.should_process_request:
            return MealPlanResponse(
                meals=[],
                additional_notes="Request is not valid or should not be processed.",
            )
        # Prepare the system prompt with user meal preferences
        system_prompt = (
            user_request.system_prompt
            if user_request.system_prompt
            else self.meal_plan_system_prompt
        )
        user_prompt = (
            user_request.user_prompt
            if user_request.user_prompt
            else "Generate a meal plan for a week."
        )

        response = self.client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": dedent(system_prompt),
                },
                {
                    "role": "user",
                    "content": dedent(user_prompt),
                },
                {
                    "role": "assistant",
                    "content": dedent(
                        f"""Generate a meal plan for with the following preferences:
                                        {user_meal_preferences.model_dump_json(indent=2)}
                                        Please ensure the meal plan is balanced, nutritious, and adheres to the specified dietary restrictions.
                                        """
                    ),
                },
            ],
            model=Config.AZURE_DEPLOYMENT,
            response_format=MealPlanResponse,
        )
        meal_plan = response.choices[0].message.parsed
        return meal_plan

    def get_user_meal_preferences(self, user_request: UserRequest) -> UserRequestIntent:
        response = self.client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": dedent(
                        """
                                      You are a highly skilled nutritionist with extensive knowledge in creating personalized meal plans
                                      that cater to individual dietary preferences and cultural cuisines.
                                      Your expertise includes designing balanced and flavorful meals suitable for a variety of dietary choices
                                      such as vegetarian, vegan, egg-based, and non-vegetarian, with an emphasis on Indian cuisine.
                                      Your task is to generate user meal preferences based on their specific input.
                                      """
                    ),
                },
                {
                    "role": "user",
                    "content": dedent(
                        f"""User Request: {user_request.user_prompt}, System Prompt: {user_request.system_prompt}
                                    Please provide the user's meal preferences in a structured format."""
                    ),
                },
            ],
            model=Config.AZURE_DEPLOYMENT,
            response_format=UserRequestIntent,
        )
        user_meal_preferences = response.choices[0].message.parsed
        return user_meal_preferences


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "prompts", "meal-plan.txt"), "r") as file:
        system_prompt = file.read()
    user_request = UserRequest(
        system_prompt=system_prompt,
        user_prompt="I need a meal plan for a week with non vegetarian maharashtrian options. I am allergic to cheese.",
    )
    agent = MealPlannerAgent()
    user_meal_preference = agent.get_user_meal_preferences(user_request)
    if not user_meal_preference.should_process_request:
        print("Request is not valid or should not be processed.")
    else:
        meal_plan = agent.generate_meal_plan(user_meal_preference, user_request)
        print("Generated Meal Plan:")
        print(meal_plan)
        print("User Meal Preferences:")
        print(user_meal_preference.model_dump_json(indent=2))
