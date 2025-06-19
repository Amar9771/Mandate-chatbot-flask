def compare_with_peers(data, peer_avg):
    comparison = {}
    for col in ['Revenue', 'EBITDA_Margin', 'Debt_Equity']:
        comparison[col] = {
            'Company': data[col].mean(),
            'Peer Avg': peer_avg.get(col, 0)
        }
    return comparison