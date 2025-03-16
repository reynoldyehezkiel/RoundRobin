from query.player import *
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

    name_input = input("Enter a team name: ").strip()

    # Validate team name
    if name_input in existing_teams:
        print(f"\n⚠️ Team '{name_input}' already exists! Please choose a different name.\n")

    # Commit new teams to the database
    elif name_input not in existing_teams:
        connector.cur.execute(query_insert_team, (None,name_input))
        connector.commit()
        print(f"\n✅ Finished adding {name_input}.")

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
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    team_input = 0

    if not data_teams:
        print("\n⚠️ No teams available. Please create team first!")
        return

    ## Player section
    print("\n=== Team List ===")
    print_teams(data_teams)
    print("⚠️ Type 0 to back")

    # Choose team
    try:
        team_input = int(input(f"\nChoose Team: ").strip())
    except ValueError:
        print("\n❌ Invalid input! Please enter a valid number.")

    if not (1 <= team_input <= len(data_teams)):
        print("\n❌ Invalid selection. Please choose a number from the list!\n")
    else:
        # Get actual team ID and name
        team_id, team_name = data_teams[team_input - 1]

        # Get players from selected team
        print()
        data_team_players = get_team_players(team_id)
        if data_team_players:
            print_players(data_team_players, "team", team_name)
        else:
            print(f'❌ No players are assigned in team {team_name}!')

def rename_team():
    return

def delete_team():
    return
