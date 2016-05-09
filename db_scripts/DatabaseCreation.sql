CREATE TABLE player (
    id integer NOT NULL,
    leaguename text NOT NULL,
	region text NOT NULL,
	email text,
	password text NOT NULL,
    iconid integer,
	verified boolean DEFAULT FALSE,
    leagueid integer NOT NULL,
	wins integer DEFAULT 0,
	winstreak integer DEFAULT 0,
	losestreak integer DEFAULT 0,
	minion integer DEFAULT 0,
	wardkills integer DEFAULT 0,
	wardplaced integer DEFAULT 0,
	kills integer DEFAULT 0,
	deaths integer DEFAULT 0,
	assists integer DEFAULT 0,
	gold integer DEFAULT 0,
	largestkillingspree integer DEFAULT 0,
	csperminute real DEFAULT 0.0,
	highestcrit integer DEFAULT 0,
	ccduration integer DEFAULT 0,
	gamemodewins integer DEFAULT 0,
	earliestkill integer DEFAULT 0,
	earliestturret integer DEFAULT 0,
	earliest200cs integer DEFAULT 0,
	stealthamount integer DEFAULT 0,
	voidamount integer DEFAULT 0,
	yordleamount integer DEFAULT 0,
	teemoamount integer DEFAULT 0,
	teemowin integer DEFAULT 0,
	champpoints integer DEFAULT 0,
	points integer DEFAULT 0
);

CREATE TABLE achievement (
	id serial NOT NULL,
	name text,
	description text,
	points integer,
	evaluation text
);

CREATE TABLE repeatable (
	id serial NOT NULL,
	name text,
	description text,
	points integer,
	evaluation text
);

CREATE TABLE halloffame (
	id serial NOT NULL,
	name text,
	description text,
	pointsfirst integer DEFAULT 20,
	pointssecond integer DEFAULT 10,
	pointsthird integer DEFAULT 5,
	evaluation text
);

CREATE TABLE game (
	id bigint NOT NULL,
	playerid integer NOT NULL,
	region text NOT NULL,
	json text
);

CREATE TABLE champion (
	id integer NOT NULL,
	name text,
	ftp boolean,
	yordle boolean,
	stealth boolean,
	void boolean
);

CREATE TABLE player_achievement_match (
	playerid integer NOT NULL,
	region text NOT NULL,
	achievementid integer NOT NULL,
	gameid bigint NOT NULL
);

CREATE TABLE player_repeatable (
	playerid integer NOT NULL,
	region text NOT NULL,
	repeatableid integer NOT NULL,
	amount integer DEFAULT 0,
);

CREATE TABLE player_halloffame (
	playerid integer NOT NULL,
	region text NOT NULL,
	hofid integer NOT NULL,
	place integer
);

CREATE TABLE game_repeatable_player (
	playerid integer NOT NULL,
	region text NOT NULL,
	repeatableid integer NOT NULL,
	gameid bigint NOT NULL
);

CREATE TABLE player_champion (
	playerid integer NOT NULL,
	region text NOT NULL,
	championid integer NOT NULL,
	amount integer DEFAULT 0
);

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id,region);

ALTER TABLE ONLY achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (id);

ALTER TABLE ONLY repeatable
    ADD CONSTRAINT repeatable_pkey PRIMARY KEY (id);

ALTER TABLE ONLY halloffame
    ADD CONSTRAINT halloffame_pkey PRIMARY KEY (id);

ALTER TABLE ONLY champion
    ADD CONSTRAINT champion_pkey PRIMARY KEY (id);

ALTER TABLE ONLY game
	ADD CONSTRAINT game_pkey PRIMARY KEY (id, playerid, region);

ALTER TABLE ONLY game
    ADD CONSTRAINT game_playerid_fkey FOREIGN KEY (playerid) REFERENCES player(id);

ALTER TABLE ONLY game
    ADD CONSTRAINT game_region_fkey FOREIGN KEY (region) REFERENCES player(region);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_pkey PRIMARY KEY (playerid,region,achievementid,gameid);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_pkey PRIMARY KEY (playerid,region,repeatableid);

ALTER TABLE ONLY player_halloffame
    ADD CONSTRAINT player_halloffame_pkey PRIMARY KEY (playerid,region,hofid);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_pkey PRIMARY KEY (playerid,region,repeatableid,gameid);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_pkey PRIMARY KEY (playerid,region,championid);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_playerid_fkey FOREIGN KEY (playerid) REFERENCES player(id);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_region_fkey FOREIGN KEY (region) REFERENCES player(region);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_achievementid_fkey FOREIGN KEY (achievementid) REFERENCES achievement(id);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_gameid_fkey FOREIGN KEY (gameid) REFERENCES game(id);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_playerid_fkey FOREIGN KEY (playerid) REFERENCES player(id);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_region_fkey FOREIGN KEY (region) REFERENCES player(region);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_repeatableid_fkey FOREIGN KEY (repeatableid) REFERENCES repeatable(id);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_playerid_fkey FOREIGN KEY (playerid) REFERENCES player(id);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_region_fkey FOREIGN KEY (region) REFERENCES player(region);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_repeatableid_fkey FOREIGN KEY (repeatableid) REFERENCES repeatable(id);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_gameid_fkey FOREIGN KEY (gameid) REFERENCES game(id);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_playerid_fkey FOREIGN KEY (playerid) REFERENCES player(id);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_region_fkey FOREIGN KEY (region) REFERENCES player(region);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_championid_fkey FOREIGN KEY (championid) REFERENCES champion(id);
