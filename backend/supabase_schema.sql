-- ============================================================
-- AI-First CRM HCP Module -- Full Database Schema
-- Run this in: Supabase Dashboard -> SQL Editor -> New Query
-- ============================================================

-- 1. USERS
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role            VARCHAR(50)  NOT NULL DEFAULT 'rep',
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ  DEFAULT now(),
    updated_at      TIMESTAMPTZ  DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE INDEX        IF NOT EXISTS ix_users_id    ON users (id);

-- 2. AI LOGS
CREATE TABLE IF NOT EXISTS ai_logs (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER      NOT NULL REFERENCES users(id),
    session_id  VARCHAR(100) NOT NULL,
    input_text  TEXT         NOT NULL,
    output_text TEXT,
    tool_used   VARCHAR(100),
    model_used  VARCHAR(100),
    tokens_used INTEGER,
    latency_ms  INTEGER,
    created_at  TIMESTAMPTZ  DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_ai_logs_id         ON ai_logs (id);
CREATE INDEX IF NOT EXISTS ix_ai_logs_session_id ON ai_logs (session_id);
CREATE INDEX IF NOT EXISTS ix_ai_logs_user_id    ON ai_logs (user_id);

-- 3. HCPS (Healthcare Professionals)
CREATE TABLE IF NOT EXISTS hcps (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    hospital    VARCHAR(255),
    speciality  VARCHAR(255),
    location    VARCHAR(255),
    email       VARCHAR(255),
    phone       VARCHAR(50),
    notes       TEXT,
    created_by  INTEGER      NOT NULL REFERENCES users(id),
    created_at  TIMESTAMPTZ  DEFAULT now(),
    updated_at  TIMESTAMPTZ  DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_hcp_name_hospital ON hcps (name, hospital);
CREATE INDEX IF NOT EXISTS ix_hcps_hospital     ON hcps (hospital);
CREATE INDEX IF NOT EXISTS ix_hcps_id           ON hcps (id);
CREATE INDEX IF NOT EXISTS ix_hcps_location     ON hcps (location);
CREATE INDEX IF NOT EXISTS ix_hcps_name         ON hcps (name);
CREATE INDEX IF NOT EXISTS ix_hcps_speciality   ON hcps (speciality);

-- 4. INTERACTIONS
CREATE TABLE IF NOT EXISTS interactions (
    id                  SERIAL PRIMARY KEY,
    user_id             INTEGER      NOT NULL REFERENCES users(id),
    hcp_id              INTEGER      NOT NULL REFERENCES hcps(id),
    date                DATE         NOT NULL,
    time                TIME         NOT NULL,
    visit_type          VARCHAR(100) NOT NULL,
    products_discussed  JSONB,
    samples_given       JSONB,
    feedback            TEXT,
    notes               TEXT,
    source              VARCHAR(50)  DEFAULT 'form',
    ai_summary          TEXT,
    created_at          TIMESTAMPTZ  DEFAULT now(),
    updated_at          TIMESTAMPTZ  DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_interactions_date    ON interactions (date);
CREATE INDEX IF NOT EXISTS ix_interactions_hcp_id  ON interactions (hcp_id);
CREATE INDEX IF NOT EXISTS ix_interactions_id      ON interactions (id);
CREATE INDEX IF NOT EXISTS ix_interactions_user_id ON interactions (user_id);

-- 5. FOLLOW-UPS
CREATE TABLE IF NOT EXISTS followups (
    id                  SERIAL PRIMARY KEY,
    interaction_id      INTEGER      NOT NULL REFERENCES interactions(id),
    hcp_id              INTEGER      NOT NULL REFERENCES hcps(id),
    user_id             INTEGER      NOT NULL REFERENCES users(id),
    date                DATE,
    status              VARCHAR(50)  DEFAULT 'pending',
    priority            VARCHAR(50)  DEFAULT 'medium',
    notes               TEXT,
    recommended_action  TEXT,
    suggested_products  JSONB,
    suggested_questions JSONB,
    created_at          TIMESTAMPTZ  DEFAULT now(),
    updated_at          TIMESTAMPTZ  DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_followups_date           ON followups (date);
CREATE INDEX IF NOT EXISTS ix_followups_hcp_id         ON followups (hcp_id);
CREATE INDEX IF NOT EXISTS ix_followups_id             ON followups (id);
CREATE INDEX IF NOT EXISTS ix_followups_interaction_id ON followups (interaction_id);
CREATE INDEX IF NOT EXISTS ix_followups_user_id        ON followups (user_id);

-- 6. INTERACTION HISTORY (Audit Trail)
CREATE TABLE IF NOT EXISTS interaction_history (
    id              SERIAL PRIMARY KEY,
    interaction_id  INTEGER      NOT NULL REFERENCES interactions(id),
    changed_by      INTEGER      NOT NULL REFERENCES users(id),
    change_type     VARCHAR(50)  NOT NULL,
    old_data        JSONB,
    new_data        JSONB,
    created_at      TIMESTAMPTZ  DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_interaction_history_id             ON interaction_history (id);
CREATE INDEX IF NOT EXISTS ix_interaction_history_interaction_id ON interaction_history (interaction_id);

-- Alembic version tracking
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version (version_num)
VALUES ('413e52c9ced1')
ON CONFLICT DO NOTHING;

SELECT 'Schema created successfully' AS status;
