import re

def handover_to_human(email, summary):
    # Requirement 3D: Transfer confirmation with case summary
    return (f"【轉接成功】已為您轉接真人客服，請稍候。\n"
            f"案件摘要：{summary}\n"
            f"聯絡信箱：{email}")