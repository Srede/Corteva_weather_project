# Corteva Weather Project 🌦️

This project involves designing, building, and deploying a **Weather Data Management System** that ingests, stores, analyzes, and exposes weather data through a REST API. It is designed with flexibility and scalability in mind, providing a robust platform for querying weather data and retrieving statistics.

## Project Overview

The project is divided into four main phases:
1. **Data Modeling**: Designing the database schema for storing weather data efficiently.
2. **Data Ingestion**: Ingesting raw weather data from CSV files and storing it in a PostgreSQL database.
3. **Data Analysis**: Running SQL queries and Python scripts to derive useful insights from the data.
4. **REST API Development**: Exposing the ingested and analyzed data through a Flask-based API with Swagger documentation.

---

## Phases of Execution

### Phase 1: Data Modeling  
In this phase, we designed a relational database schema to store the weather data in a **PostgreSQL** database. The database includes a table `weather_data` with the following columns:
- `station_id`: Weather station identifier (string).
- `date`: Date of the weather record (YYYY-MM-DD format).
- `max_temp`: Maximum temperature recorded (in Celsius).
- `min_temp`: Minimum temperature recorded (in Celsius).
- `precipitation`: Total precipitation recorded (in cm).

This schema allows for efficient querying and supports filtering by **station_id** and **date**, which are key to retrieving specific weather records.

#### Key Considerations:
- Ensuring proper data types for each field to maintain data integrity.
- Designing the schema to allow for easy aggregation (such as calculating averages) and filtering.
- Planning for scalability, as large datasets of weather information need to be handled efficiently.

---

### Phase 2: Data Ingestion  
This phase focused on ingesting raw weather data from provided text files in **CSV format**. The ingestion process involved:
1. **Reading data** from text files using **Pandas** and **Python** file handling functions.
2. **Data validation** to ensure records are clean and consistent before being inserted into the database.
3. **Bulk insertions** into the PostgreSQL database using **SQLAlchemy**.

We created a Python script, `ingest.py`, which automates this process, reading multiple files, cleaning the data, and storing it into the `weather_data` table.

#### Ingestion Challenges:
- Handling missing or malformed data.
- Ensuring bulk inserts are done efficiently to avoid performance bottlenecks.
- Using proper error handling to log any failed records.

---

### Phase 3: Data Analysis  
Once the data was stored in the database, we moved to the **data analysis** phase. SQL queries and Python scripts were used to derive insights from the data:
- **Average maximum and minimum temperatures** were calculated over specified periods (e.g., yearly).
- **Total precipitation** was calculated for specific weather stations and time periods.
- **Data filtering** by `station_id` and `date` allows users to extract records for specific stations or dates.

Python and SQLAlchemy were used to run queries against the PostgreSQL database, and the analysis results were made accessible through the API in the next phase.

#### Analysis Challenges:
- Ensuring efficient queries, particularly for large datasets.
- Handling edge cases where data might be missing for certain weather stations or dates.
- Implementing pagination to improve performance when querying large datasets.

---

### Phase 4: REST API Development  
The API is built using **Flask** and **Flask-RESTX** to expose the ingested and analyzed weather data. The API provides two key endpoints:

#### 1. Retrieve Weather Data:
- **Endpoint**: `/api/weather`
- **Method**: `GET`
- **Query Parameters**:
  - `station_id`: Filter data by the weather station (optional).
  - `date`: Filter data by a specific date (optional).
  - `page`: Specify the page of results (for pagination).
  - `per_page`: Specify the number of records per page.
  
This endpoint allows users to retrieve weather data with optional filters and pagination to manage large datasets.

#### 2. Retrieve Weather Statistics:
- **Endpoint**: `/api/weather/stats`
- **Method**: `GET`
- **Query Parameters**:
  - `station_id`: Filter data by weather station (optional).
  - `year`: Filter data by a specific year (optional).
  - `page`: Specify the page of results (for pagination).
  - `per_page`: Specify the number of records per page.

This endpoint provides statistics, including average temperatures and total precipitation, aggregated by `station_id` and year.

#### 3. Swagger Documentation:
The API comes with **Swagger** (via Flask-RESTX) for easy documentation and testing. The Swagger UI is accessible via `/swagger/` and provides an interactive interface for testing the API endpoints.
---
## Technologies Used

### **Languages and Frameworks**:
- **Python**: Core programming language for developing the ingestion scripts and API.
- **Flask**: Lightweight web framework for creating the REST API.
- **Flask-RESTX**: Extended support for REST APIs and Swagger documentation.
- **SQLAlchemy**: ORM used to interact with the PostgreSQL database.
- **PostgreSQL**: Relational database to store weather data.
- **Gunicorn**: A production-ready WSGI server to serve the Flask app in production.
- **Heroku**: Platform for deploying the application.

### **Testing Tools**:
- **pytest**: Unit tests were created to verify the API endpoints, ensuring that the `/api/weather` and `/api/weather/stats` endpoints work as expected under different scenarios.
---

## **Setup and Installation**

Follow these steps to set up and run the project locally.

First, clone the repository from GitHub. After cloning, navigate to the project directory and install the required dependencies.

Ensure that PostgreSQL is installed on your system. Once PostgreSQL is set up, create a database named `weather_db`.

Next, create an `.env` file in the root directory of the project and set the database URL with your PostgreSQL credentials.

To run the application, start the Flask app, and you can access the Swagger documentation by navigating to the provided local URL.

You can also run unit tests to ensure everything is functioning correctly using pytest.

For deployment, push the application to Heroku. Install the Heroku CLI and log in to your Heroku account. Create a new Heroku app and add PostgreSQL as an add-on. Finally, push the code to Heroku.

---

## **Future Improvements**

Some potential areas for improvement include:
- Data Validation Enhancements to handle more complex data integrity checks.
- Additional API endpoints for advanced filtering and statistics, such as monthly averages or station-specific summaries.
- Improved error handling to provide more detailed error responses to users.




