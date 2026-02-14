# LFG-Mathai (Beta)

**Interactive math tutor wrapper for LLM models providing step-by-step explanations and problem-solving guidance.**  

This project was created in **one day** for the **Wissenschaftswoche** at the **Lion Feuchtwanger Gymnasium**.  
> ⚠️ **Beta:** The project is partially complete and experimental.


---


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
```

---

## Credits

This project was created by the following team:

- **Hüseyin Seyfi Girgin** – Project lead / Python development  
- **Deniz Percinel** – Testing
- **Martin Schindler** – Prompt Engineering