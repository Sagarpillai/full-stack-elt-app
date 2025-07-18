import yaml
from pathlib import Path
from sqlalchemy import create_engine, text
from .process_csv import load_csv_to_postgres

def get_db_engine():
    """Reads config and returns a new SQLAlchemy engine."""
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    db_config = config['target']
    db_url = (f"postgresql://{db_config['user']}:{db_config['password']}"
              f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    return create_engine(db_url)

def run_job():
    """
    Finds all new CSV files and processes them, returning a summary.
    """
    try:
        engine = get_db_engine()
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        source_dir = Path(config['source']['path'])
        db_config = config['target']

        with engine.connect() as connection:
            query = text("SELECT file_name FROM job_history WHERE status = 'Success'")
            result = connection.execute(query)
            processed_files = {row[0] for row in result}

        all_csv_files = {p.name for p in source_dir.glob('*.csv')}
        files_to_process = all_csv_files - processed_files

        if not files_to_process:
            message = "No new files to process."
            print(message)
            return {"status": "Complete", "message": message, "details": []}

        # Collect the result of each job
        job_results = []
        for file_name in sorted(list(files_to_process)):
            file_path = source_dir / file_name
            print(f"--- Processing new file: {file_name} ---")
            result = load_csv_to_postgres(str(file_path), db_config)
            job_results.append(result)

        # Return a summary message along with the detailed results
        summary_message = f"Job finished. Processed {len(job_results)} new file(s)."
        return {"status": "Complete", "message": summary_message, "details": job_results}

    except Exception as e:
        error_msg = f"An unexpected error occurred in main: {e}"
        print(error_msg)
        return {"status": "Error", "message": error_msg}