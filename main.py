import src.agents.routing_agent as agent
import argparse
from src.utils.populate_database import populate_database

parser = argparse.ArgumentParser()
parser.add_argument("--reset", action="store_true", help="Reset the database.")
parser.add_argument("--update", action="store_true", help="Update the database with new documents.")
args = parser.parse_args()

if args.update:
    populate_database()
elif args.reset:
    populate_database(True)

print("\n\nEnter 'exit' or 'bye' to quit")

while True:
    user_prompt = input("User: ")
    if (user_prompt.lower() != "exit" and user_prompt.lower() != "bye"):
        agent.super_agent(user_prompt)
        print("")
    else:
        print("Goodbye! (AI can also make mistakes sometimes)")
        break
