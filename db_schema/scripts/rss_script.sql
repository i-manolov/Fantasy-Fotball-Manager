Create Table rss_data (
        id serial primary key,
        title varchar(256),
        url varchar(256),
        content_1 varchar(1024),
        content_2 varchar(1024),
        rss_id varchar(256),
        timestamp timestamp
);

DROP TABLE IF EXISTS rss_data;

CREATE TABLE yahoo_rss_data (
        id serial primary key,
        title varchar(256),
        url varchar(256),
        content_1 varchar(1024),
        content_2 varchar(1024),
        rss_id varchar(512),
	media_url varchar(512),
	media_inf varchar(1024),
        timestamp timestamp
);

CREATE  TABLE roto_rss_data (
	id serial primary key,
	title varchar(256),
	url varchar(256),
	content_1 varchar(1024),
	rss_id varchar(512),
	timestamp timestamp
);

ALTER TABLE yahoo_rss_data ALTER "content_1" TYPE character varying(2048);
ALTER TABLE yahoo_rss_data ALTER "content_2" TYPE character varying(2048);
ALTER TABLE yahoo_rss_data ALTER "media_inf" TYPE character varying(1024);

CREATE TABLE roto_rss_player_data (
        id serial primary key,
        title varchar(256),
        player_url varchar(256),
        content varchar(1024),
	full_name varchar(512),
	first_name varchar(256),
	last_name varchar(256),
	team_abbr varchar(128),
        rss_id varchar(512),
        timestamp timestamp
);



