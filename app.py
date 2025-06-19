# app.py (Streamlit version, no Flask)

import streamlit as st
import pandas as pd
import re

# Load Excel file
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("MandatesData.xlsx")
        df["Mandate ID"] = df["Mandate ID"].astype(int)
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()

df = load_data()

def get_mandate_info(text):
    match = re.search(r'\b(\d{5}|\d{2}[\s-]?\d{3})\b', text)
    if match:
        mandate_id = int(re.sub(r'\D', '', match.group()))
    else:
        return "⚠️ Please enter a valid Mandate ID (e.g. 82669)."

    result = df[df["Mandate ID"] == mandate_id]
    if result.empty:
        return f"❌ No data found for Mandate ID {mandate_id}."

    record = result.iloc[0]
    text_lower = text.lower()

    def published_date_str(date):
        if pd.notnull(date):
            return date.strftime('%Y-%m-%d') if isinstance(date, pd.Timestamp) else str(date)
        return "N/A"

    if "analyst" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Analyst:** {record.get('Analyst', 'N/A')}"
    elif "chairperson" in text_lower or "cp" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Chairperson:** {record.get('Chairperson', 'N/A')}"
    elif "rating type" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Rating Type:** {record.get('Rating Type', 'N/A')}"
    elif "rating action" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Rating Action:** {record.get('RatingAction', 'N/A')}"
    elif "rating" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Rating:** {record.get('Rating', 'N/A')}"
    elif "status" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Mandate Status:** {record.get('Mandate Status', 'N/A')}"
    elif "published date" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Published Date:** {published_date_str(record.get('Published Date'))}"
    elif "issue size" in text_lower:
        return f"**Mandate ID:** {mandate_id}\n\n**Issue Size:** {record.get('Issue Size', 'N/A')} Cr"
    else:
        return f"""
        **Mandate ID:** {mandate_id}  
        **Analyst:** {record.get('Analyst', 'N/A')}  
        **Chairperson:** {record.get('Chairperson', 'N/A')}  
        **Rating Type:** {record.get('Rating Type', 'N/A')}  
        **Rating:** {record.get('Rating', 'N/A')}  
        **Mandate Status:** {record.get('Mandate Status', 'N/A')}  
        **Rating Action:** {record.get('RatingAction', 'N/A')}  
        **Published Date:** {published_date_str(record.get('Published Date'))}  
        **Issue Size:** {record.get('Issue Size', 'N/A')} Cr
        """

# Streamlit UI
st.title("📄 Mandate Info Chatbot")
user_input = st.text_input("Ask a question (e.g., 'Who is the analyst for 82669?')")

if user_input:
    st.markdown(get_mandate_info(user_input))
