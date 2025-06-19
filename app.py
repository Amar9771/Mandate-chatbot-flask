from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import re
import logging
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')  # Safer for deployment

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load Excel data
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "MandatesData.xlsx")

try:
    df = pd.read_excel(EXCEL_PATH)
    df["Mandate ID"] = df["Mandate ID"].astype(int)
except Exception as e:
    logging.error(f"Error loading Excel file: {e}")
    df = pd.DataFrame()

def get_mandate_info(text):
    try:
        # Detect Mandate ID like "82 669" or "82-669" or "82669"
        match = re.search(r'\b(\d{5}|\d{2}[\s-]?\d{3})\b', text)
        if match:
            mandate_id = int(re.sub(r'\D', '', match.group()))
            session['last_mandate_id'] = mandate_id
        else:
            mandate_id = session.get('last_mandate_id')
            if not mandate_id:
                return "⚠️ Please provide a valid Mandate ID (e.g., 'Who is the analyst for 82669?')."

        result = df[df["Mandate ID"] == mandate_id]
        if result.empty:
            return f"❌ No data found for Mandate ID {mandate_id}."

        record = result.iloc[0]
        text_lower = text.lower()

        def format_date(val):
            return val.strftime('%Y-%m-%d') if pd.notnull(val) and hasattr(val, 'strftime') else "N/A"

        if "analyst" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Analyst:</strong> {record.get('Analyst', 'N/A')}</p>"

        if "chairperson" in text_lower or "cp" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Chairperson:</strong> {record.get('Chairperson', 'N/A')}</p>"

        if "rating type" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Rating Type:</strong> {record.get('Rating Type', 'N/A')}</p>"

        if "rating action" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Rating Action:</strong> {record.get('RatingAction', 'N/A')}</p>"

        if "rating" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Rating:</strong> {record.get('Rating', 'N/A')}</p>"

        if "status" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Status:</strong> {record.get('Mandate Status', 'N/A')}</p>"

        if "published date" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Published Date:</strong> {format_date(record.get('Published Date'))}</p>"

        if "issue size" in text_lower:
            return f"<p><strong>Mandate ID:</strong> {mandate_id}</p><p><strong>Issue Size:</strong> {record.get('Issue Size', 'N/A')} Cr</p>"

        # Fallback: Show full details
        return f"""
        <p><strong>Mandate ID:</strong> {mandate_id}</p>
        <p><strong>Analyst:</strong> {record.get('Analyst', 'N/A')}</p>
        <p><strong>Chairperson:</strong> {record.get('Chairperson', 'N/A')}</p>
        <p><strong>Rating Type:</strong> {record.get('Rating Type', 'N/A')}</p>
        <p><strong>Rating:</strong> {record.get('Rating', 'N/A')}</p>
        <p><strong>Mandate Status:</strong> {record.get('Mandate Status', 'N/A')}</p>
        <p><strong>Rating Action:</strong> {record.get('RatingAction', 'N/A')}</p>
        <p><strong>Published Date:</strong> {format_date(record.get('Published Date'))}</p>
        <p><strong>Issue Size:</strong> {record.get('Issue Size', 'N/A')} Cr</p>
        """

    except Exception as e:
        logging.error(f"Error in get_mandate_info: {e}")
        return "⚠️ Something went wrong. Please try again."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("message", "")
    reply = get_mandate_info(user_text)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
