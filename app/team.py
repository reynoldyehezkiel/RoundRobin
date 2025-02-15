from query.player import *
from query.match import *
from query.team import *

def create_team():
    print("\n🛠️ This feature is in development")
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    existing_teams = set(name for _, name in data_teams) if data_teams else set()

    print("\n=== Create Team ===")
    print("Please enter team name.")
    print("⚠️ Type 0 to back\n")

    while True:
        # Asking for team name
        name_input = input("Enter a team name: ").strip()

        # Validate team name
        if name_input in existing_teams:
            print(f"\n⚠️ Team '{name_input}' already exists! Please choose a different name.\n")

        # Cancel operation
        elif name_input == "0":
            break

        # Commit new teams to the database
        elif name_input not in existing_teams:
            connector.cur.execute(query_insert_team, (None,name_input))
            connector.commit()
            print(f"\n✅ Finished adding {name_input}.")
            break



def view_team():
    print("\n🛠️ This feature is in development")

"""
    - Main Menu
        1. Create team ✅
        2. Assign players to teams 🛠️
        3. View team and its players 🛠️
    
    - Add New Player
        1. If team exists:
            a. Choose team 🛠️
        2. If team doesn't exist:
            a. Ask to create team 🛠️
            b. May not choose team (skip) 🛠️
"""