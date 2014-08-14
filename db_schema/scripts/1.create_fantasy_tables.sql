Create Table Users (
	user_id serial primary key,
	first_name varchar(100),
	last_name varchar(100),
	email varchar(100),
	user_name varchar(100),
	password varchar(100),
	last_sign_out timestamp
);

Create Table F_League(
	league_id serial primary key,
	user_id int, 
	league_name varchar(100),
	Foreign KEY (user_id) REFERENCES Users(user_id)
);

Create Table F_Team(
	team_id serial primary key,
	league_id int,
	team_name varchar(100),
	FOREIGN KEY (league_id) REFERENCES F_League(league_id)
);

Create Table F_Player(
	fplayer_id serial primary key,
	player_id varchar(10),
	team_id int,
	FOREIGN KEY (player_id) REFERENCES Player(player_id),
	FOREIGN KEY (team_id) REFERENCES F_Team(team_id)
);

Create Table Week_LookUp(
	week_id serial primary key,
	week_description varchar(50)
);

Create Table F_PlayedForWeek(
	fplayed_id serial primary key,
	fplayer_id int,
	week_id int,
	played bit,
	FOREIGN KEY (fplayer_id) REFERENCES F_Player(fplayer_id),
	FOREIGN KEY (week_id) REFERENCES Week_LookUp(week_id)
);