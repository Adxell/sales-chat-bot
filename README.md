# Sales Training Chat Bot: Empowering Students to Sell and Acquire Clients

This project is a Sales Training Chat Bot built using FastAPI, Slack, and Gemini. It is designed to help students learn and practice sales techniques, improve their communication skills, and acquire more clients effectively. The bot leverages the power of the Gemini language model to simulate real-world sales scenarios and provide intelligent feedback.

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- ngrok
- FastAPI
- Uvicorn
- Gemini API Key (for integrating the Gemini language model)s

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Adxell/sales-chat-bot.git
   cd sales-chat-bot
2. **Environment Variables:**:

    Create a `.env` file in the root of your project:
   ```bash
    DATABASE_PORT=your-db-port
    POSTGRES_PASSWORD=your-db-password
    POSTGRES_USER=your-db-user
    POSTGRES_DB=your-db-name
    POSTGRES_HOST=your-db-host
    SLACK_SIGNING_SECRET=your-slack-signing-secret
    GEMINI_API_KEY=your-gemini-secret
3. **Docker Setup:**

    Build and run the Docker containers:
   ```bash
    docker-compose -f docker/db.yaml up --build
4. **Run SQL Tables:**

    After the PostgreSQL container is running, execute the SQL script to create the necessary tables. Connect to the database and run the following commands:
   ```bash
    docker exec -it postgres_db psql -U user -d chatdb
   ``` 
    **Run sql file**
5. **Run FastAPI Application:**

    For development, run the FastAPI app with:
   ```bash
    uvicorn main:app --reload
6. **Expose with ngrok:**

   ```bash
    ngrok http 8000
    ```
    Use the provided https URL for Slack app configuration.
7. **Configure Slack App:**

    * Enable Event Subscriptions and set the Request URL to your ngrok URL.

    * Subscribe to bot events and set the necessary OAuth scopes.

## Testing
Once everything is set up, interact with your Slack bot to test the integration.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License

[MIT](https://choosealicense.com/licenses/mit/)


This documentation provides a comprehensive guide to setting up your project and includes all necessary steps from environment setup to testing. Adjust the placeholders and URLs as per your actual project details.
