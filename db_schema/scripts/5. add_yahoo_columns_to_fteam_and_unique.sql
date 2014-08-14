ALTER TABLE f_team ADD COLUMN yahoo_team_id int not null; 
ALTER TABLE f_team ADD COLUMN yahoo_team_url text not null; 
ALTER TABLE f_team ADD COLUMN yahoo_team_logo text; 
ALTER TABLE f_team ADD COLUMN yahoo_manager_guid text not null;
ALTER TABLE f_team ADD COLUMN yahoo_manager_name text not null;
ALTER TABLE f_team ADD COLUMN yahoo_manager_id int not null; 


ALTER TABLE F_Team DROP CONSTRAINT uniqueTeam ;
ALTER TABLE f_team ADD CONSTRAINT uniqueTeam UNIQUE (league_id, yahoo_team_id)



