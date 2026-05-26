from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from data.database import load_creature, save_creature
from services.generate_reply import generate_reply
from services.startup import create_or_load_creature

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.get("/creature/{creature_id}")
def get_creature_endpoint(creature_id: int, q: str = None):
    creature = load_creature()
    if creature:
        return {"creature_id": creature_id, "creature": creature, "q": q}
    return {"error": "Creature not found"}

@app.post("/creature/")
def create_creature(creature_id: int, name: str, description: str):
    save_creature(creature_id, name, description)
    return {"message": "Creature saved successfully", "creature_id": creature_id}

@app.post("/chat")
def chat(payload: dict):
    user_input = payload.get("message", "")
    if not user_input:
        return {"success": False}
    
    creature = create_or_load_creature()  # Load creature data from the database
    response = generate_reply(creature, user_input)  # Generate response based on user input and creature data
    save_creature(creature)  # Save updated creature data back to the database
    return {
        "reply": response["reply"],
        "creature_stats": {
            "energy": creature.energy,
            "happiness": creature.happiness,
            "fullness": creature.fullness
        }
    }

# all of our creature methods are set up to return appropriate responses
@app.post("/feed")
def feed():
    creature = create_or_load_creature()
    result = creature.feed()
    save_creature(creature)
    return result

@app.post("/play")
def play():
    creature = create_or_load_creature()
    result = creature.play()
    save_creature(creature)
    return result

@app.post("/rest")
def rest():
    creature = create_or_load_creature()
    result = creature.rest()
    save_creature(creature)
    return result