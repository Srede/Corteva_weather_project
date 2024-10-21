from flask import Flask, jsonify, request
from flask_restx import Api, Resource, Namespace, fields
from sqlalchemy import create_engine, text
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)

# Initialize SQLAlchemy engine for PostgreSQL
engine = create_engine('postgresql://postgres:corteva@localhost:5432/weather_data')

# Initialize Flask-RESTX API with Swagger UI
api = Api(app, doc='/swagger/', title="Weather Data API", description="API for retrieving weather data and statistics")

# Define a custom namespace for Suprith's implementation
suprith_ns = Namespace('Suprith\'s Implementation', description='Custom implementation by Suprith')

# Model for weather data (for Swagger documentation)
weather_model = suprith_ns.model('Weather', {
    'station_id': fields.String(description='Weather station ID', required=True),
    'date': fields.String(description='Date in YYYY-MM-DD format', required=True),
    'max_temp': fields.Float(description='Maximum temperature (Celsius)', required=True),
    'min_temp': fields.Float(description='Minimum temperature (Celsius)', required=True),
    'precipitation': fields.Float(description='Precipitation (cm)', required=True),
})

# Function to handle Decimal conversion
def decimal_to_float(data):
    if isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data

# Pagination utility function
def paginate(query, page, per_page):
    offset = (page - 1) * per_page
    query += f" LIMIT {per_page} OFFSET {offset}"
    return query

# Endpoint: /api/weather
@suprith_ns.route('/weather')
class Weather(Resource):
    @suprith_ns.marshal_list_with(weather_model)
    def get(self):
        """Retrieve weather data with optional filtering and pagination"""
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Base query
        query = "SELECT * FROM weather_data WHERE 1=1"
        params = {}

        # Add filtering logic
        if station_id:
            query += " AND station_id = :station_id"
            params['station_id'] = station_id
        
        if date:
            query += " AND date = :date"
            params['date'] = date

        # Apply pagination
        query = paginate(query, page, per_page)

        # Execute query with filters and pagination
        with engine.connect() as conn:
            result = conn.execute(text(query), params).mappings().all()

        # Convert RowMapping objects to dictionaries
        result_dicts = [dict(row) for row in result]

        # Convert Decimals to floats
        result_dicts = decimal_to_float(result_dicts)

        return result_dicts, 200

# Endpoint: /api/weather/stats
@suprith_ns.route('/weather/stats')
class WeatherStats(Resource):
    def get(self):
        """Retrieve weather statistics with optional filtering and pagination"""
        station_id = request.args.get('station_id')
        year = request.args.get('year')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Base query
        query = """
            SELECT station_id, EXTRACT(YEAR FROM date) as year, AVG(max_temp) as avg_max_temp, 
                   AVG(min_temp) as avg_min_temp, SUM(precipitation) as total_precipitation
            FROM weather_data
            WHERE 1=1
        """
        params = {}

        # Add filtering logic
        if station_id:
            query += " AND station_id = :station_id"
            params['station_id'] = station_id

        if year:
            query += " AND EXTRACT(YEAR FROM date) = :year"
            params['year'] = year

        query += " GROUP BY station_id, year"

        # Apply pagination
        query = paginate(query, page, per_page)

        # Execute query with filters and pagination
        with engine.connect() as conn:
            result = conn.execute(text(query), params).mappings().all()

        # Convert RowMapping objects to dictionaries
        result_dicts = [dict(row) for row in result]

        # Convert Decimals to floats
        result_dicts = decimal_to_float(result_dicts)

        return result_dicts, 200

# Add the custom namespace to the API
api.add_namespace(suprith_ns, path='/api')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
