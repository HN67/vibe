DELIMETER //

-- /api/moods/
CREATE PROCEDURE get_moods()
    READS SQL DATA
    BEGIN
        SELECT (name)
        FROM Mood;
    END;
//

DELIMITER ;
