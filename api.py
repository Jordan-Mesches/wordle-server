import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services import ValidWordChecker, WordleValidator

app = FastAPI()

ValidWordChecker.load_from_file("words.txt")

class GuessRequest(BaseModel):
    guess: str

# keeps track of guess attempts
sessions: dict[str: int] = {}

@app.post("/session")
def create_session():
    session_id = uuid.uuid4().hex

    sessions[session_id] = 0

    return {"session_id": session_id}

@app.post("/session/{session_id}/guess")
def make_guess(session_id: str, guess_request: GuessRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if sessions[session_id] >= 6:
        raise HTTPException(status_code=400, detail="Max attempts reached")

    if not ValidWordChecker.check(guess_request.guess):
        raise HTTPException(status_code=400, detail="Not a valid word")

    sessions[session_id] += 1

    return WordleValidator().validate(guess_request.guess)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)