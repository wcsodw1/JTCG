import json

class OrderService:
    def __init__(self, path="data/orders.json"):
        self.path = path
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.db = json.load(f).get("orders_db", {})
        except Exception:
            self.db = {}

    def list_orders(self, user_id):
            user_data = self.db.get(user_id)
            if not user_data:
                return f"找不到 User ID: {user_id} 的訂單資料。"
            
            # 取得 orders 列表，如果沒有則設為空列表
            orders = user_data.get("orders", [])
            if not orders:
                return f"用戶 {user_id} 目前沒有任何訂單紀錄。"
            
            res = ["為您找到以下訂單："]
            for o in orders:
                # 安全取得 items，避免 KeyError: 'items'
                items_list = o.get('items', [])
                items_str = ", ".join([f"{i.get('name', '未知商品')}x{i.get('qty', 1)}" for i in items_list])
                
                res.append(f"- 訂單號: {o.get('order_id', 'N/A')} | 狀態: {o.get('status', '處理中')} | 品項: {items_str}")
            
            return "\n".join(res)