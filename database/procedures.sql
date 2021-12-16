USE vibe;

DELIMITER //

CREATE OR REPLACE PROCEDURE get_moods()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM Mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mood(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name
        FROM Mood
        WHERE Mood.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_mood(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Mood (name)
        VALUES (name)
            ON DUPLICATE KEY UPDATE
            Mood.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_mood(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Mood
        WHERE Mood.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_tastes()
    READS SQL DATA
    BEGIN
        SELECT type
        FROM Taste
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_taste(IN type NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT type
        FROM Taste
        WHERE Taste.type = type
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_taste(IN type NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Taste (type)
        VALUES (type)
            ON DUPLICATE KEY UPDATE
            Taste.type = type
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_taste(IN type NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Taste
        WHERE Taste.type = type
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_scents()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM Scent
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_scent(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name, family
        FROM Scent
        WHERE Scent.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_scent(IN name NVARCHAR(255), IN family NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Scent (name, family)
        VALUES (name, family)
            ON DUPLICATE KEY UPDATE
            Scent.name = name, Scent.family = family
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_scent(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Scent
        WHERE Scent.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_colors()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM Color
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_color(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name, hue, saturation, brightness
        FROM Color
        WHERE Color.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_color(IN name NVARCHAR(255), IN hue INT, IN saturation INT, IN brightness INT)
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Color (name, hue, saturation, brightness)
        VALUES (name, hue, saturation, brightness)
            ON DUPLICATE KEY UPDATE
            Color.name = name, Color.hue = hue, Color.saturation = saturation, Color.brightness = brightness
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_color(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Color
        WHERE Color.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_shapes()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM Shape
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_shape(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name, sides
        FROM Shape
        WHERE Shape.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_shape(IN name NVARCHAR(255), IN sides INT)
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Shape (name, sides)
        VALUES (name, sides)
            ON DUPLICATE KEY UPDATE
            Shape.name = name, Shape.sides = sides
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_shape(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Shape
        WHERE Shape.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_mediagenres()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM MediaGenre
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mediagenre(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name
        FROM MediaGenre
        WHERE MediaGenre.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_mediagenre(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO MediaGenre (name)
        VALUES (name)
            ON DUPLICATE KEY UPDATE
            MediaGenre.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_mediagenre(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM MediaGenre
        WHERE MediaGenre.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_musicgenres()
    READS SQL DATA
    BEGIN
        SELECT name
        FROM MusicGenre
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_musicgenre(IN name NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT name
        FROM MusicGenre
        WHERE MusicGenre.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_musicgenre(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO MusicGenre (name)
        VALUES (name)
            ON DUPLICATE KEY UPDATE
            MusicGenre.name = name
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_musicgenre(IN name NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM MusicGenre
        WHERE MusicGenre.name = name
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_admins()
    READS SQL DATA
    BEGIN
        SELECT id
        FROM admin
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_admin(IN id INT)
    READS SQL DATA
    BEGIN
        SELECT id, permissions
        FROM admin
        WHERE admin.id = id
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_admin(IN id INT, IN permissions INT)
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO admin (id, permissions)
        VALUES (id, permissions)
            ON DUPLICATE KEY UPDATE
            admin.id = id, admin.permissions = permissions
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_admin(IN id INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM admin
        WHERE admin.id = id
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_clients()
    READS SQL DATA
    BEGIN
        SELECT id
        FROM client
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_client(IN id INT)
    READS SQL DATA
    BEGIN
        SELECT id, birthday, email, displayName, bio
        FROM client
        WHERE client.id = id
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_client(IN id INT, IN birthday DATE, IN email NVARCHAR(255), IN displayName NVARCHAR(255), IN bio NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO client (id, birthday, email, displayName, bio)
        VALUES (id, birthday, email, displayName, bio)
            ON DUPLICATE KEY UPDATE
            client.id = id, client.birthday = birthday, client.email = email, client.displayName = displayName, client.bio = bio
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_client(IN id INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM client
        WHERE client.id = id
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_users()
    READS SQL DATA
    BEGIN
        SELECT id
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
        SELECT id, username
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
        SELECT username
        FROM User
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_username(IN username NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT id, username
        FROM User
        WHERE User.username = username
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_results(IN clientId INT)
    READS SQL DATA
    BEGIN
        SELECT number
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
        SELECT clientId, number, mood, taste, scent, color, shape, media, music
        FROM Result
        WHERE Result.clientId = clientId AND Result.number = number
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_result_all(IN clientId INT)
    READS SQL DATA
    BEGIN
        SELECT clientId, number, mood, taste, scent, color, shape, media, music
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

DELIMITER ;
