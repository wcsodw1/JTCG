import pandas as pd
import json
from agent.brain import JTCGAgent

def run():

    '''1.Launch AI Agent & Loading data '''
    agent = JTCGAgent() # 啟動你的智慧大腦
    input_path = 'evaluation/ai-eng-test-sample-conversations.json' # 載入官方提供的 324 個場景
    output_path = 'evaluation/evalResults_fullCompare_withToken.csv'
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        all_flattened_results = []
        # Simulation Loop(模擬多輪對話) : 
        # 職責： 這是自動化測試的核心。它模擬真實客人的提問，並把訊息餵給你寫的 agent.handle_query。這可以幫你快速發現 AI 在處理特定複雜意圖（如查訂單同時問運費）時是否會出錯。
        for scenario_idx, session in enumerate(data):
                    scenario_id = scenario_idx + 1
                    for msg_idx, message in enumerate(session):
                        role = message['role']
                        content = message['content'][0]['text']
                        
                        # 初始化變數
                        agent_response = ""
                        decision_code = ""
                        
                        # Only the Agent answers User questions
                        if role == 'user':
                            # 💡 接收 brain.py 回傳的兩個值
                            agent_response, decision_code = agent.handle_query(content)
                        
                        all_flattened_results.append({
                            "Scenario_ID": scenario_id,
                            "Turn": msg_idx + 1,
                            "Role": role,
                            "Original_Text": content,
                            "Agent_New_Response": agent_response,
                            "Decision": decision_code,  # ✅ 新增的 Tokenize 欄位 (1-5)
                            "Is_Correct": ""           # 留給你手動填寫 1 或 0
                        })
        
        df = pd.DataFrame(all_flattened_results)
        # 調整欄位順序，讓 Decision 緊跟在 Response 後面，方便對照
        cols = ["Scenario_ID", "Turn", "Role", "Original_Text", "Agent_New_Response", "Decision", "Is_Correct"]
        df = df[cols]

        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Simulation successful! Total rows: {len(all_flattened_results)}")
        print(f"📊 New column 'Decision' (1-5) added for logic tracking.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()