import datetime
from enum import Enum

# simple enum for any switching on the state of the creature, 
# emotionally or "physically" so to speak
class CreatureState(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    TIRED = "tired"
    HUNGRY = "hungry"

# the foundation of the creature itself
class Creature:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
        # all needs set to a base value of 100, decreases over time
        self.energy = 100
        self.hunger = 100
        self.happiness = 100

        # starts newborn, will age in realtime
        self.age = 0
        
        # lists for storing necessary information regarding the creature's experience
        self.memory = []
        self.known_tricks = []

        # necessary for tracking the creature's state and interactions
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()

    def initial_prompt(self):
        prompt = f""" 
        You are a {self.species}
        Your name is {self.name}
        Your current mood is {self.mood}
        Your current energy level is {self.energy}
        Your current hunger level is {self.hunger}
        """
        return prompt

    def age_one_day(self):
        now = datetime.now()
        # if a day has passed since the creature was created, 
        # age it and decrease needs. time will decay needs, actions will improve them
        if now - self.created_at >= datetime.timedelta(days=1):
            self.age += 1
            self.energy -= 5
            self.hunger -= 5
            self.happiness -= 2

    def feed(self):
        self.hunger += 20
        if self.hunger > 100:
            self.hunger = 100
        self.last_interaction = datetime.now()