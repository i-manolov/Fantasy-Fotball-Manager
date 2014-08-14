alter table f_playedforweek drop column played ;
alter table f_playedforweek drop column position_played;
Alter table f_playedforweek rename to f_played_for_week; 
Alter table f_played_for_week add column selected_position text; 
Alter table f_played_for_week add column display_position text;
alter table f_played_for_week rename fplayed_id to f_played_id;

