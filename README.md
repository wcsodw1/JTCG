# jtcg-ai-agent
## Project Purpose

jtcg-ai-agent is an AI-powered conversational agent designed for customer support scenarios.
It can:

Detect user intent

Answer FAQs

Recommend products

Query order status

Handover to human agents when necessary

The system also allows evaluation via simulated conversations to measure agent performance.

## Architecture Overview
jtcg-ai-agent/
├── agent/                   # Core AI modules
│   ├── intent.py            # Intent detection
│   ├── faq_rag.py           # FAQ retrieval
│   ├── product_search.py    # Product recommendation
│   ├── order_service.py     # Order query
│   ├── handover.py          # Human handover
│   └── agent.py             # Main agent class integrating all modules
├── data/                    # Sample data
│   ├── knowledges.csv       # FAQ knowledge base
│   ├── products.csv         # Products information
│   └── orders.json          # Order records
├── evaluation/              # Simulation & evaluation
│   ├── run_simulation.py    # Run test conversations
│   └── evaluation_results.csv
├── requirements.txt         # Dependencies
└── README.md                # Project overview


## Workflow

User sends a message.

agent/agent.py detects the intent (intent.py).

Relevant module is called:

faq_rag.py → FAQ answer

product_search.py → Product recommendation

order_service.py → Order query

handover.py → Transfer to human agent

Agent returns the response, intent, and tool used.

Optional: evaluation via run_simulation.py.

## How to Use
Install dependencies

pip install -r requirements.txt


Run the agent

from agent.agent import Agent

agent = Agent()
response = agent.run("請問我訂單狀態")
print(response)


Run simulation evaluation

python evaluation/run_simulation.py