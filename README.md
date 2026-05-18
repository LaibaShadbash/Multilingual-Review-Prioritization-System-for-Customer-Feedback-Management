#A Hybrid Multilingual Toxicity Detection and Review-Prioritization System

## Setup Instructions
1. Clone this repository.
2. Recreate the virtual environment: `python -m venv .venv` and run `pip install -r requirements.txt`.
3. **Note on the Model:** Due to file size limitations on GitHub, the fine-tuned `final_urgency_model` folder must be placed manually inside a directory named `models/` in the project root before launching `dashboard.py`.
4. to run the Flask application: `python app.py`
5. to run the Streamlit dashboard: `streamlit run dashboard.py`