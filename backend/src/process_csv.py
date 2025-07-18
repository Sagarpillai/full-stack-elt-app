import pandas as pd
from sqlalchemy import create_engine, text
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv_to_postgres(csv_path: str, db_config: dict):
    db_url = (f"postgresql://{db_config['user']}:{db_config['password']}"
              f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    engine = create_engine(db_url)
    table_name = Path(csv_path).stem.lower()
    file_name = Path(csv_path).name

    status = "Failed"
    rows_loaded = 0

    try:
        logging.info(f"Reading CSV file: {csv_path}")
        df = pd.read_csv(csv_path)
        rows_loaded = len(df)

        logging.info(f"Loading data into table '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        status = "Success"
        success_message = f"Successfully loaded {rows_loaded} rows into '{table_name}'."
        logging.info(success_message)
        return {"status": status, "message": success_message, "rows_loaded": rows_loaded}

    except Exception as e:
        error_message = f"An error occurred: {e}"
        logging.error(error_message)
        return {"status": status, "message": error_message, "rows_loaded": rows_loaded}

    finally:
        # This block will run whether the job succeeds or fails
        logging.info(f"Logging job status to job_history table.")
        with engine.connect() as connection:
            # Use a text() object for the SQL statement to prevent SQL injection warnings
            log_query = text(
                "INSERT INTO job_history (file_name, status, rows_loaded) "
                "VALUES (:file, :status, :rows)"
            )
            connection.execute(log_query, {"file": file_name, "status": status, "rows": rows_loaded})
            connection.commit()