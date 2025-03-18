--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: event_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event_roles (
    event_role_id integer NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    role_type_id integer NOT NULL,
    notes character varying
);


ALTER TABLE public.event_roles OWNER TO postgres;

--
-- Name: event_roles_event_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.event_roles_event_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_roles_event_role_id_seq OWNER TO postgres;

--
-- Name: event_roles_event_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.event_roles_event_role_id_seq OWNED BY public.event_roles.event_role_id;


--
-- Name: event_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event_types (
    event_type_id integer NOT NULL,
    event_type_name character varying NOT NULL,
    event_type_description character varying
);


ALTER TABLE public.event_types OWNER TO postgres;

--
-- Name: event_types_event_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.event_types_event_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.event_types_event_type_id_seq OWNER TO postgres;

--
-- Name: event_types_event_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.event_types_event_type_id_seq OWNED BY public.event_types.event_type_id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    event_id integer NOT NULL,
    source_id integer NOT NULL,
    event_type_id integer NOT NULL,
    event_location_id integer,
    event_date date,
    recorded_event_date character varying,
    priest_id integer,
    event_description character varying
);


ALTER TABLE public.events OWNER TO postgres;

--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_event_id_seq OWNER TO postgres;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: location_recorded_names; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_recorded_names (
    location_recorded_names_id integer NOT NULL,
    recorded_name character varying NOT NULL,
    location_id integer NOT NULL
);


ALTER TABLE public.location_recorded_names OWNER TO postgres;

--
-- Name: location_recorded_names_location_recorded_names_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_recorded_names_location_recorded_names_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.location_recorded_names_location_recorded_names_id_seq OWNER TO postgres;

--
-- Name: location_recorded_names_location_recorded_names_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_recorded_names_location_recorded_names_id_seq OWNED BY public.location_recorded_names.location_recorded_names_id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    location_id integer NOT NULL,
    tgn_id integer,
    place_type_id integer NOT NULL,
    place_type_name character varying
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.locations_location_id_seq OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations.location_id;


--
-- Name: persons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.persons (
    person_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    birth_date date,
    birth_date_typed character varying,
    birth_place_id integer,
    gender character varying,
    CONSTRAINT gender_check CHECK (((gender)::text = ANY ((ARRAY['male'::character varying, 'female'::character varying, 'unknown'::character varying])::text[])))
);


ALTER TABLE public.persons OWNER TO postgres;

--
-- Name: persons_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.persons_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persons_person_id_seq OWNER TO postgres;

--
-- Name: persons_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;


--
-- Name: place_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.place_types (
    place_type_id integer NOT NULL,
    place_type_name character varying NOT NULL
);


ALTER TABLE public.place_types OWNER TO postgres;

--
-- Name: place_types_place_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.place_types_place_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.place_types_place_type_id_seq OWNER TO postgres;

--
-- Name: place_types_place_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.place_types_place_type_id_seq OWNED BY public.place_types.place_type_id;


--
-- Name: relationship_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.relationship_types (
    relationship_type_id integer NOT NULL,
    relationship_type_name character varying NOT NULL,
    relationship_type_description character varying
);


ALTER TABLE public.relationship_types OWNER TO postgres;

--
-- Name: relationship_types_relationship_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.relationship_types_relationship_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.relationship_types_relationship_type_id_seq OWNER TO postgres;

--
-- Name: relationship_types_relationship_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.relationship_types_relationship_type_id_seq OWNED BY public.relationship_types.relationship_type_id;


--
-- Name: relationships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.relationships (
    relationship_id integer NOT NULL,
    person_id_1 integer NOT NULL,
    person_id_2 integer NOT NULL,
    relationship_type_id integer NOT NULL,
    notes character varying,
    CONSTRAINT no_self_relationship CHECK ((person_id_1 <> person_id_2))
);


ALTER TABLE public.relationships OWNER TO postgres;

--
-- Name: relationships_relationship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.relationships_relationship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.relationships_relationship_id_seq OWNER TO postgres;

--
-- Name: relationships_relationship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.relationships_relationship_id_seq OWNED BY public.relationships.relationship_id;


--
-- Name: role_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_types (
    role_type_id integer NOT NULL,
    role_type_name character varying NOT NULL,
    role_type_description character varying
);


