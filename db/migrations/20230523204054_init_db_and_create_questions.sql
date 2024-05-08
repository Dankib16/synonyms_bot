-- migrate:up
CREATE TABLE synonyms (
  id SERIAL PRIMARY KEY,
  word TEXT,
  synonyms TEXT
);
-- migrate:down