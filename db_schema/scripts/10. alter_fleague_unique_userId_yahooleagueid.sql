ALTER TABLE f_league DROP CONSTRAINT uniqueyahoo_league_id;

ALTER TABLE f_league ADD CONSTRAINT uniquefleague UNIQUE (user_id, yahoo_league_id);