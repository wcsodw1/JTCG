import re  
# re 過濾 (True/False)：快速過濾掉不相關的訊息, 提取 (Extraction)：精準抓取 u_123 或 abc@gmail.com, 價值：針對訂單 ID 或 Email 這類「固定模式」，在 0.001 秒內就能給出答案，完全不花一毛 Token 錢。
from .tools.orders import OrderService
from .tools.faq_rag import FAQSearcher
from .tools.products import ProductSearcher
from .tools.handover import handover_to_human

''' 2.Routing Layer(意圖路由層) '''
class JTCGAgent:
    def __init__(self):
        self.order_tool = OrderService()
        self.faq_tool = FAQSearcher()
        self.prod_tool = ProductSearcher()
        self.history = []

    def handle_query(self, text):
        t = text.lower()
        self.history.append(text) # 為了實現轉接時的「案件摘要」。系統會記錄對話歷史，這樣在 handover_to_human 時，真人客服才能知道客人的第一個問題是什麼。
        is_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)


        # Decision 1: 設計轉接真人的邏輯 Handover (Email detection) 設計轉接真人的邏輯 -> ["真人", "human", "agent", "客服"]
        # re 進階版的文件過濾器,用「篩網」來比喻, 這邊用re會檢查格式, 判斷以下是否為mail, 
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', t)
        if email_match:
            summary = f"User inquired: '{self.history[0]}'"
            return handover_to_human(email_match.group(), summary), "1"

        if any(w in t for w in ["真人", "human", "agent", "客服"]):
            res = "好的，請提供您的 Email 以便為您轉接真人客服。" if is_chinese else "Please provide your Email to transfer to a human agent."
            return res, "1"

        # Decision 2: Orders
        # re 判斷完之後，還能把那串符合格式的文字「抓」出來, # 這裡不只是知道它是 True，還把 "u_12345" 抓出來遞交給下一個部門
        uid_match = re.search(r'u_\d+|u_empty', t)
        if uid_match:
            return self.order_tool.list_orders(uid_match.group()), "2"

        # Decision 3: FAQ
        # FAQ 部門的職責是 「提供權威性的標準答案」，避免 AI 產生幻覺（Hallucination）。
        # 讀取 agent/tool/faq_reg.py 裡面的 knowledges.csv
        # 政策優先。 如果不是查訂單，先去翻「政策手冊」(FAQSearcher)。如果匹配到退換貨、運費等關鍵字，就回傳權威答案與官方連結。
        faq = self.faq_tool.search(t)
        if faq:
            return f"{faq['ans']}\n🔗 詳情參考: {faq['url']}", "3"

        # Decision 4: Products
        # 銷售導向。 如果前面都沒匹配到，最後去翻「產品目錄」(ProductSearcher)。當提到產品名稱時，它會輸出詳盡的規格與產品頁面連結。
        prod = self.prod_tool.search(t)
        if prod:
            return f"為您推薦：{prod['name']}\n規格：{prod['specs']}\n🔗 產品頁: {prod['url']}", "4"

        # Decision 5. Default Navigation (Requirement 3E)
        # 當 AI 完全聽不懂時，它不會當機，而是會根據客人的語系（中文或英文）給出一段親切的導引，告訴客人「我可以幫你什麼」。
        if is_chinese:
            res = "您好！我是 JTCG 助手。我可以幫您查詢訂單、了解退換貨政策或推薦產品。請問您的 User ID 是？或想了解哪款支架？"
        else:
            res = "Hello! I'm the JTCG Assistant. I can help with order tracking, FAQs, or product specs. How can I help today?"
            
        return res, "5"