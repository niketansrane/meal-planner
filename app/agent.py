import os
from textwrap import dedent

from config import Config
from openai import AzureOpenAI


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

    def generate_meal_plan(self):
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": dedent(self.meal_plan_system_prompt),
                },
                {
                    "role": "user",
                    "content": dedent(
                        """
                                Generate a meal plan for a week with a focus on healthy eating.
                                Include breakfast, lunch, and dinner for each day. The plan should be balanced and include a variety of foods.
                                """
                    ),
                },
            ],
            max_completion_tokens=100000,
            model=Config.AZURE_DEPLOYMENT,
        )
        llm_response = response.choices[0].message.content
        return llm_response


agent = MealPlannerAgent()
print(agent.generate_meal_plan())
