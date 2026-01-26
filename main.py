from agent.brain import JTCGAgent
if __name__ == "__main__":
    agent = JTCGAgent()
    print("JTCG Agent Online.")
    while True:
        inp = input("You: ")
        if inp == "exit": break
        print(f"Agent: {agent.handle_query(inp)}")

