import pandas as pd

class ProductSearcher:
    def __init__(self, path="data/products.csv"):
        try:
            self.df = pd.read_csv(path, encoding='utf-8-sig')
        except:
            self.df = None

    def search(self, text):
        if self.df is None: return None
        text = text.lower()
        for _, row in self.df.iterrows():
            if any(k in text for k in str(row['name']).lower().split()):
                specs = f"螢幕支援: {row['specs/size_max_inch']} 吋 | 承重: {row['specs/weight_per_arm_kg']}kg"
                return {
                    "name": row['name'],
                    "specs": specs,
                    "url": row['url']
                }
        return None