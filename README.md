
## Prerequisites
- Install Ollama: https://ollama.com
- Download the required models via Ollama:
  - e.g., `ollama pull model_name`
  - ministral-3:3b-cloud
  - kimi-k2-thinking:cloud
  - glm-5:cloud
- Gemini currently isn't supported
## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
