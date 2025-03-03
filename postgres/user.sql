-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	keycloak_id uuid NOT NULL,
	username varchar(255) NOT NULL,
	first_name varchar(255) NOT NULL,
	last_name varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	phone_number varchar(20) NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_keycloak_id_key UNIQUE (keycloak_id),
	CONSTRAINT users_phone_number_key UNIQUE (phone_number),
	CONSTRAINT users_pkey PRIMARY KEY (id)
);