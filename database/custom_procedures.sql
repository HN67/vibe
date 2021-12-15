CREATE OR REPLACE PROCEDURE get_users()
    READS SQL DATA
    BEGIN
        SELECT (id)
        FROM User
        ;
    END;
//

CREATE OR REPLACE PROCEDURE post_user(IN username NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO User (username)
        VALUES (username)
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_user(IN id INT)
    READS SQL DATA
    BEGIN
        SELECT (id, username)
        FROM User
        WHERE User.id = id
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_user(IN id INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM User
        WHERE User.id = id
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_usernames()
    READS SQL DATA
    BEGIN
        SELECT (username)
        FROM User
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_username(IN username NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT (id, username)
        FROM User
        WHERE User.username = username
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_results(IN clientId INT)
    READS SQL DATA
    BEGIN
        SELECT (number)
        FROM Result
        WHERE Result.clientId = clientId
        ;
    END;
//

CREATE OR REPLACE PROCEDURE post_result(
    IN clientId INT, IN mood NVARCHAR(255), IN taste NVARCHAR(255), IN scent NVARCHAR(255),
    IN color NVARCHAR(255), IN shape NVARCHAR(255), IN media NVARCHAR(255), IN music NVARCHAR(255)
)
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Result (clientId, mood, taste, scent, color, shape, media, music)
        VALUES (clientId, mood, taste, scent, color, shape, media, music)
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_result(IN clientId INT, IN number INT)
    READS SQL DATA
    BEGIN
        SELECT (clientId, number, mood, taste, scent, color, shape, media, music)
        FROM Result
        WHERE Result.clientId = clientId AND Result.number = number
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_result_all(IN clientId INT)
    READS SQL DATA
    BEGIN
        SELECT (clientId, number, mood, taste, scent, color, shape, media, music)
        FROM Result
        WHERE Result.clientId = clientId
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_result(IN clientId INT, IN number INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Result
        WHERE Result.clientId = clientId AND Result.number = number
        ;
    END;
//    
