WITH last_line AS (
    SELECT
        money_line.game_id, money_line.sportsbook, money_line.team,
        (
            CASE
                WHEN game.away = money_line.team THEN game.home
                WHEN game.away != money_line.team THEN game.away
            END
        ) AS opp, p.updated, money_line.price, 1 / money_line.price AS imp_prob
    FROM
        money_line
    JOIN
        (
            SELECT
                game_id, sportsbook, team, MAX(updated) as updated
            FROM
                money_line
            GROUP BY game_id, sportsbook, team
        ) p
            ON
        money_line.game_id = p.game_id
            AND
        money_line.sportsbook = p.sportsbook
            AND
        money_line.team = p.team
            AND
        money_line.updated = p.updated
    JOIN
        game
            ON
        game.game_id = money_line.game_id
    WHERE
        game.game_date > datetime('now', '+5 hours')
)
SELECT
    last_line.team, last_line.opp, last_line.sportsbook,
    last_line.updated, last_line.price, last_line.imp_prob, 
    agg_lines.imp_prob, last_line.imp_prob - agg_lines.imp_prob As positive_ev
FROM
    last_line
LEFT JOIN
    (
        SELECT
            game_id, team, AVG(price) as avg_line,
            AVG(1 / price) as imp_prob
        FROM
            last_line
        GROUP BY
            game_id, team
    ) agg_lines
        ON
    last_line.game_id = agg_lines.game_id
        AND
    last_line.team = agg_lines.team
WHERE
    positive_ev > .01
ORDER BY
    positive_ev;