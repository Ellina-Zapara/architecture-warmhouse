-- SmartHome DB init script

CREATE TABLE IF NOT EXISTS sensors (
    id          SERIAL PRIMARY KEY,
    device_id   VARCHAR(128) UNIQUE NOT NULL,
    type        VARCHAR(64)  NOT NULL DEFAULT 'sensor',
    location    VARCHAR(256) NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Seed data
INSERT INTO sensors (device_id, type, location) VALUES
    ('dev-001', 'sensor',    'Living Room'),
    ('dev-002', 'sensor',    'Bedroom'),
    ('dev-003', 'gateway',   'Kitchen')
ON CONFLICT (device_id) DO NOTHING;
