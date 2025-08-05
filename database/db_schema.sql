CREATE TABLE "Persona" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "lastname" varchar,
  "birth_date" date,
  "birth_place" int,
  "death_date" date,
  "death_place" int,
  "notes" text
);

CREATE TABLE "PersonaCondition" (
  "id" int PRIMARY KEY,
  "person_id" int,
  "condition_vocab_id" int,
  "event_id" int
);

CREATE TABLE "ConditionVocab" (
  "id" int PRIMARY KEY,
  "label" varchar,
  "type" varchar
);

CREATE TABLE "PersonaRoleInEvent" (
  "id" int PRIMARY KEY,
  "event_id" int,
  "person_id" int,
  "role" varchar
);

CREATE TABLE "PersonaRelationship" (
  "id" int PRIMARY KEY,
  "person_subject_id" int,
  "person_object_id" int,
  "relationship_type" varchar,
  "event_id" int
);

CREATE TABLE "Event" (
  "id" int PRIMARY KEY,
  "event_type" varchar,
  "event_date" date,
  "event_place" int,
  "record_id" int
);

CREATE TABLE "Place" (
  "id" int PRIMARY KEY,
  "place_label" varchar,
  "language" varchar,
  "latitude" float,
  "longitude" float,
  "source" varchar,
  "uri" varchar,
  "country_code" varchar,
  "part_of" varchar,
  "part_of_uri" varchar,
  "mentioned_as" int
);

CREATE TABLE "OriginalTerms" (
  "id" int PRIMARY KEY,
  "label_type" varchar,
  "label_value" varchar,
  "label_language" varchar
);

CREATE TABLE "Record" (
  "id" int PRIMARY KEY,
  "record_type" varchar,
  "record_identifier" varchar,
  "record_file" varchar
);

ALTER TABLE "Persona" ADD FOREIGN KEY ("birth_place") REFERENCES "Place" ("id");

ALTER TABLE "Persona" ADD FOREIGN KEY ("death_place") REFERENCES "Place" ("id");

ALTER TABLE "PersonaCondition" ADD FOREIGN KEY ("person_id") REFERENCES "Persona" ("id");

ALTER TABLE "PersonaCondition" ADD FOREIGN KEY ("condition_vocab_id") REFERENCES "ConditionVocab" ("id");

ALTER TABLE "PersonaCondition" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("id");

ALTER TABLE "PersonaRoleInEvent" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("id");

ALTER TABLE "PersonaRoleInEvent" ADD FOREIGN KEY ("person_id") REFERENCES "Persona" ("id");

ALTER TABLE "PersonaRelationship" ADD FOREIGN KEY ("person_subject_id") REFERENCES "Persona" ("id");

ALTER TABLE "PersonaRelationship" ADD FOREIGN KEY ("person_object_id") REFERENCES "Persona" ("id");

ALTER TABLE "PersonaRelationship" ADD FOREIGN KEY ("event_id") REFERENCES "Event" ("id");

ALTER TABLE "Event" ADD FOREIGN KEY ("event_place") REFERENCES "Place" ("id");

ALTER TABLE "Event" ADD FOREIGN KEY ("record_id") REFERENCES "Record" ("id");

ALTER TABLE "Place" ADD FOREIGN KEY ("mentioned_as") REFERENCES "OriginalTerms" ("id");
