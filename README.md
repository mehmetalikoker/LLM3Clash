# What's LLM3Clash Project
With the LLM3Clash project, we obtain simultaneous responses from three different AI models—OpenAI, DeepSeek, and Claude—for every prompt. This allows us to benchmark and compare these AI models based on their response quality and processing speed

## 🎨 How Does It Look

![Ekran görüntüsü 2026-04-18 104914.png](../../Desktop/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202026-04-18%20104914.png)

## 🖥️ Installation
1) Clone the repository:

```bash
# git clone
https://github.com/mehmetalikoker/LLM3Clash.git
```
2) Set up your environment variables in a .env file
 ```bash
 # You simply need to add the API Key's to the project's .env file.
- OPENAI_API_KEY
- DEEPSEEK_API_KEY
- ANTHROPIC_API_KEY
- LANGCHAIN_API_KEY
```

## 🖥️ How It Works
It is sufficient to run it through the terminal.

 ```bash 
streamlit run generate.py
```