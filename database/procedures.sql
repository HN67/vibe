USE vibe;

DELIMETER //

-- /api/moods/
CREATE OR REPLACE PROCEDURE get_moods()
    READS SQL DATA
    BEGIN
        SELECT (name)
        FROM Mood;
    END;
//

DELIMITER ;
