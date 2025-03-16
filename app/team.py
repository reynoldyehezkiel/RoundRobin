from query.player import *
from query.match import *
from query.team import *

def create_team():
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    existing_teams = set(name for _, name in data_teams) if data_teams else set()

    # Check player data before create new team
    data_players = get_all_players_data()
    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    print("\n=== Create New Team ===")
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
            print(f"\n✅ Finished adding {name_input}.\n")

def assign_player_to_team():
    # Get existing players & teams from the database
    data_players = get_all_players_data()
    data_teams = get_all_teams_data()

    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    if not data_teams:
        print("\n⚠️ No teams available. Please create team first!")
        return

    while True:
        ## Player section
        print("\n=== Assign Player to Team ===")
        print_players(data_players)
        print("⚠️ Type 0 to back")

        # Choose player
        try:
            player_input = int(input("\nChoose player to assign: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.\n")
            continue

        if player_input == 0:
            break
        elif not (1 <= player_input <= len(data_players)):
            print("\n❌ Invalid selection. Please choose a number from the list!\n")
            continue
        else:
            # Get actual player ID and name
            player_id, player_name = data_players[player_input - 1]

            # Get available teams
            available_teams = get_available_teams(player_id)
            while True:
                ## Team section
                print_teams(available_teams)
                print("⚠️ Type 0 to back")

                # Choose team
                try:
                    team_input = int(input(f"\nChoose Team for '{player_name}': ").strip())
                except ValueError:
                    print("\n❌ Invalid input! Please enter a valid number.\n")
                    continue

                if team_input == 0:
                    break
                elif not (1 <= team_input <= len(available_teams)):
                    print("\n❌ Invalid selection. Please choose a number from the list!\n")
                    continue
                else:
                    # Get actual team ID and name
                    team_id, team_name = available_teams[team_input - 1]

                    connector.cur.execute(query_insert_player_team, (player_id, team_id))
                    connector.commit()
                    print(f"\n✅ Player '{player_name}' assigned to '{team_name}' successfully!.")
                    return

def view_team():
    print("\n🛠️ This feature is in development")

"""
    - Main Menu
        1. Create team ✅
        2. Assign players to teams 🛠️
        3. View team and its players ❌
    
    - Add New Player
        1. If team exists:
            a. Assign team ❌
            b. May not choose team (skip) ❌
        2. If team doesn't exist:
            a. Ask to create team first from main menu. ❌
"""