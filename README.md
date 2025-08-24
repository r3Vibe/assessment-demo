# assessment-demo

Hi hope you are doing well. Thank you for this opportunity. Given the time i tried to do as best as i can. This is a basic demo and there is a lot of room for improvements. I had a openai account so i used gpt for the LLM. It can be easily swapped with gemini if needed. 

### Please Follow the SETUP Requirements before running

Here is a loom video link for a walkthrough:- 

## Table of contents

- [Quick overview](#quick-overview)
- [Tech stack](#tech-stack)
- [Repository structure](#repository-structure)
- [SETUP Requirements](#requirements--assumptions)
- [Features](#features)
- [Run locally (dev)](#run-locally-dev)
  - [Backend (Python)](#backend-python)
  - [Frontend (Vite + React + TypeScript)](#frontend-vite--react--typescript)
  - [Both together (recommended)](#both-together-recommended)
- [Run with Docker (recommended for quick demo)](#run-with-docker-recommended-for-quick-demo)


## Quick overview

- Backend: Python service (FastAPI and LangChain) located in `backend/` exposing HTTP APIs and WebSocket endpoints. The code lives under `backend/app/`.
- Frontend: Vite + React + TypeScript app inside `frontend/` (entry `src/main.tsx`, main component `src/App.tsx`).
- Docker: Root `docker-compose.yml` and service Dockerfiles for running everything with Docker.

This project is intended as a compact demonstration or assessment project and is organized to be easy to run locally or inside Docker.


## Tech stack

- Backend: Python 3.12+ (project files reference CPython 3.12 bytecode). Uses common web stack patterns (FastAPI/uvicorn, Pydantic) — see `backend/requirements.txt` for exact packages.
- Frontend: Vite, React, TypeScript.
- Containerization: Docker and docker-compose.


## Repository structure

Top-level:

- `backend/` — Python service
  - `Dockerfile` — container image for the backend
  - `requirements.txt` — Python dependencies
  - `setup-db.py` — helper to initialize data/storage
  - `app/` — python application package
    - `main.py` — app entrypoint
    - `sockets.py` — WebSocket handlers
    - `schema.py` — request/response schemas
    - `config.py` — configuration
    - `agent/` — domain logic (graph, tools)

- `frontend/` — Vite + React app
  - `Dockerfile` — container image for frontend
  - `package.json` — npm scripts and deps
  - `src/` — React + TypeScript source code

- `docker-compose.yml` — start both frontend & backend together
- `README.md` — this file


## SETUP Requirements

- Git clone the project `git@github.com:r3Vibe/assessment-demo.git`
- Add database url and openai api key in the `.env` file
- Run the setup-db file from the `backend` folder
    - RUN `docker exec -it backend bash`
    - Once inside RUN `python setup-db.py`

## Features
- Streaming Responses
- Short and Long Term Memory (Ability to remember user name)
- Uses REPL to plot data image and send to Frontend
- Ability to talk about the uploaded Data


## Run locally (dev)

We'll show separate instructions to run each side during development. Use a dedicated terminal per service.

### Backend (Python)

1. Create a virtual environment and install deps:

```powershell
cd backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Start the app (common options):

```powershell
# If the project uses uvicorn + FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


### Frontend (Vite + React + TypeScript)

1. Install dependencies and start the dev server:

```powershell
cd frontend
npm install
npm run dev
```

2. Open the app in the browser (Vite will print the local URL, typically http://localhost:5173).


### Both together (recommended)

- Run backend + frontend in parallel (two terminals) following the two sections above.
- Or use Docker Compose (see next section) to run both in containers.


## Run with Docker (recommended for quick demo)

The repo includes `docker-compose.yml` and Dockerfiles for both services so you can run the full stack with one command.

1. Build and start everything:

```powershell
docker compose up --build
```

2. Stop and remove containers:

```powershell
docker compose down
```
