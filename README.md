# DevOps Group Project - Flask Web Application

CSD-4503 Group Project for deploying a Flask web app with CI/CD pipeline to Azure VM.

## Team Members
- Onyeka
- Ajit
- Justin

## What This Project Does

This is a simple Flask web application that we're deploying using Docker and CI/CD practices. The app has a homepage and a health check endpoint that returns the app status.

## Project Structure

.
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Homepage template
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── requirements.txt       # Python dependencies
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions pipeline
└── tests/
    └── test_app.py       # Unit tests


## Running the App Locally

1. Install dependencies:
bash
pip install -r requirements.txt


2. Run the Flask app:
bash
python app.py


3. Open your browser and go to http://localhost:5000

## Running with Docker

Build and run the container:
bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app


Or use Docker Compose:
bash
docker-compose up


## Testing

Run the tests:
bash
pytest test_app.py


## Deployment

The app automatically deploys to our Azure VM when changes are pushed to the main branch. The GitHub Actions workflow handles:
- Running tests
- Building Docker image
- Pushing to Docker Hub
- Deploying to Azure VM

## Technologies Used

- Flask (Python web framework)
- Docker (containerization)
- GitHub Actions (CI/CD)
- Azure VM (deployment)
- pytest (testing)

## Course Information

*Course:* CSD-4503 - DevOps  
*Institution:* Lambton College  
*Semester:* Fall 2025
