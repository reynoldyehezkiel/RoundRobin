SELECT
	m.id,
    m.player1_id, p1.name AS player1_name,
    m.player2_id, p2.name AS player2_name,
    m.winner_id, p_win.name AS winner_name
FROM matches m
JOIN players p1 ON m.player1_id = p1.id
JOIN players p2 ON m.player2_id = p2.id
JOIN players p_win ON m.winner_id = p_win.id