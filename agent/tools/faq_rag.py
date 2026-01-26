import pandas as pd

class FAQSearcher:
    def __init__(self, path="data/knowledges.csv"):
        try:
            self.df = pd.read_csv(path, encoding='utf-8-sig')
        except:
            self.df = None

    def search(self, text):
        if self.df is None: return None
        text = text.lower()
        for _, row in self.df.iterrows():
            # Check if any part of the title or content matches
            if any(k in text for k in str(row['title']).lower().split()) or \
               any(k in text for k in str(row['tags/0']).lower().split()):
                return {
                    "ans": row['content'],
                    "url": row['urls/0/href']
                }
        return None