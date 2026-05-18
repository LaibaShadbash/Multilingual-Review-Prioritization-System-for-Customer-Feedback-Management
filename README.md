#A Hybrid Multilingual Toxicity Detection and Review-Prioritization System

## Setup Instructions
1. Clone this repository.
2. Recreate the virtual environment: `python -m venv .venv` and run `pip install -r requirements.txt`.
3. **Note on the Model:** Due to GitHub's strict 100MB file size limitations, the fine-tuned DistilBERT transformer weights could not be pushed to this repository. 

    Google Colab link for the trained model: **https://colab.research.google.com/drive/1KpPjOj4f6q5sN_-VtSBNFADmstRh8Mjs?usp=sharing**
    
4. to run the Flask application: `python app.py`
5. to run the Streamlit dashboard: `streamlit run dashboard.py`
