from connection import *

# create statement for players
teams_create = """
	CREATE TABLE teams
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(255) NOT NULL
	)
"""

# create statement for players
players_create = """
	CREATE TABLE players
	(
    	id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		total_win INT DEFAULT 0
	)
"""

player_teams_create = """
	CREATE TABLE player_teams
	(
		player_id INT NOT NULL,
		team_id INT NOT NULL,
		PRIMARY KEY (player_id, team_id),
		FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
		FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
	)
"""

# create statement for matches
matches_create = """
	CREATE TABLE matches
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		player1_id INT NOT NULL,
		player2_id INT NOT NULL,
		winner_id INT,
		FOREIGN KEY (player1_id) REFERENCES players(id) ON DELETE CASCADE,
		FOREIGN KEY (player2_id) REFERENCES players(id) ON DELETE CASCADE,
		FOREIGN KEY (winner_id) REFERENCES players(id) ON DELETE SET NULL
	)
"""

# create statement for categories
categories_create = """
	CREATE TABLE categories 
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		player_id INT NOT NULL,
		FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
	);
"""

connector.cur.execute(teams_create)
connector.cur.execute("desc teams")
for i in connector.cur:
	print(i)

connector.cur.execute(players_create)
connector.cur.execute("desc players")
for i in connector.cur:
	print(i)

connector.cur.execute(player_teams_create)
connector.cur.execute("desc player_teams")
for i in connector.cur:
	print(i)

connector.cur.execute(matches_create)
connector.cur.execute("desc matches")
for i in connector.cur:
	print(i)



# finally closing the database connection
connector.close()
