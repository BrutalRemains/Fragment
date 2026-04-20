from services.startup import create_or_load_creature, create_and_save_creature

# fairly simple CLI for interacting with the creature. The llm will have some agency
# reducing the amount of input needed from the user from a code perspective, but the user will still have a lot of freedom  
def user_manual():
    print("Welcome to the NeuroPet user manual!")
    print("")
    print("In this manual, you'll learn how to interact with your virtual creature and take care of its needs.")
    print("")
    print("1. Interacting with Your Creature:")
    print("- You can talk to your creature by typing messages in the chat. Your creature will respond based on its current mood and needs.")
    print("- Your creature will also respond according to the species you chose.")
    print("- You can ask your creature about its feelings, memories, or tricks it knows.")
    print("- You may also give your creature commands. Refer to the command section for specific commands")
    print("")  

def chat():  
    load_creature_data = create_or_load_creature()
     
    if load_creature_data is None:
        print("Hello! Welcome to NeuroPet!")
        print("")
        print("Let's start by creating your creature.")
        print("First, let's choose a species for your creature.")
        print("It can be anything you like! The species you choose will influence your creature's behavior")
        species = input("What species would you like your creature to be? ")
        while species.strip() == "":
            species = input("What species would you like your creature to be? ")
            if species.strip() == "":
                continue
        name = input("What would you like to name your creature? ")
        while name.strip() == "":
            name = input("What would you like to name your creature? ")
            if name.strip() == "":
                continue
        creature = create_and_save_creature(name, species)
        print(f"Great! You've created a {species} named {name}.")
        print("Now, let's interact with your creature! You can feed it, play with it, or just talk to it.")

    else:
            creature = create_or_load_creature()
    
    running = True
    while running:
        print("")
        print(f"{creature.name} is waiting to hang out with you!")
        print("Please type \"c\" to continue to your creature, \"m\" to view the user manual, or \"q\" to quit.")
        choice = input("Your choice: ").strip().lower()
        if choice == "c":
            # Continue to interact with the creature
            pass
        elif choice == "m":
            user_manual()
        elif choice == "q":
            running = False
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    chat()
