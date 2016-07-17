--------------------------
-- Game relevant tables --
--------------------------
CREATE TABLE player (
    id integer NOT NULL,
    leaguename text NOT NULL,
	region text NOT NULL,
    iconid integer,
    leagueid integer,
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
	amount integer DEFAULT 0
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
    ADD CONSTRAINT player_pkey PRIMARY KEY (id, region);

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
    ADD CONSTRAINT game_playerid_region_fkey FOREIGN KEY (playerid, region) REFERENCES player(id, region);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_pkey PRIMARY KEY (playerid, region, achievementid, gameid);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_pkey PRIMARY KEY (playerid, region, repeatableid);

ALTER TABLE ONLY player_halloffame
    ADD CONSTRAINT player_halloffame_pkey PRIMARY KEY (playerid, region, hofid);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_pkey PRIMARY KEY (playerid, region, repeatableid, gameid);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_pkey PRIMARY KEY (playerid, region, championid);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_gameid_playerid_region_fkey FOREIGN KEY (gameid, playerid, region) REFERENCES game(id, playerid, region);

ALTER TABLE ONLY player_achievement_match
    ADD CONSTRAINT player_achievement_match_achievementid_fkey FOREIGN KEY (achievementid) REFERENCES achievement(id);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_playerid_region_fkey FOREIGN KEY (playerid, region) REFERENCES player(id, region);

ALTER TABLE ONLY player_repeatable
    ADD CONSTRAINT player_repeatable_repeatableid_fkey FOREIGN KEY (repeatableid) REFERENCES repeatable(id);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_gameid_playerid_region_fkey FOREIGN KEY (gameid, playerid, region) REFERENCES game(id, playerid, region);

ALTER TABLE ONLY game_repeatable_player
    ADD CONSTRAINT game_repeatable_player_repeatableid_fkey FOREIGN KEY (repeatableid) REFERENCES repeatable(id);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_playerid_region_fkey FOREIGN KEY (playerid, region) REFERENCES player(id, region);

ALTER TABLE ONLY player_champion
    ADD CONSTRAINT player_champion_championid_fkey FOREIGN KEY (championid) REFERENCES champion(id);

--------------------------------------------------
-- Authentication relevant tables and functions --
--------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS basic_auth;

CREATE TABLE basic_auth.users (
    leaguename text NOT NULL,
    region text NOT NULL,
    -- email text NOT NULL CHECK ( email ~* '^.+@.+\..+$' ),
    pass text NOT NULL CHECK (length(pass) < 72),
    role name NOT NULL CHECK (length(role) < 72)
);

ALTER TABLE basic_auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (leaguename, region);

DROP type IF EXISTS basic_auth.jwt_claims CASCADE;
CREATE type basic_auth.jwt_claims AS (role text, id integer, region text);

DROP type IF EXISTS current_id_type CASCADE;
CREATE type current_id_type AS (id text, region text);

CREATE OR REPLACE FUNCTION basic_auth.check_role_exists() RETURNS TRIGGER
    LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles AS r WHERE r.rolname = new.role) THEN
        RAISE foreign_key_violation USING message =
            'unknown database role: ' || new.role;
        RETURN NULL;
    END IF;
    return new;
END;
$$;

CREATE OR REPLACE FUNCTION basic_auth.encrypt_pass() RETURNS TRIGGER
    LANGUAGE plpgsql AS $$
BEGIN
    IF tg_op = 'INSERT' OR new.pass <> old.pass THEN
        new.pass = crypt(new.pass, gen_salt('bf'));
    END IF;
    return new;
END;
$$;

CREATE OR REPLACE FUNCTION basic_auth.user_role(leaguename text, region text, pass text) RETURNS name
    LANGUAGE plpgsql AS $$
BEGIN
    return (
        SELECT role
        FROM basic_auth.users
        WHERE users.leaguename = user_role.leaguename
        AND users.region = user_role.region
        AND users.pass = crypt(user_role.pass, users.pass)
    );
END;
$$;

CREATE OR REPLACE FUNCTION basic_auth.match_id(leaguename text, region text) RETURNS integer
    LANGUAGE plpgsql AS $$
BEGIN
    return (
        SELECT player.id
        FROM player
        WHERE player.leaguename = match_id.leaguename
        AND player.region = match_id.region
    );
END;
$$;

CREATE OR REPLACE FUNCTION signup(leaguename text, region text, pass text) RETURNS void
AS $$
    INSERT INTO basic_auth.users (leaguename, region, pass, role) VALUES
        (lower(signup.leaguename), lower(signup.region), signup.pass, 'player');
$$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION login(leaguename text, region text, pass text) RETURNS basic_auth.jwt_claims
    LANGUAGE plpgsql AS $$
DECLARE
    _role name;
    _id integer;
    result basic_auth.jwt_claims;
BEGIN
    SELECT basic_auth.user_role(lower(leaguename), lower(region), pass) INTO _role;
    IF _role IS NULL THEN
        RAISE invalid_password USING message = 'invalid user or password';
    END IF;

    SELECT basic_auth.match_id(lower(leaguename), lower(region)) INTO _id;
    IF _id IS NULL THEN
        RAISE invalid_password USING message = 'either not verified or data not built yet';
    END IF;
    SELECT _role AS role, _id AS id, lower(login.region) AS region INTO result;
    return result;
END;
$$;

ALTER DATABASE luc SET postgrest.claims.id TO '';
ALTER DATABASE luc SET postgrest.claims.region TO '';
CREATE OR REPLACE FUNCTION current_id() RETURNS current_id_type
    LANGUAGE plpgsql AS $$
BEGIN
    return (
        current_setting('postgrest.claims.id'),
        current_setting('postgrest.claims.region')
    );
END;
$$;

DROP TRIGGER IF EXISTS ensure_user_role_exists on basic_auth.users;
CREATE CONSTRAINT TRIGGER ensure_user_role_exists
    AFTER INSERT OR UPDATE ON basic_auth.users
    FOR EACH ROW
    EXECUTE PROCEDURE basic_auth.check_role_exists();

DROP TRIGGER IF EXISTS encrypt_pass ON basic_auth.users;
CREATE TRIGGER encrypt_pass
    BEFORE INSERT OR UPDATE ON basic_auth.users
    FOR EACH ROW
    EXECUTE PROCEDURE basic_auth.encrypt_pass();

CREATE OR REPLACE VIEW users AS
SELECT '***'::text AS pass, role, leaguename, region
FROM basic_auth.users;

CREATE ROLE player;
CREATE ROLE anon;

GRANT USAGE ON SCHEMA basic_auth, public TO anon;
GRANT SELECT ON users TO anon;
GRANT INSERT ON TABLE basic_auth.users TO anon;
GRANT SELECT ON TABLE basic_auth.users, player TO anon;
GRANT EXECUTE ON FUNCTION
    login(text,text,text),
    signup(text,text,text)
    TO anon;

GRANT USAGE ON SCHEMA public TO player;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO player;
GRANT EXECUTE ON FUNCTION current_id() TO player;
