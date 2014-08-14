ALTER TABLE f_league ADD COLUMN yahoo_league_id int  NOT NUll;
ALTER TABLE f_league ADD COLUMN start_date date  not null;
ALTER TABLE f_league ADD COLUMN end_date date  not null; 
ALTER TABLE f_league ADD COLUMN num_teams date  not null; 
ALTER TABLE f_league ADD COLUMN league_url text NOT NULL;