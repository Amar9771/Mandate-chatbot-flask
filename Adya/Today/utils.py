import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def plot_financials(df, company):
    comp_data = df[df['Company'] == company]
    if comp_data.empty:
        return None
    fig, ax = plt.subplots()
    metrics = ['Revenue', 'ProfitMargin', 'DebtEquity', 'ROE']
    values = [comp_data.iloc[0][m] for m in metrics]
    ax.bar(metrics, values, color='skyblue')
    ax.set_title(f'Financial Metrics for {company}')
    return fig
