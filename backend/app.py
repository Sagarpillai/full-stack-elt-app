from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import yaml
from src.main import run_job

# Initialize Flask App
app = Flask(__name__)
CORS(app)

def get_db_engine():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    db_config = config['target']
    db_url = (f"postgresql://{db_config['user']}:{db_config['password']}"
              f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    return create_engine(db_url)

@app.route('/')
def index():
    return "<h1>ELT Backend API is Running</h1>"

@app.route('/api/trigger', methods=['POST'])
def trigger_job():
    print("API call received. Triggering ELT job...")
    result = run_job()
    return jsonify(result)

@app.route('/api/history', methods=['GET'])
def get_history():
    engine = get_db_engine()
    with engine.connect() as connection:
        query = text("SELECT * FROM job_history ORDER BY timestamp DESC LIMIT 20")
        result = connection.execute(query)
        history = [dict(row._mapping) for row in result]
        return jsonify(history)

@app.route('/api/table/<table_name>', methods=['GET'])
def view_table(table_name):
    """API endpoint to view the contents of any table."""
    # Basic protection against SQL injection on table names
    if not table_name.isalnum():
        return jsonify({"error": "Invalid table name"}), 400
        
    engine = get_db_engine()
    try:
        with engine.connect() as connection:
            query = text(f"SELECT * FROM {table_name} LIMIT 100")
            result = connection.execute(query)
            data = [dict(row._mapping) for row in result]
            return jsonify(data)
    except Exception as e:
        error_message = f"Error fetching data for table '{table_name}': {e}"
        print(error_message)
        return jsonify({"error": error_message}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)