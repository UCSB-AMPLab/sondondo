--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-08-05 14:53:21 PDT

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
-- TOC entry 219 (class 1259 OID 24715)
-- Name: ConditionVocab; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionVocab" (
    id integer NOT NULL,
    label character varying,
    type character varying
);


ALTER TABLE public."ConditionVocab" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24736)
-- Name: Event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Event" (
    id integer NOT NULL,
    event_type character varying,
    event_date date,
    event_place integer,
    record_id integer
);


ALTER TABLE public."Event" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24750)
-- Name: OriginalTerms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."OriginalTerms" (
    id integer NOT NULL,
    label_type character varying,
    label_value character varying,
    label_language character varying
);


ALTER TABLE public."OriginalTerms" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24703)
-- Name: Persona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Persona" (
    id integer NOT NULL,
    name character varying,
    lastname character varying,
    birth_date date,
    birth_place integer,
    death_date date,
    death_place integer,
    notes text
);


ALTER TABLE public."Persona" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24710)
-- Name: PersonaCondition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PersonaCondition" (
    id integer NOT NULL,
    person_id integer,
    condition_vocab_id integer,
    event_id integer
);


ALTER TABLE public."PersonaCondition" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24729)
-- Name: PersonaRelationship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PersonaRelationship" (
    id integer NOT NULL,
    person_subject_id integer,
    person_object_id integer,
    relationship_type character varying,
    event_id integer
);


ALTER TABLE public."PersonaRelationship" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 24722)
-- Name: PersonaRoleInEvent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PersonaRoleInEvent" (
    id integer NOT NULL,
    event_id integer,
    person_id integer,
    role character varying
);


ALTER TABLE public."PersonaRoleInEvent" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 24743)
-- Name: Place; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Place" (
    id integer NOT NULL,
    place_label character varying,
    language character varying,
    latitude double precision,
    longitude double precision,
    source character varying,
    uri character varying,
    country_code character varying,
    part_of character varying,
    part_of_uri character varying,
    mentioned_as integer
);


ALTER TABLE public."Place" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24757)
-- Name: Record; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Record" (
    id integer NOT NULL,
    record_type character varying,
    record_identifier character varying,
    record_file character varying
);


ALTER TABLE public."Record" OWNER TO postgres;

--
-- TOC entry 3659 (class 0 OID 24715)
-- Dependencies: 219
-- Data for Name: ConditionVocab; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ConditionVocab" (id, label, type) FROM stdin;
\.


--
-- TOC entry 3662 (class 0 OID 24736)
-- Dependencies: 222
-- Data for Name: Event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Event" (id, event_type, event_date, event_place, record_id) FROM stdin;
\.


--
-- TOC entry 3664 (class 0 OID 24750)
-- Dependencies: 224
-- Data for Name: OriginalTerms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."OriginalTerms" (id, label_type, label_value, label_language) FROM stdin;
\.


--
-- TOC entry 3657 (class 0 OID 24703)
-- Dependencies: 217
-- Data for Name: Persona; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Persona" (id, name, lastname, birth_date, birth_place, death_date, death_place, notes) FROM stdin;
\.


--
-- TOC entry 3658 (class 0 OID 24710)
-- Dependencies: 218
-- Data for Name: PersonaCondition; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."PersonaCondition" (id, person_id, condition_vocab_id, event_id) FROM stdin;
\.


--
-- TOC entry 3661 (class 0 OID 24729)
-- Dependencies: 221
-- Data for Name: PersonaRelationship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."PersonaRelationship" (id, person_subject_id, person_object_id, relationship_type, event_id) FROM stdin;
\.


--
-- TOC entry 3660 (class 0 OID 24722)
-- Dependencies: 220
-- Data for Name: PersonaRoleInEvent; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."PersonaRoleInEvent" (id, event_id, person_id, role) FROM stdin;
\.


--
-- TOC entry 3663 (class 0 OID 24743)
-- Dependencies: 223
-- Data for Name: Place; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Place" (id, place_label, language, latitude, longitude, source, uri, country_code, part_of, part_of_uri, mentioned_as) FROM stdin;
\.


--
-- TOC entry 3665 (class 0 OID 24757)
-- Dependencies: 225
-- Data for Name: Record; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Record" (id, record_type, record_identifier, record_file) FROM stdin;
\.


--
-- TOC entry 3486 (class 2606 OID 24721)
-- Name: ConditionVocab ConditionVocab_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionVocab"
    ADD CONSTRAINT "ConditionVocab_pkey" PRIMARY KEY (id);


--
-- TOC entry 3492 (class 2606 OID 24742)
-- Name: Event Event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (id);


--
-- TOC entry 3496 (class 2606 OID 24756)
-- Name: OriginalTerms OriginalTerms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."OriginalTerms"
    ADD CONSTRAINT "OriginalTerms_pkey" PRIMARY KEY (id);


