import pandas as pd
import json
from agent.brain import JTCGAgent

def run():
    agent = JTCGAgent()
    input_path = 'evaluation/ai-eng-test-sample-conversations.json'
    output_path = 'evaluation/eval_results_full_compare.csv'
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        all_flattened_results = []
        for scenario_idx, session in enumerate(data):
            scenario_id = scenario_idx + 1
            for msg_idx, message in enumerate(session):
                role = message['role']
                content = message['content'][0]['text']
                
                # Only the Agent answers User questions
                agent_response = agent.handle_query(content) if role == 'user' else ""
                
                all_flattened_results.append({
                    "Scenario_ID": scenario_id,
                    "Turn": msg_idx + 1,
                    "Role": role,
                    "Original_Text": content,
                    "Agent_New_Response": agent_response,
                    "Is_Correct": "" # Column for your manual review
                })
        
        df = pd.DataFrame(all_flattened_results)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ Simulation successful! Total rows: {len(all_flattened_results)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()