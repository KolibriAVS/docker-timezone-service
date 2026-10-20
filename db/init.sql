CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    base_time TIMESTAMP NOT NULL,
    target_timezone VARCHAR(50) NOT NULL,
    converted_time TIMESTAMP
);

INSERT INTO meetings (title, base_time, target_timezone) 
VALUES ('Встреча с партнерами из Токио', '2026-10-20 12:00:00', 'Asia/Tokyo');