--
-- TOC entry 3484 (class 2606 OID 24714)
-- Name: PersonaCondition PersonaCondition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaCondition"
    ADD CONSTRAINT "PersonaCondition_pkey" PRIMARY KEY (id);


--
-- TOC entry 3490 (class 2606 OID 24735)
-- Name: PersonaRelationship PersonaRelationship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRelationship"
    ADD CONSTRAINT "PersonaRelationship_pkey" PRIMARY KEY (id);


--
-- TOC entry 3488 (class 2606 OID 24728)
-- Name: PersonaRoleInEvent PersonaRoleInEvent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRoleInEvent"
    ADD CONSTRAINT "PersonaRoleInEvent_pkey" PRIMARY KEY (id);


--
-- TOC entry 3482 (class 2606 OID 24709)
-- Name: Persona Persona_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Persona"
    ADD CONSTRAINT "Persona_pkey" PRIMARY KEY (id);


--
-- TOC entry 3494 (class 2606 OID 24749)
-- Name: Place Place_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Place"
    ADD CONSTRAINT "Place_pkey" PRIMARY KEY (id);


--
-- TOC entry 3498 (class 2606 OID 24763)
-- Name: Record Record_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Record"
    ADD CONSTRAINT "Record_pkey" PRIMARY KEY (id);


--
-- TOC entry 3509 (class 2606 OID 24814)
-- Name: Event Event_event_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_event_place_fkey" FOREIGN KEY (event_place) REFERENCES public."Place"(id);


--
-- TOC entry 3510 (class 2606 OID 24819)
-- Name: Event Event_record_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_record_id_fkey" FOREIGN KEY (record_id) REFERENCES public."Record"(id);


--
-- TOC entry 3501 (class 2606 OID 24779)
-- Name: PersonaCondition PersonaCondition_condition_vocab_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaCondition"
    ADD CONSTRAINT "PersonaCondition_condition_vocab_id_fkey" FOREIGN KEY (condition_vocab_id) REFERENCES public."ConditionVocab"(id);


--
-- TOC entry 3502 (class 2606 OID 24784)
-- Name: PersonaCondition PersonaCondition_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaCondition"
    ADD CONSTRAINT "PersonaCondition_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id);


--
-- TOC entry 3503 (class 2606 OID 24774)
-- Name: PersonaCondition PersonaCondition_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaCondition"
    ADD CONSTRAINT "PersonaCondition_person_id_fkey" FOREIGN KEY (person_id) REFERENCES public."Persona"(id);


--
-- TOC entry 3506 (class 2606 OID 24809)
-- Name: PersonaRelationship PersonaRelationship_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRelationship"
    ADD CONSTRAINT "PersonaRelationship_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id);


--
-- TOC entry 3507 (class 2606 OID 24804)
-- Name: PersonaRelationship PersonaRelationship_person_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRelationship"
    ADD CONSTRAINT "PersonaRelationship_person_object_id_fkey" FOREIGN KEY (person_object_id) REFERENCES public."Persona"(id);


--
-- TOC entry 3508 (class 2606 OID 24799)
-- Name: PersonaRelationship PersonaRelationship_person_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRelationship"
    ADD CONSTRAINT "PersonaRelationship_person_subject_id_fkey" FOREIGN KEY (person_subject_id) REFERENCES public."Persona"(id);


--
-- TOC entry 3504 (class 2606 OID 24789)
-- Name: PersonaRoleInEvent PersonaRoleInEvent_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRoleInEvent"
    ADD CONSTRAINT "PersonaRoleInEvent_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id);


--
-- TOC entry 3505 (class 2606 OID 24794)
-- Name: PersonaRoleInEvent PersonaRoleInEvent_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PersonaRoleInEvent"
    ADD CONSTRAINT "PersonaRoleInEvent_person_id_fkey" FOREIGN KEY (person_id) REFERENCES public."Persona"(id);


--
-- TOC entry 3499 (class 2606 OID 24764)
-- Name: Persona Persona_birth_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Persona"
    ADD CONSTRAINT "Persona_birth_place_fkey" FOREIGN KEY (birth_place) REFERENCES public."Place"(id);


--
-- TOC entry 3500 (class 2606 OID 24769)
-- Name: Persona Persona_death_place_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Persona"
    ADD CONSTRAINT "Persona_death_place_fkey" FOREIGN KEY (death_place) REFERENCES public."Place"(id);


--
-- TOC entry 3511 (class 2606 OID 24824)
-- Name: Place Place_mentioned_as_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Place"
    ADD CONSTRAINT "Place_mentioned_as_fkey" FOREIGN KEY (mentioned_as) REFERENCES public."OriginalTerms"(id);


-- Completed on 2025-08-05 14:53:26 PDT

--
-- PostgreSQL database dump complete
--

