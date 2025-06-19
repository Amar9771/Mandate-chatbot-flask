def generate_rationale(fin_data):
    rationale = []
    if fin_data['Revenue'].mean() > 100:
        rationale.append("Strong revenue base with consistent growth.")
    if fin_data['EBITDA_Margin'].mean() > 15:
        rationale.append("Healthy operating margins.")
    if fin_data['Debt_Equity'].mean() > 2:
        rationale.append("High leverage remains a concern.")
    return " ".join(rationale)