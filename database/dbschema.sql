CREATE TABLE IF NOT EXISTS public.place_types (
    place_type_id SERIAL PRIMARY KEY,
    place_type_name character varying NOT NULL
);

ALTER TABLE public.place_types ADD CONSTRAINT place_type_name_unique UNIQUE (place_type_name);

CREATE TABLE IF NOT EXISTS public.locations (
    location_id SERIAL PRIMARY KEY,
    tgn_id integer,
    place_type_id integer NOT NULL REFERENCES public.place_types(place_type_id),
    place_type_name character varying
);

ALTER TABLE public.locations ADD CONSTRAINT tgn_id_unique UNIQUE (tgn_id);

CREATE TABLE IF NOT EXISTS public.location_recorded_names (
    location_recorded_names_id SERIAL PRIMARY KEY,
    recorded_name character varying NOT NULL,
    location_id integer NOT NULL REFERENCES public.locations(location_id)
);

ALTER TABLE public.location_recorded_names ADD CONSTRAINT location_recorded_names_unique UNIQUE (location_id, recorded_name);

CREATE TABLE IF NOT EXISTS public.persons (
    person_id SERIAL PRIMARY KEY,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    birth_date date,
    birth_date_typed character varying,
    birth_place_id integer REFERENCES public.locations(location_id),
    gender character varying
);

ALTER TABLE public.persons ADD CONSTRAINT gender_check CHECK (gender IN ('male', 'female', 'unknown'));

CREATE TABLE IF NOT EXISTS public.sources (
    source_id SERIAL PRIMARY KEY,
    archival_reference TEXT NOT NULL,
    title character varying,
    folio_start VARCHAR(10),
    folio_end VARCHAR(10),
    date_start DATE,
    date_end DATE,
    recorded_date_start character varying,
    recorded_date_end character varying,
    notes character varying
);

ALTER TABLE public.sources ADD CONSTRAINT archival_reference_unique UNIQUE (archival_reference);

CREATE TABLE IF NOT EXISTS public.event_types (
    event_type_id SERIAL PRIMARY KEY,
    event_type_name character varying NOT NULL,
    event_type_description character varying
);

ALTER TABLE public.event_types ADD CONSTRAINT event_type_name_unique UNIQUE (event_type_name);

CREATE TABLE IF NOT EXISTS public.events (
    event_id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES public.sources(source_id),
    event_type_id INTEGER NOT NULL REFERENCES public.event_types(event_type_id),
    event_location_id INTEGER REFERENCES public.locations(location_id),
    event_date DATE,
    recorded_event_date character varying,
    priest_id INTEGER REFERENCES public.persons(person_id),
    event_description character varying
);

CREATE TABLE IF NOT EXISTS public.relationship_types (
    relationship_type_id SERIAL PRIMARY KEY,
    relationship_type_name character varying NOT NULL,
    relationship_type_description character varying
);

ALTER TABLE public.relationship_types ADD CONSTRAINT relationship_type_name_unique UNIQUE (relationship_type_name);

CREATE TABLE IF NOT EXISTS public.relationships (
    relationship_id SERIAL PRIMARY KEY,
    person_id_1 INTEGER NOT NULL REFERENCES public.persons(person_id),
    person_id_2 INTEGER NOT NULL REFERENCES public.persons(person_id),
    relationship_type_id INTEGER NOT NULL REFERENCES public.relationship_types(relationship_type_id),
    notes character varying
);

ALTER TABLE public.relationships ADD CONSTRAINT unique_relationship UNIQUE (person_id_1, person_id_2, relationship_type_id);
ALTER TABLE public.relationships ADD CONSTRAINT no_self_relationship CHECK (person_id_1 <> person_id_2);


CREATE TABLE IF NOT EXISTS public.role_types (
    role_type_id SERIAL PRIMARY KEY,
    role_type_name character varying NOT NULL,
    role_type_description character varying
);

ALTER TABLE public.role_types ADD CONSTRAINT role_type_name_unique UNIQUE (role_type_name);

CREATE TABLE IF NOT EXISTS public.event_roles (
    event_role_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES public.events(event_id),
    person_id INTEGER NOT NULL REFERENCES public.persons(person_id),
    role_type_id INTEGER NOT NULL REFERENCES public.role_types(role_type_id),
    notes character varying
);

ALTER TABLE public.event_roles ADD CONSTRAINT unique_event_role_type UNIQUE (event_id, role_type_id);


--
-- Indexes
--

CREATE INDEX idx_person_name ON public.persons (first_name, last_name);
CREATE INDEX idx_event_date ON public.events (event_date);
CREATE INDEX idx_source_reference ON public.sources (archival_reference);


--
-- GRANT ALL PRIVILEGES to sondondo
--

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sondondo;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sondondo;

