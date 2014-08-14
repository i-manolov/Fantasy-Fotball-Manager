create table yahoo_user_guid (
	user_id int not null,
	yahoo_guid text not null UNIQUE,
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
);