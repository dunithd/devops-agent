-- Cluster: workshop-cluster
-- Database: workshop

CREATE SCHEMA slack;

CREATE TABLE slack.messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);