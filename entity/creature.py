from datetime import datetime, timedelta
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
        self.fullness = 100
        self.happiness = 100

        # starts newborn, will age in realtime
        self.age = 0
        
        # lists for storing necessary information regarding the creature's experience
        self.memory = []
        self.known_tricks = []

        # necessary for tracking the creature's state and interactions
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()
        self.last_decay_check = datetime.now()

    def calculate_mood(self):
        if self.energy < 30:
            return CreatureState.TIRED
        elif self.fullness < 30:
            return CreatureState.HUNGRY
        elif self.happiness < 30:
            return CreatureState.SAD
        elif self.happiness > 70:
            return CreatureState.HAPPY
        else:
            return CreatureState.ANGRY

    # this tells the language model what it needs to know to "stay in character"
    def initial_prompt(self):
        mood = self.calculate_mood()
        prompt = f""" 
        You are a {self.species}
        Your name is {self.name}
        You are currently {self.age} days old
        
        Current Status:
        Your current mood is {mood.value}
        Your current energy level is {self.energy}
        Your current fullness level is {self.fullness}
        Your current happiness level is {self.happiness}

        Recent memories: {', '.join(self.memory[-3:]) if self.memory else 'none yet'}
        Tricks you know: {', '.join(self.known_tricks) if self.known_tricks else 'none yet'}
        """
        return prompt

    def age_one_day(self):
        # adjust all values based on the time passed since the last decay check, this allows for real-time aging and decay of needs
        now = datetime.now()
        days_passed = (now - self.last_decay_check).days
        if days_passed >= 1:

            self.age += days_passed
            self.energy = max(0, self.energy - (5 * days_passed))
            self.fullness = max(0, self.fullness - (5 * days_passed))
            self.happiness = max(0, self.happiness - (2 * days_passed))
            self.last_decay_check += timedelta(days=days_passed)

    def feed(self):
        self.fullness += 20
        if self.fullness > 100:
            self.fullness = 100
        self.last_interaction = datetime.now()

    def play(self):
        self.happiness += 20
        if self.happiness > 100:
            self.happiness = 100
        self.energy -= 10
        if self.energy < 0:
            self.energy = 0
        self.last_interaction = datetime.now()