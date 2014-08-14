ALTER TABLE f_player_points_per_week DROP COLUMN player_id;
ALTER TABLE f_player_points_per_week DROP COLUMN f_team_id;
ALTER TABLE f_player_points_per_week drop column points;
Alter table f_player_points_per_week add column points numeric(5,2);
ALTER TABLE f_player add column offense boolean;
