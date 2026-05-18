import streamlit as st
import sqlite3
import pandas as pd
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import urllib.parse

# 1. Load AI Models into Cache
@st.cache_resource
def load_models():
    # Local fine-tuned classification brain
    clf = pipeline("sentiment-analysis", model="./models/final_urgency_model")
    
    # Explicitly load translation components to avoid task string verification bugs
    trans_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
    trans_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
    
    return clf, (trans_model, trans_tokenizer)

classifier, translation_pack = load_models()

# 2. Database Ingestion
conn = sqlite3.connect('reviews.db')
df = pd.read_sql_query("SELECT * FROM reviews", conn)
conn.close() # Safe to close connection now since all data is cached in the DataFrame

# 3. Dynamic Multilingual & Prioritization Processor
def get_priority(row):
    text_to_analyze = row['content']
    
    # Check if string contains Arabic characters (Unicode range tracking)
    is_arabic = any("\u0600" <= char <= "\u06FF" for char in text_to_analyze)
    
    if is_arabic:
        model_ar, tokenizer_ar = translation_pack
        inputs = tokenizer_ar(text_to_analyze, return_tensors="pt")
        generated_tokens = model_ar.generate(**inputs)
        text_to_analyze = tokenizer_ar.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    
    # Run classification evaluation
    result = classifier(text_to_analyze)[0]
    label = result['label'].lower()
    
    # Flags standard label variations (handles 'negative' or default 'label_0')
    if label in ["negative", "label_0"] or row['stars'] <= 2:
        return 1  # High Priority
    return 0  # Normal Priority

# Render UI Layers
if df.empty:
    st.title("Your Pending Reviews")
    st.info("No reviews found in the database! All clear. 🎉")
else:
    # Run prioritization logic across records
    df['priority'] = df.apply(get_priority, axis=1)
    
    # Segregate datasets to eliminate cross-section display duplication
    pending_df = df[df['status'] != 'Resolved'].copy()
    resolved_df = df[df['status'] == 'Resolved'].copy()
    
    # --- SECTION A: ACTIVE PENDING TRIAGE FEED ---
    st.title("Your Pending Reviews")
    
    if pending_df.empty:
        st.info("No pending reviews! All clear.")
    else:
        # Sort pending queue: Urgent alerts jump to the top, then sorts by date
        pending_df = pending_df.sort_values(by=['priority', 'date'], ascending=[False, False])
        
        for idx, row in pending_df.iterrows():
            with st.container():
                st.subheader(f"Rating: {row['stars']} ⭐")
                
                # Format text layout direction dynamically if script matches Arabic script
                is_arabic = any("\u0600" <= char <= "\u06FF" for char in row['content'])
                if is_arabic:
                    st.markdown(f'<div style="text-align: right; direction: rtl; font-size: 18px; margin-bottom: 10px;">{row["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.write(row['content'])
                
                # Show priority flag if review is urgent
                if row['priority'] == 1:
                    st.error("🚨 Urgent Action Needed!")
                
                # Dispatch action anchor button
                safe_suggestion = urllib.parse.quote("Thank you for your feedback!") 
                reply_url = f"http://127.0.0.1:5000/admin/reply/{row['id']}?suggested={safe_suggestion}"
                st.link_button("Reply on Website", reply_url)
                
                st.divider()

    # --- SECTION B: ARCHIVED HISTORY AUDIT LOG ---
    st.write("")
    st.header("✅ Resolved Review History")
    
    if resolved_df.empty:
        st.write("No reviews resolved yet.")
    else:
        # Sort history to reveal newly completed updates first
        resolved_df = resolved_df.sort_values(by=['date'], ascending=False)
        
        for idx, row in resolved_df.iterrows():
            with st.expander(f"Review #{row['id']} - {row['stars']} ⭐"):
                
                is_arabic = any("\u0600" <= char <= "\u06FF" for char in row['content'])
                if is_arabic:
                    st.markdown(f'<div style="text-align: right; direction: rtl;">**Customer said:** {row["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.write(f"**Customer said:** {row['content']}")
                    
                st.info(f"**Your Reply:** {row['reply_content']}")