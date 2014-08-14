drop table f_player cascade;

Create table f_player (
	f_player_id serial primary key,
	f_team_id int,
	on_roster bit,
	foreign key (f_team_id) references f_team(f_team_id)
);

Create TABLE f_def_player(
	f_def_player_id serial primary key,
	team_id varchar(3) not null, 
	f_player_id int not null,
	Foreign Key (team_id) references team(team_id),
	foreign key (f_player_id) references f_player(f_player_id)
);

Create Table f_offense_player(
	f_offense_player_id serial primary key,
	player_id varchar(10) not null,
	f_player_id int not null,
	foreign key (player_id) references player(player_id),
	foreign key (f_player_id) references f_player(f_player_id)
);




	
