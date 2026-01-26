import re
from .tools.orders import OrderService
from .tools.faq_rag import FAQSearcher
from .tools.products import ProductSearcher
from .tools.handover import handover_to_human

class JTCGAgent:
    def __init__(self):
        self.order_tool = OrderService()
        self.faq_tool = FAQSearcher()
        self.prod_tool = ProductSearcher()
        self.history = []

    def handle_query(self, text):
        t = text.lower()
        self.history.append(text)
        is_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)

        # 1. Decision: Handover (Email detection)
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', t)
        if email_match:
            summary = f"User inquired: '{self.history[0]}'"
            return handover_to_human(email_match.group(), summary)

        if any(w in t for w in ["真人", "human", "agent", "客服"]):
            return "好的，請提供您的 Email 以便為您轉接真人客服。" if is_chinese else "Please provide your Email to transfer to a human agent."

        # 2. Decision: Orders
        uid_match = re.search(r'u_\d+|u_empty', t)
        if uid_match:
            return self.order_tool.list_orders(uid_match.group())

        # 3. Decision: FAQ
        faq = self.faq_tool.search(t)
        if faq:
            return f"{faq['ans']}\n🔗 詳情參考: {faq['url']}"

        # 4. Decision: Products
        prod = self.prod_tool.search(t)
        if prod:
            return f"為您推薦：{prod['name']}\n規格：{prod['specs']}\n🔗 產品頁: {prod['url']}"

        # 5. Default Navigation (Requirement 3E)
        if is_chinese:
            return "您好！我是 JTCG 助手。我可以幫您查詢訂單、了解退換貨政策或推薦產品。請問您的 User ID 是？或想了解哪款支架？"
        return "Hello! I'm the JTCG Assistant. I can help with order tracking, FAQs, or product specs. How can I help today?"