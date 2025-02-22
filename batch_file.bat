call venv\Scripts\activate.bat
python scripts/data_collector.py
python scripts/model_trainer.py
python scripts/carbon_calculator.py
python app/app.py
python scripts/esg_reporter.py 