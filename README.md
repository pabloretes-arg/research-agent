# Research Agent

A small AI agent built with [smolagents](https://github.com/huggingface/smolagents) and Google Gemini, as the hands-on project for **Unit 1 of the [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course)**.

It answers questions by reasoning in a **Thought → Action → Observation** loop: it decides which tool it needs, writes Python code to call it, reads the result, and repeats until it can give a final answer.

## Demo

<!-- Drag research_agent_demo.mp4 here when editing this file on GitHub -->

## What it can do

| Tool | What it does | Source |
|---|---|---|
| `get_current_time_in_timezone` | Gets the current time in any time zone | Custom tool (`pytz`) |
| `web_search` | Searches the web | smolagents built-in (DuckDuckGo) |
| `visit_webpage` | Reads the full text of a web page | smolagents built-in |
| `generate_image` | Creates an image from a text prompt | Custom tool ([Pollinations](https://pollinations.ai)) |

Example questions:

- *"What time is it in Tokyo and Sydney right now?"*: two tool calls in a single Python step.
- *"Draw me an astronaut cat."*: the agent rewrites the prompt in detail before calling the image tool.
- *"Give me a summary of today's Argentine news."*: checks today's date first, then searches and summarizes.

## How it works

- **Brain:** Gemini Flash-Lite via [LiteLLM](https://github.com/BerriAI/litellm).
- **Agent type:** `CodeAgent`. Instead of emitting JSON, the agent writes Python code to call its tools, so it can combine several actions in one step.
- **Instructions:** a custom rule tells the agent to check the current date whenever the user says "today" or "now", and to keep only search results from that date.
- **Interface:** a local chat UI with Gradio.

## Run it locally

```bash
git clone https://github.com/<your-user>/research-agent.git
cd research-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your Gemini API key to .env
python3 research_agent.py
```

Open http://127.0.0.1:7860 in your browser.

## Lessons learned

- **Free tiers change.** The course template ran on a free Hugging Face Space with Hugging Face inference credits. Both are now paid, so I adapted the project to run locally with Gemini's free tier.
- **Agents hallucinate observations.** Sometimes the model "imagined" a tool result instead of waiting for the real one. The agent loop caught the broken code and recovered.
- **Instructions matter.** One sentence about checking the date fixed answers that mixed up news from different days.
- **Secrets stay out of the code.** API keys live in a `.env` file that is never committed.

## Credits

Built by **Pablo Retes** while taking the [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course).
