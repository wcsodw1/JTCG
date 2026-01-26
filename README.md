# jtcg-ai-agent

## Project Purpose

**jtcg-ai-agent** is a modular AI-powered conversational agent designed to provide a "one-stop" support experience for JTCG Shop customers. It balances automated efficiency with human empathy by seamlessly connecting FAQ retrieval, product recommendations, and real-time order tracking.

It can:
- **Detect user intent**: Automatically routes queries to the appropriate service (Order, FAQ, or Product).
- **Answer FAQs**: Provides authoritative answers on brand policies and platform regulations using `knowledges.csv`.
- **Recommend products**: Suggests JTCG arms and accessories based on specs found in `products.csv`.
- **Query order status**: Real-time tracking of shipping progress via `orders.json`.
- **Handover conversations**: Seamlessly escalates to human agents with a summarized session context.

Additionally, the system supports evaluation through simulated conversations, allowing you to measure and improve agent performance.

## Architecture Overview



```bash
jtcg-ai-agent/
├── agent/
│   ├── __init__.py
│   ├── brain.py            # Main Agent logic (Intent Routing)
│   ├── prompts.py          # Brand Voice & System instructions
│   └── tools/              # Functional Modules
│       ├── faq_rag.py      # Logic for knowledges.csv
│       ├── products.py     # Search logic for products.csv
│       ├── orders.py       # JSON lookup logic for orders.json
│       └── handover.py     # Mock handover with session summary
├── data/
│   ├── knowledges.csv      # JTCG FAQ & Policies
│   ├── products.csv        # Product Specs & Catalog
│   └── orders.json         # Customer Order Database
├── evaluation/
│   ├── run_simulation.py   # Script to process the 324 scenarios
│   ├── ai-eng-test-sample-conversations.json # Input test cases
│   └── eval_results_full_compare.csv # Final output for submission
├── main.py                 # Interactive CLI Chatbot entry point
├── requirements.txt        # Project dependencies (pandas, etc.)
├── .gitignore              # Excludes venv and cache files
└── README.md               # Technical documentation
```



---

## Workflow

1. User sends a message: Input is received via main.py or the evaluation script.
2. Intent Detection: agent/brain.py identifies the intent (Order, FAQ, Product, or Handover).
3. Module Execution: The relevant tool is called based on intent:
    - `faq_rag.py` → FAQ answer + Source URL
    - `products.py` → Product recommendation + Specs
    - `order_service.py` → Order status via User ID
    - `handover.py` → Transfer with session summary
4. Response Generation: Agent returns a concise, friendly response following the brand voice.
5. Evaluation: Use `run_simulation.py` to batch-process scenarios and audit agent accuracy.

---

## How to Use

### Install dependencies
```bash
pip install -r requirements.txt

```

### Run the agent (Interactive Mode)
```bash
python3 main.py
```

### Run simulation evaluation
```bash
python3 -m evaluation.run_simulation
```