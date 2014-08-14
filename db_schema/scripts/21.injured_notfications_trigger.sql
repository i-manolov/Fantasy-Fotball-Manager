CREATE TABLE nfl_player_update_status
(
  status_update_id serial primary key,
  nfl_player_id text,
  old_status text NOT NULL,
  new_status text NOT NULL,
  date timestamp NOT NULL,
  FOREIGN KEY (nfl_player_id) REFERENCES player (player_id) 
);


Create function update_player_status() 
	RETURNS trigger AS $$
	BEGIN
	INSERT INTO nfl_player_update_status(nfl_player_id,old_status, new_status, date) values
		(NEW.player_id,OLD.status, New.status, now());
	RETURN NEW;
	END;
	$$ Language plpgsql;

Create Trigger update__player_status 
AFTER UPDATE on player
FOR EACH ROW 
WHEN (OLD.status is distinct from NEW.status)
EXECUTE Procedure update_player_status();