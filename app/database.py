from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.config import Config
from app.models import MealPlanResponse


class Database:
    """
    Initialize the MongoDB client and test the connection.
    """

    def __init__(self, connection_string: str):
        """
        Initialize the MongoDB client and test the connection.
        """
        self.client = MongoClient(
            connection_string,
            server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
        )

    def get_or_create_database(self, db_name: str):
        """
        Get or create a MongoDB database.

        :param db_name: Name of the database to get or create.
        :return: The MongoDB database object.
        """
        return self.client[db_name]

    def get_or_create_collection(self, db_name: str, collection_name: str):
        """
        Get or create a MongoDB collection.

        :param db_name: Name of the database.
        :param collection_name: Name of the collection to get or create.
        :return: The MongoDB collection object.
        """
        db = self.get_or_create_database(db_name)
        return db[collection_name]

    def add_document(self, db_name: str, collection_name: str, document: dict):
        """
        Add a document to a MongoDB collection.

        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        :param document: The document to add.
        :return: The result of the insert operation.
        """
        collection = self.get_or_create_collection(db_name, collection_name)
        return collection.insert_one(document)

    def find_documents(self, db_name: str, collection_name: str, query: dict):
        """
        Find documents in a MongoDB collection.

        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        :param query: The query to filter documents.
        :return: A cursor to the found documents.
        """
        collection = self.get_or_create_collection(db_name, collection_name)
        return collection.find(query)


class MealsPlannerDatabase(Database):
    """
    Meals database class to handle meals-related operations.
    """

    def __init__(self, connection_string: str, db_name: str = "meals_planner"):
        """
        Initialize the MealsDatabase with a specific database name.
        """
        super().__init__(connection_string)
        self.db_name = db_name

    def get_meals_collection(self):
        """
        Get the meals collection.
        """
        return self.get_or_create_collection(self.db_name, "meals")

    def add_meal_plan_for_user(self, user_id: str, meal_plan: MealPlanResponse):
        """
        Add a meal plan for a user.

        :param user_id: The ID of the user.
        :param meal_plan: The meal plan to add.
        :return: The result of the insert operation.
        """
        collection = self.get_meals_collection()
        document = {
            "user_id": user_id,
            "meal_plan": meal_plan.model_dump_json(),
        }
        return collection.insert_one(document)

    def get_meal_plan_for_user(self, user_id: str):
        """
        Get the meal plan for a user.

        :param user_id: The ID of the user.
        :return: The meal plan for the user, or None if not found.
        """
        collection = self.get_meals_collection()
        result = collection.find_one({"user_id": user_id})
        return result.get("meal_plan") if result else None


if __name__ == "__main__":
    # Example usage
    config = Config()
    db = MealsPlannerDatabase(connection_string=config.MONGODB_CONNECTION_STRING)

    # Add a meal plan for a user
    user_id = "user123"
    meal_plan = {
        "breakfast": "Oatmeal with fruits",
        "lunch": "Grilled chicken salad",
        "dinner": "Steamed vegetables and fish",
    }
    db.add_meal_plan_for_user(user_id, meal_plan)

    # Retrieve the meal plan for the user
    retrieved_plan = db.get_meal_plan_for_user(user_id)
    print(f"Meal plan for {user_id}: {retrieved_plan}")
