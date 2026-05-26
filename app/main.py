from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from data.database import get_creature, save_creature

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.get("/creature/{creature_id}")
def get_creature_endpoint(creature_id: int, q: str = None):
    creature = get_creature(creature_id)
    if creature:
        return {"creature_id": creature_id, "creature": creature, "q": q}
    return {"error": "Creature not found"}

@app.post("/creature/")
def create_creature(creature_id: int, name: str, description: str):
    save_creature(creature_id, name, description)
    return {"message": "Creature saved successfully", "creature_id": creature_id}