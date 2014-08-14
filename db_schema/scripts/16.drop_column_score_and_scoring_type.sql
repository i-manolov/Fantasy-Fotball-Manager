alter table f_matchups drop column score;
alter table f_matchups	rename column winner_f_team_id to opponent1_f_team_id;
alter table f_matchups	rename column loser_f_team_id to opponent2_f_team_id;
alter table f_team_points_per_week drop column scoring_type; 
