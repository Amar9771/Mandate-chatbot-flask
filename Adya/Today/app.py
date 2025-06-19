import streamlit as st
import pandas as pd
from models.rating_model import RatingModel
from utils import load_data, plot_financials

st.title("Brickwork Ratings AI Assistant - Demo")

uploaded_file = st.file_uploader("Upload Financials CSV", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("Please upload financial data CSV.")
    st.stop()

model = RatingModel()
model.train(df)

company_list = df['Company'].tolist()
selected_company = st.selectbox("Select Company to Analyze", company_list)

if selected_company:
    comp_data = df[df['Company'] == selected_company].iloc[0]
    st.subheader(f"Financial Overview - {selected_company}")
    st.write(comp_data)

    st.subheader("Generated Rating")
    rating = model.predict_rating(comp_data['ROE'], comp_data['DebtEquity'])
    st.markdown(f"### Credit Rating: **{rating}**")

    st.subheader("Financial Metrics Visualization")
    fig = plot_financials(df, selected_company)
    if fig:
        st.pyplot(fig)

    # Sample AI assistant message
    st.subheader("AI Research Agent Insight")
    insight = (
        f"The company {selected_company} has an ROE of {comp_data['ROE']:.2f} and "
        f"Debt to Equity ratio of {comp_data['DebtEquity']:.2f}. Based on these metrics, "
        f"the predicted credit rating is {rating}. "
        f"Monitor debt levels closely to maintain or improve this rating."
    )
    st.info(insight)
