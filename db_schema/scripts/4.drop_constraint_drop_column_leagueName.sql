ALTER TABLE f_league DROP CONSTRAINT uniqueLeagueName;

ALTER TABLE f_league DROP COLUMN league_name;

ALTER TABLE f_league ADD CONSTRAINT uniqueYahoo_league_id UNIQUE (yahoo_league_id);