Smart Content Moderator API

Project Overview

This project is a take-home assignment to build a robust content moderation service using modern backend technologies. The service analyzes user-submitted content (text and images) for inappropriate material using a Large Language Model (LLM), stores the moderation results in a database, and provides an API for retrieving analytics. The architecture is built for scalability and maintainability, leveraging Docker for containerization and asynchronous task processing for efficiency.

Core Features

    RESTful API: Implemented with FastAPI for high performance and automatic documentation.

    AI Integration: Uses the Google Gemini API for content classification (toxic, spam, harassment, safe).

    Asynchronous Processing: Utilizes a Celery worker with Redis as a message broker to handle I/O-bound tasks like image moderation in the background.

    Database Management: Stores all moderation requests and results in a PostgreSQL database.

    Containerization: The entire application is containerized using Docker, with services orchestrated by Docker Compose.

    Data Validation: All incoming API requests are validated using Pydantic models.

API Endpoints

The following RESTful API endpoints are implemented:
Method	Endpoint	Description
POST	/api/v1/moderate/text	Submits text for moderation. Returns immediately.
POST	/api/v1/moderate/image	Submits an image URL for moderation asynchronously.
GET	/api/v1/analytics/summary	Retrieves a summary of moderation activity by user.

Project Structure

smart-content-moderator/
├── app/
│   ├── db/
│   │   ├── database.py       # DB connection setup
│   │   └── models.py         # SQLAlchemy ORM models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py            # Gemini API integration
│   │   └── notifications.py  # Email/Slack notification service
│   ├── tasks/
│   │   └── image_moderation.py # Celery background task
│   └── main.py                 # FastAPI application and endpoints
├── docker-compose.yml          # Defines all Docker services
├── Dockerfile                  # Builds the application image
└── requirements.txt            # Python dependencies

Setup and Installation

Prerequisites

    Docker and Docker Compose installed on your system.

    A Gemini API Key from Google AI Studio.

Steps

    Clone the repository:
    Bash

git clone https://github.com/your-username/your-repo-name.git
cd smart-content-moderator

Create a .env file:
Create a .env file in the project's root directory and add your Gemini API key. This is a secure way to manage secrets.
Bash

LLM_API_KEY=your_gemini_api_key

Replace your_gemini_api_key with your actual key.

Build and run the containers:
Use docker-compose to build the application image and start all the services (FastAPI, PostgreSQL, Redis, Celery worker).
Bash

    docker-compose up --build

    Access the API:
    Once the services are running, open your web browser and navigate to the interactive API documentation.
    http://localhost:8000/docs

Evaluation Notes

    Architecture: The project follows a modular, microservice-like architecture with a clear separation of concerns (API, database, tasks, services).

    Async/Await: FastAPI and Celery are used to handle synchronous and asynchronous tasks efficiently.

    Docker: The multi-stage Dockerfile ensures a small production image, and docker-compose simplifies the entire setup.

Challenges and Assumptions

    LLM Parsing: The parsing of the LLM's raw response to a structured JSON object (classification, confidence, reasoning) requires careful prompt engineering. The current implementation uses placeholders for this logic.

    Notification Service: A simple placeholder function for notifications is provided. In a real-world scenario, this would be replaced with a robust third-party API integration (e.g., BrevoMail, Slack).

    Sentry Integration: The bonus requirement for Sentry integration was not implemented in this version to focus on the core functionality. It can be added by installing the Sentry SDK and configuring it in the application's main file.
