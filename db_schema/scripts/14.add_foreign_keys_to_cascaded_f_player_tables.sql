alter table f_playedforweek 
	add constraint fplayerforweek_f_player_id_fk Foreign Key (fplayer_id) references f_player(f_player_id);
alter table f_player_points_per_week 
	add constraint f_player_points_per_week_f_player_id_fk foreign key(f_player_id) references f_player(f_player_id);

alter table f_playedforweek rename column fplayer_id to f_player_id;