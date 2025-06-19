from sklearn.linear_model import LogisticRegression
import pandas as pd

class RatingModel:
    def __init__(self):
        # Simple dummy model - assign ratings based on ROE and DebtEquity ratio
        self.model = LogisticRegression()
        self.trained = False

    def train(self, df: pd.DataFrame):
        # Dummy binary target: 1 for good rating, 0 for poor rating (just for example)
        df['GoodRating'] = ((df['ROE'] > 0.15) & (df['DebtEquity'] < 0.7)).astype(int)
        features = df[['ROE', 'DebtEquity']]
        target = df['GoodRating']
        self.model.fit(features, target)
        self.trained = True

    def predict_rating(self, roe, debt_equity):
        if not self.trained:
            raise Exception("Model not trained")
        prob = self.model.predict_proba([[roe, debt_equity]])[0,1]
        if prob > 0.7:
            return "AAA"
        elif prob > 0.5:
            return "AA"
        elif prob > 0.3:
            return "A"
        else:
            return "BBB"
