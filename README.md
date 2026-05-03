# genai-dev-assistant-mcp
Build a GenAI assistant for GitHub MCP

This project can load a local repository or clone a GitHub repository URL, then use an LLM to explain code, answer questions, or generate a README.

## Run the modern frontend

```bash
streamlit run frontend/streamlit_app.py
```

Enter a local path like `./data/sample_repo` or a GitHub URL like `https://github.com/VenkatProjects/mcp_server_weather_agent`.

## Deployment

See `DEPLOYMENT.md` for recommended deployment platforms and instructions. Netlify cannot host the Streamlit app directly.

> Do not commit `.env` with real API keys. Use Streamlit Cloud secrets instead.

Include:

🔹 What it does
🔹 Architecture diagram (even simple)
🔹 Screenshots
🔹 Example queries