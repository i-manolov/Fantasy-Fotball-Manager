create table f_team_owner(
	user_id int not null, 
	f_team_id int not null,
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (f_team_id) REFERENCES f_team(team_id), 
	CONSTRAINT uniqueTeamOwner UNIQUE (user_id, f_team_id)
);