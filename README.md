# Meal Planner

A personalized meal planning application powered by Azure OpenAI that generates weekly meal plans based on dietary preferences and cuisine choices.

## Tech Stack

- **Backend**: Python 3.12 with FastAPI
- **AI Integration**: Azure OpenAI API
- **Frontend**: HTML, CSS, JavaScript
- **Data Validation**: Pydantic
- **Containerization**: Docker

## Features

- Generate personalized weekly meal plans
- Support for various dietary preferences (vegetarian, vegan, etc.)
- Cuisine type selection
- Detailed meal information including ingredients and cooking instructions
- Responsive web interface with a calendar-style meal planner
- Custom system and user prompts for fine-tuning meal generation

## Project Structure

```
meal-planner/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── meal_planner_agent.py # Agent for Azure OpenAI integration
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   └── prompts/             # System prompts for the AI
│       └── meal-plan.txt    # Default system prompt for meal planning
├── static/
│   ├── index.html           # Frontend interface
│   └── js/
│       └── mealplanner.js   # API calls and UI interactions
├── .env                     # Environment variables (not tracked in git)
├── Dockerfile               # Docker configuration
├── startup.sh               # Script to start the application
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## How It Works

1. Users enter their dietary preferences and cuisine choices through the web interface
2. The FastAPI backend sends the request to the Azure OpenAI API via the MealPlannerAgent
3. The AI generates a personalized meal plan in a structured format
4. The meal plan is displayed in a calendar-style interface on the web frontend
5. Users can click on meals to view detailed information including ingredients and cooking instructions

## Setup Instructions

### Prerequisites

- Python 3.12+
- Azure OpenAI API access (endpoint and key)
- Docker (optional, for containerized deployment)

### Installation

#### Option 1: Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/meal-planner.git
   cd meal-planner
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Azure OpenAI API credentials:
   ```
   AZURE_ENDPOINT=your-azure-endpoint
   AZURE_SUBSCRIPTION_KEY=your-subscription-key
   AZURE_API_VERSION=2023-05-15
   AZURE_DEPLOYMENT=your-deployment-name
   ```

4. Run the application using one of the following methods:
   
   **Using uvicorn directly:**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   **Using the startup script:**
   ```bash
   chmod +x startup.sh
   ./startup.sh
   ```

#### Option 2: Docker Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/meal-planner.git
   cd meal-planner
   ```

2. Create a `.env` file with your Azure OpenAI API credentials as described above.

3. Build and run the Docker container:
   ```bash
   docker build -t meal-planner .
   docker run -p 8000:80 --env-file .env meal-planner
   ```

5. Open your browser and navigate to:
   - When running locally: `http://localhost:8000`
   - When using Docker: `http://localhost:8000` (or whatever port you mapped in the Docker run command)

## Usage

1. Open the web interface in your browser
2. Enter your meal preferences in the User Prompt area (e.g., "vegetarian meals with South Indian cuisine")
3. (Optional) Customize the System Prompt for more specific instructions
4. Click "Generate" button
5. View your personalized meal plan in the calendar-style interface
6. Click on individual meals to see ingredients and cooking instructions in a popup modal

## Future Enhancements

- User accounts and saved meal plans
- Grocery list generation
- Recipe rating and favorites
- Nutritional information
- Mobile app version
- Support for additional cuisines and dietary preferences

## Troubleshooting

- **Azure OpenAI API Issues**: Ensure your API credentials are correct in the `.env` file and that you have proper access to the Azure OpenAI service.
- **Docker Port Conflicts**: If port 8000 is already in use, you can map to a different port using `-p <host-port>:80` in your Docker run command.
- **Missing Dependencies**: If you encounter errors about missing modules, ensure you've installed all dependencies with `pip install -r requirements.txt`.

## Author

Niketan Rane - &copy; 2025

## License

This project is licensed under the [MIT License](LICENSE).
