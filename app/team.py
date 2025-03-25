from query.player import *
from query.team import *

def create_team():
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    existing_teams = set(name for _, name, _ in data_teams) if data_teams else set()
    existing_category = list(set(category for _, _, category in data_teams if category != "Uncategorized")) if data_teams else set()

    # Check player data before create new team
    data_players = get_all_players_data()
    if not data_players:
        print("\n⚠️ No players available. Please add players first!")
        return

    print("\n=== Create New Team ===")

    while True:
        print("Please enter team name.")
        print("⚠️ Type 0 to back\n")

        try:
            name_input = input("Enter a new team name: ").strip()
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid name.\n")
            continue

        if name_input == "0":
            break

        # Validate team name
        elif name_input in existing_teams:
            print(f"\n⚠️ Team '{name_input}' already exists! Please choose a different name.\n")

        elif name_input not in existing_teams:
            # Choose team category
            while True:
                print()
                print_teams(existing_category, "category")
                print("⚠️ Type 0 to cancel\n")

                try:
                    category_input = int(input("Choose category: ").strip())
                except ValueError:
                    print("\n❌ Invalid input! Please enter a valid number.\n")
                    continue

                if category_input == 0:
                    print()
                    break

                elif not (1 <= category_input <= len(existing_category)+1):
                    print("\n❌ Invalid selection. Please choose a number from the list!")
                    continue

                # Commit new teams to the database
                elif category_input:
                    if category_input == len(existing_category)+1:
                        # Create new category
                        category_name = input("Enter a category name: ").strip()
                    else:
                        # Select existing category
                        category_name = existing_category[category_input - 1]
                    connector.cur.execute(query_insert_team, (None, name_input, category_name))
                    connector.commit()
                    print(f"\n✅ Finished adding {name_input} as {category_name}.")
                    return


def assign_player():
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
        print("\n=== Assign Player ===")
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
                    # Get actual team data
                    team_id, team_name, team_category = available_teams[team_input - 1]

                    connector.cur.execute(query_insert_player_team, (player_id, team_id))
                    connector.commit()
                    print(f"\n✅ Player '{player_name}' assigned to '{team_name}' successfully!.")
                    return

def view_teams():
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    team_input = 0

    if not data_teams:
        print("\n⚠️ No teams available. Please create team first!")
        return

    ## Player section
    print("\n============ Team List ============")
    print_teams(data_teams)
    print("⚠️ Type 0 to back")

    # Choose team
    try:
        team_input = int(input(f"\nChoose Team: ").strip())
    except ValueError:
        print("\n❌ Invalid input! Please enter a valid number.")

    if team_input == 0:
        return
    elif not (1 <= team_input <= len(data_teams)):
        print("\n❌ Invalid selection. Please choose a number from the list!\n")
    else:
        # Get actual team ID and name
        team_id, team_name, team_category = data_teams[team_input - 1]

        # Get players from selected team
        print()
        data_team_players = get_team_players(team_id)
        if data_team_players:
            print_players(data_team_players, "team", team_name)
        else:
            print(f'❌ No players are assigned in team {team_name}!')

def search_teams():
    print()
    search_input = input("Enter team name to search: ").strip()
    team_name = get_teams_by_search(search_input)
    print()

    if team_name:
        print_teams(team_name, "search")
    else:
        print("No teams found.")

def rename_team():
    # Get existing teams from the database
    data_teams = get_all_teams_data()
    print(data_teams)
    existing_teams = set(name for _, name, _ in data_teams) if data_teams else set()

    if not data_teams:
        print("\n⚠️ No teams available. Please add teams first!")
        return

    while True:
        print("\n=========== Rename Team ===========")
        print_teams(data_teams)
        print("⚠️ Type 0 to back")

        try:
            index_input = int(input("\nChoose team to rename: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.")
            continue

        if index_input == 0:
            break
        elif not (1 <= index_input <= len(data_teams)):
            print("\n❌ Invalid selection. Please choose a number from the list!")
        else:
            # Get actual team ID and name
            team_id, team_name, team_category = data_teams[index_input - 1]

            print(f"\nTeam '{team_name}' selected!")
            print("⚠️ Type 0 to back")

            while True:
                new_name_input = input("\nEnter new team name: ").strip()

                if new_name_input == team_name:
                    print("\n⚠️ Team's name can't be same!")

                elif new_name_input == "":
                    print("\n⚠️ Team's name can't be empty!")

                # Cancel operation
                elif new_name_input == "0":
                    print("\n⚠️ No teams were added.")
                    break

                # Validate team name
                elif new_name_input in existing_teams:
                    print(f"\n⚠️ Team '{new_name_input}' already exists! Please choose a different name.")

                else:
                    # Rename team to the database
                    connector.cur.execute(query_rename_team, (new_name_input, team_id))
                    connector.commit()
                    print(f"\n✅ Team '{team_name}' successfully changed name to '{new_name_input}'")
                break
            break
    return

def delete_team():
    # Get all teams
    data_teams = get_all_teams_data()

    if not data_teams:
        print("\n⚠️ No teams available. Please add teams first!")
        return

    while True:
        print("\n=========== Delete Team ===========")

        print_teams(data_teams)
        print("⚠️ Type 0 to back")

        try:
            index_input = int(input("\nChoose team to delete: ").strip())
        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.\n")
            continue

        if index_input == 0:
            break
        elif not (1 <= index_input <= len(data_teams)):
            print("\n❌ Invalid selection. Please choose a number from the list!\n")
        else:
            # Get actual team ID and name
            team_id, team_name, team_category = data_teams[index_input - 1]

            # Delete team from database
            connector.cur.execute(query_delete_team, (team_id,))
            connector.commit()

            print(f"\n✅ Team '{team_name}' deleted successfully!")
            break

"""
TO DO

- [Create New Team]
    - Choose Category or skip

"""