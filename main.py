from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Mock knowledge base for guessing
mock_guesses = [
    {
        "guess": "Elon Musk",
        "conditions": ["living", "human", "alive", "male", "celebrity", "not actor", "inventor"]
    },
    {
        "guess": "Lion",
        "conditions": ["living", "not human", "animal", "wild"]
    },
    {
        "guess": "Taj Mahal",
        "conditions": ["not living", "not human", "place", "India"]
    },
    {
        "guess": "Mufti Ismail Menk",
        "conditions": ["living", "human", "alive", "male", "religious", "Islam"]
    },
]

# Sample follow-up questions
questions_pool = [
    "Is it a living thing?",
    "Is it a human?",
    "Is it male?",
    "Is it a celebrity?",
    "Is it fictional?",
    "Is it an animal?",
    "Is it from the past?",
    "Is it a political figure?",
    "Is it from India?",
    "Is it a religious person?",
    "Is it a place?",
    "Is it a product or invention?",
    "Is it an actor?",
]

asked_questions = set()

class AnswerPayload(BaseModel):
    history: List[str]

@app.post("/next-question")
def next_question(payload: AnswerPayload):
    history = payload.history
    
    if len(history) >= 10:
        # Try to guess based on mock conditions
        for item in mock_guesses:
            if all(condition.lower() in ",".join(history).lower() for condition in item["conditions"]):
                return {"guess": item["guess"], "done": True}
        return {"guess": "I'm not sure. Try again?", "done": True}

    # Pick next unused question
    for q in questions_pool:
        if q not in history:
            asked_questions.add(q)
            return {"question": q, "done": False}

    return {"guess": "Out of questions!", "done": True}
