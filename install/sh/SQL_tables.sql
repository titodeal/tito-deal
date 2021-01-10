DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id_user serial PRIMARY KEY,
    login varchar(24) UNIQUE NOT NULL,
    first_name varchar(24),
    last_name varchar(24),
    passwd varchar(128) NOT NULL,
    email varchar(24) UNIQUE NOT NULL,
    phone varchar(16)
);

CREATE TABLE offers
(
   id_offer serial UNIQUE NOT NULL,
   user_id int REFERENCES users(id_user),
   contractor_id int REFERENCES users(id_user),
   conditions text,
   message varchar(900),
   accepted bool NOT NULL DEFAULT 'False',
   CONSTRAINT pk_offers PRIMARY KEY (user_id, contractor_id)
);
