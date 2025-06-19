import streamlit as st
st.set_page_config(page_title="Mandate Chatbot", page_icon="🤖", layout="centered")

import pandas as pd
import re

# --- Load Excel ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("MandatesData.xlsx")
        df["Mandate ID"] = pd.to_numeric(df["Mandate ID"], errors="coerce").dropna().astype(int)
        return df
    except Exception as e:
        st.error(f"❌ Failed to load Excel file: {e}")
        return pd.DataFrame()

df = load_data()

# --- Mandate Info Extractor ---
def get_mandate_info(text, last_mandate_id=None):
    try:
        match = re.search(r'\b\d{2}[\s-]?\d{3}\b', text) or re.search(r'\b\d{5}\b', text)
        if match:
            mandate_id = int(re.sub(r'\D', '', match.group()))
            st.session_state.last_mandate_id = mandate_id
        else:
            mandate_id = last_mandate_id
            if not mandate_id:
                return "⚠️ Please provide a valid Mandate ID."

        result = df[df["Mandate ID"] == mandate_id]
        if result.empty:
            return f"❌ No data found for Mandate ID {mandate_id}."

        record = result.iloc[0]
        text_lower = text.lower()
        response = [f"**Mandate ID:** {mandate_id}"]

        if "analyst" in text_lower:
            response.append(f"**Analyst:** {record.get('Analyst', 'N/A')}")

        if "chairperson" in text_lower or "cp" in text_lower:
            response.append(f"**Chairperson:** {record.get('Chairperson', 'N/A')}")

        if "rating type" in text_lower:
            response.append(f"**Rating Type:** {record.get('Rating Type', 'N/A')}")

        if "rating action" in text_lower:
            response.append(f"**Rating Action:** {record.get('RatingAction', 'N/A')}")

        if "rating" in text_lower and "rating action" not in text_lower:
            response.append(f"**Rating:** {record.get('Rating', 'N/A')}")

        if "status" in text_lower:
            response.append(f"**Mandate Status:** {record.get('Mandate Status', 'N/A')}")

        if "published date" in text_lower:
            date = record.get('Published Date')
            response.append(f"**Published Date:** {date.strftime('%Y-%m-%d') if pd.notnull(date) else 'N/A'}")

        if "issue size" in text_lower:
            response.append(f"**Issue Size:** {record.get('Issue Size', 'N/A')} Cr")

        if len(response) == 1:
            # No specific match – return all details
            date = record.get('Published Date')
            full_info = [
                f"**Analyst:** {record.get('Analyst', 'N/A')}",
                f"**Chairperson:** {record.get('Chairperson', 'N/A')}",
                f"**Rating Type:** {record.get('Rating Type', 'N/A')}",
                f"**Rating:** {record.get('Rating', 'N/A')}",
                f"**Mandate Status:** {record.get('Mandate Status', 'N/A')}",
                f"**Rating Action:** {record.get('RatingAction', 'N/A')}",
                f"**Published Date:** {date.strftime('%Y-%m-%d') if pd.notnull(date) else 'N/A'}",
                f"**Issue Size:** {record.get('Issue Size', 'N/A')} Cr"
            ]
            response.extend(full_info)

        return "\n\n".join(response)

    except Exception as e:
        return f"⚠️ Error: {e}"

# --- Streamlit UI ---
st.title("🤖 Mandate Chatbot (FY 2024–2025)")
st.caption("Ask me anything about a mandate, like: *'Who is the analyst for mandate 82669?'*")

# Initialize session state
if "last_mandate_id" not in st.session_state:
    st.session_state.last_mandate_id = None
if "history" not in st.session_state:
    st.session_state.history = []

# Show chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New user input
user_msg = st.chat_input("Ask about any mandate ID...")

if user_msg:
    st.chat_message("user").markdown(user_msg)
    st.session_state.history.append({"role": "user", "content": user_msg})

    bot_reply = get_mandate_info(user_msg, st.session_state.last_mandate_id)
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.history.append({"role": "assistant", "content": bot_reply})
