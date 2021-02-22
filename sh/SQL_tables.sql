DROP TABLE IF EXISTS contractors;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id_user serial PRIMARY KEY,
    login varchar(128) UNIQUE NOT NULL,
    passwd varchar(128) NOT NULL,
    email varchar(64) UNIQUE NOT NULL
);

CREATE TABLE contractors
(
   id_contractor serial,
   user_id int REFERENCES users(id_user),
   user_contractor_id int REFERENCES users(id_user),
   confirmed bool NOT NULL DEFAULT 'False',
   CONSTRAINT pk_contractors PRIMARY KEY (user_id, user_contractor_id)
);

