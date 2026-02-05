from agent.brain import JTCGAgent
if __name__ == "__main__":
    ''' 1.Ingestion Layer(輸入接入層) '''
    agent = JTCGAgent() # 啟動 Agent，準備接待客人
    print("JTCG Agent Online.")
    while True:
        inp = input("You: ") # 接收客人說的話
        if inp == "exit": break
        print(f"Agent: {agent.handle_query(inp)}")  # 傳遞給大腦並回覆

