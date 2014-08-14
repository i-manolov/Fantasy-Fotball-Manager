ALTER Table Users ADD CONSTRAINT uniqueUserName UNIQUE (user_name) ;

Alter Table Users ADD CONSTRAINT uniqueEmail UNIQUE (email);

ALTER TABLE F_League ADD CONSTRAINT uniqueLeagueName UNIQUE (league_name);

ALTER TABLE F_Team ADD CONSTRAINT uniqueTeam UNIQUE (league_id, team_name);

ALTER TABLE F_Player ADD CONSTRAINT uniquePlayer UNIQUE (player_id, team_id);

ALTER TABLE F_PlayedForWeek ADD CONSTRAINT uniquePlayedForWeek UNIQUE (fplayer_id, week_id);

ALTER TABLE USERS 
	alter column first_name set not null,
	alter column last_name set not null,
	alter column user_name set not null,
	alter column password set not null,
	alter column email set not null;

ALTER TABLE F_League
	alter column user_id set not null,
	alter column league_name set not null;

ALTER TABLE F_Team
	alter column league_id set not null,
	alter team_name set not null;

ALTER TABLE F_Player
	alter column player_id set not null,
	alter column team_id set not null;
	
Alter Table week_lookup
	alter column week_description set not null;

Alter Table f_playedforweek 
	alter column fplayer_id set not null,
	alter column week_id set not null,
	alter column played set not null;