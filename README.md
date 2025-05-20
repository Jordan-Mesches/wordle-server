# Wordle Validator API

A lightweight **FastAPI** project that exposes an endpoint for validating Wordle‑style guesses against the official New York Times answer of the day.

---

## Prerequisites

| Tool   | Tested Version | Purpose              |
| ------ | -------------- | -------------------- |
| Python | **3.11+**      | Runtime              |
| Git    | Latest         | Clone the repository |

> **Tip for Windows users** – run the commands in *PowerShell*.

---

## 🛠 Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/Jordan-Mesches/wordle-server
cd wordle-validator
```

### 2. Create & activate a virtual environment

<details>
<summary>macOS / Linux</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
```

</details>

<details>
<summary>Windows</summary>

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

</details>

### 3. Install dependencies

All requirements are pinned in **requirements.txt**:

```bash
pip install -r requirements.txt
```

### 4. Run the server

`api.py` already contains an embedded Uvicorn runner, so just execute the file:

```bash
python api.py
```

By default the API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Interactive documentation is automatically generated at:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc     → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Reference

| Method & Path                          | Body                   | Description                                                              |
| -------------------------------------- | ---------------------- | ------------------------------------------------------------------------ |
| **POST** `/session`                    | –                      | Creates a new game session. Returns `{ "session_id": "…" }`.             |
| **POST** `/session/{session_id}/guess` | `{ "guess": "crane" }` | Validates a guess. Returns per‑letter feedback and overall `is_correct`. |

Example with HTTPie:

```bash
http POST :8000/session
# -> { "session_id": "01234abcde" }

http POST :8000/session/01234abcde/guess guess=crane
```

---

## 🗂️ Project Layout

```
wordle-validator/
├── api.py              # FastAPI entry‑point (contains uvicorn runner)
├── services.py         # Game logic (validators, models)
├── requirements.txt    # Locked dependencies
└── README.md           # You’re reading it
```

---

## Troubleshooting

| Symptom                  | Fix                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError`    | Activate the virtual environment and ensure `pip install -r requirements.txt` completed without errors. |
| `Address already in use` | Another process is using port 8000. Stop it or run the server on a different port by editing `api.py`.  |

---

## Resources

* FastAPI → [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* Pydantic v2 → [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
* Uvicorn → [https://www.uvicorn.org/](https://www.uvicorn.org/)
