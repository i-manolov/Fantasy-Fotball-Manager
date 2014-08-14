Alter Table f_playedforweek
	Drop Constraint f_playedforweek_week_id_fkey,
	Drop Column week_id,
	Add Column week_num smallint not null;

Alter Table week_lookup
	Drop Constraint week_lookup_pkey,
	Drop Column week_id,
	Add Column week_num smallint primary key;
	
Alter table week_lookup add Column start_date date not null;
Alter table week_lookup	Add Column end_date date not null;
	

Create Table f_team_points_per_week(
	f_team_points_per_week_id serial primary key,
	f_team_id int,
	points smallint not null,
	projected_points smallint not null, 
	scoring_type text,
	week_num smallint,
	Foreign Key (f_team_id) REFERENCES f_team(team_id), 
	Foreign Key(week_num) references week_lookup(week_num),
	Constraint f_team_points_per_week_unique UNIQUE(f_team_id, week_num, scoring_type)
	 
);

Create Table f_matchups(
	f_matchup_id serial primary key,
	winner_f_team_id int,
	loser_f_team_id int,
	score int not null,
	week_num smallint, 
	Foreign Key (winner_f_team_id) References f_team(team_id),
	Foreign Key (loser_f_team_id) References f_team(team_id), 
	Foreign Key(week_num) references week_lookup(week_num),
	Constraint f_matchups_unique UNIQUE (winner_f_team_id, loser_f_team_id, week_num)
);

Create Table f_player_points_per_week(
	f_player_points_per_week_id serial primary key,
	player_id varchar(10),
	f_player_id int,
	f_team_id int,
	points smallint,
	week_num smallint,
	Foreign Key (player_id) references player(player_id),
	Foreign Key (f_player_id) references f_player(fplayer_id),
	Foreign Key (f_team_id) references f_team(team_id),
	Foreign Key (week_num) references week_lookup(week_num)
);

Alter table f_player Rename Column fplayer_id to f_player_id;
Alter table f_team Rename Column team_id to f_team_id;
Alter table f_playedforweek Add Column position_played text not null;