ALTER TABLE public.role_types OWNER TO postgres;

--
-- Name: role_types_role_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_types_role_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_types_role_type_id_seq OWNER TO postgres;

--
-- Name: role_types_role_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_types_role_type_id_seq OWNED BY public.role_types.role_type_id;


--
-- Name: sources; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sources (
    source_id integer NOT NULL,
    archival_reference text NOT NULL,
    title character varying,
    folio_start character varying(10),
    folio_end character varying(10),
    date_start date,
    date_end date,
    recorded_date_start character varying,
    recorded_date_end character varying,
    notes character varying
);


ALTER TABLE public.sources OWNER TO postgres;

--
-- Name: sources_source_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sources_source_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sources_source_id_seq OWNER TO postgres;

--
-- Name: sources_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sources_source_id_seq OWNED BY public.sources.source_id;


--
-- Name: event_roles event_role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles ALTER COLUMN event_role_id SET DEFAULT nextval('public.event_roles_event_role_id_seq'::regclass);


--
-- Name: event_types event_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_types ALTER COLUMN event_type_id SET DEFAULT nextval('public.event_types_event_type_id_seq'::regclass);


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: location_recorded_names location_recorded_names_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_recorded_names ALTER COLUMN location_recorded_names_id SET DEFAULT nextval('public.location_recorded_names_location_recorded_names_id_seq'::regclass);


--
-- Name: locations location_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- Name: persons person_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);


--
-- Name: place_types place_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.place_types ALTER COLUMN place_type_id SET DEFAULT nextval('public.place_types_place_type_id_seq'::regclass);


--
-- Name: relationship_types relationship_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_types ALTER COLUMN relationship_type_id SET DEFAULT nextval('public.relationship_types_relationship_type_id_seq'::regclass);


--
-- Name: relationships relationship_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships ALTER COLUMN relationship_id SET DEFAULT nextval('public.relationships_relationship_id_seq'::regclass);


--
-- Name: role_types role_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_types ALTER COLUMN role_type_id SET DEFAULT nextval('public.role_types_role_type_id_seq'::regclass);


--
-- Name: sources source_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sources ALTER COLUMN source_id SET DEFAULT nextval('public.sources_source_id_seq'::regclass);


--
-- Name: sources archival_reference_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT archival_reference_unique UNIQUE (archival_reference);


--
-- Name: event_roles event_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles
    ADD CONSTRAINT event_roles_pkey PRIMARY KEY (event_role_id);


--
-- Name: event_types event_type_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_types
    ADD CONSTRAINT event_type_name_unique UNIQUE (event_type_name);


--
-- Name: event_types event_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_types
    ADD CONSTRAINT event_types_pkey PRIMARY KEY (event_type_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: location_recorded_names location_recorded_names_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_recorded_names
    ADD CONSTRAINT location_recorded_names_pkey PRIMARY KEY (location_recorded_names_id);


--
-- Name: location_recorded_names location_recorded_names_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_recorded_names
    ADD CONSTRAINT location_recorded_names_unique UNIQUE (location_id, recorded_name);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);


--
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (person_id);


--
-- Name: place_types place_type_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.place_types
    ADD CONSTRAINT place_type_name_unique UNIQUE (place_type_name);


--
-- Name: place_types place_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.place_types
    ADD CONSTRAINT place_types_pkey PRIMARY KEY (place_type_id);


--
-- Name: relationship_types relationship_type_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_types
    ADD CONSTRAINT relationship_type_name_unique UNIQUE (relationship_type_name);


--
-- Name: relationship_types relationship_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_types
    ADD CONSTRAINT relationship_types_pkey PRIMARY KEY (relationship_type_id);


--
-- Name: relationships relationships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_pkey PRIMARY KEY (relationship_id);


--
-- Name: role_types role_type_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_types
    ADD CONSTRAINT role_type_name_unique UNIQUE (role_type_name);


--
-- Name: role_types role_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_types
    ADD CONSTRAINT role_types_pkey PRIMARY KEY (role_type_id);


--
-- Name: sources sources_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (source_id);


--
-- Name: locations tgn_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT tgn_id_unique UNIQUE (tgn_id);


--
-- Name: event_roles unique_event_role_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles
    ADD CONSTRAINT unique_event_role_type UNIQUE (event_id, role_type_id);


