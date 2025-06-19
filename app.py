import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Mandate Chatbot", layout="centered")

st.title("📋 Mandate Info Chatbot")

# File uploader
uploaded_file = st.file_uploader("Upload MandatesData.xlsx", type=["xlsx"])

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df["Mandate ID"] = df["Mandate ID"].astype(int)
        st.session_state.df = df
        st.success("Excel file loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")

# User Input
query = st.text_input("Ask something about a mandate (e.g., 'Who is the analyst for 82669?')")

def answer_query(text, df):
    match = re.search(r'\b(\d{2}[\s-]?\d{3}|\d{5})\b', text)
    if not match:
        return "❗Please enter a valid Mandate ID in your question."

    mandate_id = int(re.sub(r'\D', '', match.group()))
    result = df[df["Mandate ID"] == mandate_id]

    if result.empty:
        return f"❌ No data found for Mandate ID {mandate_id}"

    record = result.iloc[0]
    text_lower = text.lower()

    if "analyst" in text_lower:
        return f"👤 Analyst for Mandate {mandate_id}: {record.get('Analyst', 'N/A')}"
    if "chairperson" in text_lower or "cp" in text_lower:
        return f"🪑 Chairperson for Mandate {mandate_id}: {record.get('Chairperson', 'N/A')}"
    if "rating type" in text_lower:
        return f"🏷️ Rating Type: {record.get('Rating Type', 'N/A')}"
    if "rating" in text_lower and "rating type" not in text_lower and "rating action" not in text_lower:
        return f"⭐ Rating: {record.get('Rating', 'N/A')}"
    if "status" in text_lower:
        return f"📌 Status: {record.get('Mandate Status', 'N/A')}"
    if "rating action" in text_lower:
        return f"⚡ Rating Action: {record.get('RatingAction', 'N/A')}"
    if "published" in text_lower:
        published_date = record.get("Published Date")
        pub_str = published_date.strftime("%Y-%m-%d") if pd.notnull(published_date) else "N/A"
        return f"📅 Published Date: {pub_str}"
    if "issue size" in text_lower:
        return f"💰 Issue Size: {record.get('Issue Size', 'N/A')} Cr"

    # Default full data
    pub_str = record.get("Published Date")
    pub_str = pub_str.strftime("%Y-%m-%d") if pd.notnull(pub_str) else "N/A"
    return f"""
**Mandate ID**: {mandate_id}  
**Analyst**: {record.get('Analyst', 'N/A')}  
**Chairperson**: {record.get('Chairperson', 'N/A')}  
**Rating Type**: {record.get('Rating Type', 'N/A')}  
**Rating**: {record.get('Rating', 'N/A')}  
**Rating Action**: {record.get('RatingAction', 'N/A')}  
**Status**: {record.get('Mandate Status', 'N/A')}  
**Published Date**: {pub_str}  
**Issue Size**: {record.get('Issue Size', 'N/A')} Cr  
"""

# Display response
if query and st.session_state.df is not None:
    response = answer_query(query, st.session_state.df)
    st.markdown(response)
elif query:
    st.warning("⚠️ Please upload the Excel file first.")
