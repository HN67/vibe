USE vibe;

DELIMITER //

-- GET /api/moods/
CREATE OR REPLACE PROCEDURE get_moods()
    READS SQL DATA
    BEGIN
        SELECT (name)
        FROM Mood
        ;
    END;
//

-- GET /api/moods/<name: string>
CREATE OR REPLACE PROCEDURE get_mood(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT (name)
        FROM Mood
        WHERE Mood.name = name
        ;
    END;
//

-- PUT /api/moods/<name: string>
CREATE OR REPLACE PROCEDURE put_mood(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Mood
        VALUES (name)
        ON DUPLICATE KEY UPDATE
            Mood.name = name
        ;
    END;
//

-- DELETE /api/moods/<name: string>
CREATE OR REPLACE PROCEDURE delete_mood(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Mood
        WHERE Mood.name = name
        ;
    END;
//

DELIMITER ;
