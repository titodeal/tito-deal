DROP TABLE IF EXISTS document_templates;
DROP TABLE IF EXISTS contracts;
DROP TABLE IF EXISTS templates CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS roots;
DROP TABLE IF EXISTS agreements;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    login varchar(24) UNIQUE NOT NULL,
    first_name varchar(24),
    last_name varchar(24),
    passwd varchar(128) NOT NULL,
    email varchar(24) UNIQUE NOT NULL,
    phone varchar(16)
);

CREATE TABLE agreements
(
   agreement_id serial UNIQUE NOT NULL,
   owner_id int REFERENCES users(user_id),
   contractor_id int REFERENCES users(user_id),
   conditions text,
   expiration date,
   accepted bool NOT NULL DEFAULT 'False',
   CONSTRAINT pk_agreements PRIMARY KEY (owner_id, contractor_id)
);

CREATE TABLE projects
(
   project_id serial UNIQUE NOT NULL,
   name varchar(24) NOT NULL,
   owner_id int REFERENCES users(user_id),
   scheme varchar(3) NOT NULL DEFAULT 'SES',
   fps smallint DEFAULT 24,
   status varchar(8) DEFAULT 'active',
   CONSTRAINT pk_projects PRIMARY KEY (name, owner_id)
);

CREATE TABLE roots
(
   root_id serial UNIQUE NOT NULL,
   path varchar(256) NOT NULL,
   project_id int REFERENCES projects(project_id),
   user_id int REFERENCES users(user_id),
   CONSTRAINT pk_roots PRIMARY KEY (project_id, user_id)
);

CREATE TABLE document_templates
(
   template_id serial UNIQUE NOT NULL,
   owner_id int REFERENCES users(user_id) NOT NULL,
   category varchar(8) NOT NULL,
   name varchar(25) NOT NULL,
   text_document text NOT NULL
);

CREATE TABLE contracts
(
   contract_id serial UNIQUE NOT NULL,
   agreement_id int REFERENCES agreements(agreement_id) NOT NULL,
   project_id int REFERENCES projects(project_id),
   documents int ARRAY,
   departments varchar(24),
   specialty varchar(24),
   role varchar(24),
   accepted bool NOT NULL DEFAULT 'False',
   date date,
   CONSTRAINT pk_contracts PRIMARY KEY (agreement_id, project_id)
);

