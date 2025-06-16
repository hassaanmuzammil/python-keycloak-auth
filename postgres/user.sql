-- public.capability definition

-- Drop table

-- DROP TABLE public.capability;

CREATE TABLE public.capability (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	"name" varchar NOT NULL,
	description varchar(255) NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at timestamp NULL,
	CONSTRAINT capability_name_key UNIQUE (name),
	CONSTRAINT capability_pkey PRIMARY KEY (id)
);


-- public."role" definition

-- Drop table

-- DROP TABLE public."role";

CREATE TABLE public."role" (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	"name" varchar NOT NULL,
	description varchar(255) NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at timestamp NULL,
	CONSTRAINT role_name_key UNIQUE (name),
	CONSTRAINT role_pkey PRIMARY KEY (id)
);


-- public."user" definition

-- Drop table

-- DROP TABLE public."user";

CREATE TABLE public."user" (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	keycloak_id uuid NOT NULL,
	username varchar(255) NOT NULL,
	first_name varchar(255) NOT NULL,
	last_name varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	phone_number varchar(20) NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at timestamp NULL,
	email_verified bool NOT NULL DEFAULT false,
	CONSTRAINT user_email_key UNIQUE (email),
	CONSTRAINT user_keycloak_id_key UNIQUE (keycloak_id),
	CONSTRAINT user_phone_number_key UNIQUE (phone_number),
	CONSTRAINT user_pkey PRIMARY KEY (id),
	CONSTRAINT user_username_key UNIQUE (username)
);


-- public.role_capability_link definition

-- Drop table

-- DROP TABLE public.role_capability_link;

CREATE TABLE public.role_capability_link (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	role_id uuid NOT NULL,
	capability_id uuid NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at timestamp NULL,
	CONSTRAINT role_capability_link_capability_id_fkey FOREIGN KEY (capability_id) REFERENCES public.capability(id),
	CONSTRAINT role_capability_link_role_id_fkey FOREIGN KEY (role_id) REFERENCES public."role"(id)
);


-- public.user_role_link definition

-- Drop table

-- DROP TABLE public.user_role_link;

CREATE TABLE public.user_role_link (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	user_id uuid NOT NULL,
	role_id uuid NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at timestamp NULL,
	CONSTRAINT user_role_link_role_id_fkey FOREIGN KEY (role_id) REFERENCES public."role"(id),
	CONSTRAINT user_role_link_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id)
);