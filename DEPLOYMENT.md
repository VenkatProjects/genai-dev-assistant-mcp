# Deployment Guide

## Important note
This repository contains a Python Streamlit app (`frontend/streamlit_app.py`). Netlify is designed for static sites and serverless functions, not long-running Python web apps like Streamlit.

### Recommended platforms for this app
- Streamlit Community Cloud
- Render
- Railway
- Fly.io

## If you still want to use Netlify
Netlify can only host a static landing page in this repo. The `netlify.toml` and `frontend/index.html` files provide a static fallback page.

The Streamlit app itself cannot run on Netlify in its current form.

## Deploying on Streamlit Community Cloud
1. Push your repo to GitHub.
2. Go to https://streamlit.io/cloud and log in.
3. Click `New app` and connect your GitHub repo.
4. Select branch `main` and the file `frontend/streamlit_app.py`.
5. Add any required environment variables in the Streamlit app settings.
6. Deploy.

## Deploying on Render
1. Push your repo to GitHub.
2. Go to https://render.com and create a new Web Service.
3. Connect your GitHub repository.
4. Set the root directory to `/`.
5. Use the following build and start commands:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run frontend/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
6. Set environment variables if needed.

## Deploying on Railway
1. Push your repo to GitHub.
2. Create a new project in Railway and connect the repo.
3. Use the same build and start commands as Render.
4. Add required environment variables.

## Adding support for more file types
The repo loader now supports these file extensions:
- `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.vue`, `.html`, `.java`, `.cpp`

If you want to add more file types, update the `SUPPORTED_EXTENSIONS` list in `backend/repo_loader.py`.

## Files to push now
- `frontend/streamlit_app.py`
- `backend/app.py`
- `backend/repo_loader.py`
- `backend/tools.py`
- `backend/llm.py`
- `backend/__init__.py`
- `requirements.txt`
- `README.md`
- `DEPLOYMENT.md`
- `netlify.toml`
- `frontend/index.html`
- any sample repo contents under `data/sample_repo`

## Continuous deployment recommendation
For continuous uptime, Streamlit Cloud or Render are the best fit. Netlify is not suitable for the actual Streamlit runtime.
