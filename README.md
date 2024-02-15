# News Article Classifier and Database

This project is aimed at creating a News Article Classifier using Python. The system enables users to input a news article either as text or URL, identifies its category (e.g., Politics, Sports, Technology), and stores this information in a MongoDB database. Additionally, it provides a REST API for users to submit articles and retrieve articles based on specific categories.

## Project Structure

- `app.py`: Python script containing the Flask application for the REST API.
- `model/`: Directory containing the trained machine learning model.
- `data/`: Directory containing the dataset used for training the model.
- `templates/`: Directory containing HTML templates for user interface rendering.
- `requirements.txt`: File listing all dependencies required for the project.

## Setup Instructions

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Make sure you have MongoDB installed and running on your system.
4. Set up the MongoDB URI in the `app.py` script.
5. Run the Flask application by executing `python app.py`.
6. Access the application through a web browser or use the provided REST API endpoints.

## User Interface

- Users can access the web interface by navigating to the root URL.
- They can input a news article either as text or URL and receive the predicted category.

## REST API Endpoints

1. **Predict Category Endpoint**
   - **URL:** `/api/classify`
   - **Method:** POST
   - **Request Body:** JSON object containing either the text or URL of the news article.
   - **Response:** JSON object containing the predicted category.

2. **Retrieve Articles by Category Endpoint**
   - **URL:** `/api/articles/<category>`
   - **Method:** GET
   - **Path Parameter:** Category (e.g., politics, sports)
   - **Response:** JSON object containing all articles of the specified category stored in the MongoDB database.

## MongoDB Integration

- The application uses MongoDB to store processed articles, including their input source, predicted categories, and timestamps.

## Images of Output
![image](https://github.com/pvchaitanya8/News-Classifier/assets/93573686/f2acd24b-e908-4981-9a28-785bd6fbae6c)
![image](https://github.com/pvchaitanya8/News-Classifier/assets/93573686/127207cf-2736-4188-9c9c-6e814336029c)

