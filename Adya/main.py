from financial_parser import load_financial_data
from peer_compare import compare_with_peers
from rating_writer import generate_rationale

# Load company data
company_data = load_financial_data('mock_data/company_financials.csv')

# Peer average for simplicity
peer_avg = {
    'Revenue': 90,
    'EBITDA_Margin': 12,
    'Debt_Equity': 1.5
}

# Compare and generate report
comparison = compare_with_peers(company_data, peer_avg)
rationale = generate_rationale(company_data)

print("Peer Comparison:")
for k, v in comparison.items():
    print(f"{k}: Company={v['Company']} vs Peer Avg={v['Peer Avg']}")
print("\nGenerated Rating Rationale:")
print(rationale)