--
-- Name: relationships unique_relationship; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT unique_relationship UNIQUE (person_id_1, person_id_2, relationship_type_id);


--
-- Name: idx_event_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_event_date ON public.events USING btree (event_date);


--
-- Name: idx_person_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_person_name ON public.persons USING btree (first_name, last_name);


--
-- Name: idx_source_reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_source_reference ON public.sources USING btree (archival_reference);


--
-- Name: event_roles event_roles_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles
    ADD CONSTRAINT event_roles_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: event_roles event_roles_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles
    ADD CONSTRAINT event_roles_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(person_id);


--
-- Name: event_roles event_roles_role_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event_roles
    ADD CONSTRAINT event_roles_role_type_id_fkey FOREIGN KEY (role_type_id) REFERENCES public.role_types(role_type_id);


--
-- Name: events events_event_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_event_location_id_fkey FOREIGN KEY (event_location_id) REFERENCES public.locations(location_id);


--
-- Name: events events_event_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_event_type_id_fkey FOREIGN KEY (event_type_id) REFERENCES public.event_types(event_type_id);


--
-- Name: events events_priest_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_priest_id_fkey FOREIGN KEY (priest_id) REFERENCES public.persons(person_id);


--
-- Name: events events_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.sources(source_id);


--
-- Name: location_recorded_names location_recorded_names_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_recorded_names
    ADD CONSTRAINT location_recorded_names_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id);


--
-- Name: locations locations_place_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_place_type_id_fkey FOREIGN KEY (place_type_id) REFERENCES public.place_types(place_type_id);


--
-- Name: persons persons_birth_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_birth_place_id_fkey FOREIGN KEY (birth_place_id) REFERENCES public.locations(location_id);


--
-- Name: relationships relationships_person_id_1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_person_id_1_fkey FOREIGN KEY (person_id_1) REFERENCES public.persons(person_id);


--
-- Name: relationships relationships_person_id_2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_person_id_2_fkey FOREIGN KEY (person_id_2) REFERENCES public.persons(person_id);


--
-- Name: relationships relationships_relationship_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_relationship_type_id_fkey FOREIGN KEY (relationship_type_id) REFERENCES public.relationship_types(relationship_type_id);


--
-- Name: TABLE event_roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.event_roles TO sondondo;


--
-- Name: SEQUENCE event_roles_event_role_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.event_roles_event_role_id_seq TO sondondo;


--
-- Name: TABLE event_types; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.event_types TO sondondo;


--
-- Name: SEQUENCE event_types_event_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.event_types_event_type_id_seq TO sondondo;


--
-- Name: TABLE events; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.events TO sondondo;


--
-- Name: SEQUENCE events_event_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.events_event_id_seq TO sondondo;


--
-- Name: TABLE location_recorded_names; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.location_recorded_names TO sondondo;


--
-- Name: SEQUENCE location_recorded_names_location_recorded_names_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.location_recorded_names_location_recorded_names_id_seq TO sondondo;


--
-- Name: TABLE locations; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.locations TO sondondo;


--
-- Name: SEQUENCE locations_location_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.locations_location_id_seq TO sondondo;


--
-- Name: TABLE persons; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.persons TO sondondo;


--
-- Name: SEQUENCE persons_person_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.persons_person_id_seq TO sondondo;


--
-- Name: TABLE place_types; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.place_types TO sondondo;


--
-- Name: SEQUENCE place_types_place_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.place_types_place_type_id_seq TO sondondo;


--
-- Name: TABLE relationship_types; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.relationship_types TO sondondo;


--
-- Name: SEQUENCE relationship_types_relationship_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.relationship_types_relationship_type_id_seq TO sondondo;


--
-- Name: TABLE relationships; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.relationships TO sondondo;


--
-- Name: SEQUENCE relationships_relationship_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.relationships_relationship_id_seq TO sondondo;


--
-- Name: TABLE role_types; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.role_types TO sondondo;


--
-- Name: SEQUENCE role_types_role_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.role_types_role_type_id_seq TO sondondo;


--
-- Name: TABLE sources; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.sources TO sondondo;


--
-- Name: SEQUENCE sources_source_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.sources_source_id_seq TO sondondo;


--
-- PostgreSQL database dump complete
--

