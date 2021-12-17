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

CREATE OR REPLACE PROCEDURE put_tasteaffects(IN taste NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO TasteAffects (taste, mood)
        VALUES (taste, mood)
        ON DUPLICATE KEY UPDATE
            TasteAffects.taste = taste, TasteAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_tasteaffects(IN taste NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM TasteAffects
        WHERE TasteAffects.taste = taste AND TasteAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_tasteaffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT taste, mood
        FROM TasteAffects
        WHERE TasteAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_tasteaffects_taste(IN taste NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT taste, mood
        FROM TasteAffects
        WHERE TasteAffects.taste = taste
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_tasteaffects_taste_mood(IN taste NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT taste, mood
        FROM TasteAffects
        WHERE TasteAffects.taste = taste AND TasteAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_tasteaffects()
    READS SQL DATA
    BEGIN
        SELECT taste, mood
        FROM TasteAffects
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

CREATE OR REPLACE PROCEDURE put_scentaffects(IN scent NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO ScentAffects (scent, mood)
        VALUES (scent, mood)
        ON DUPLICATE KEY UPDATE
            ScentAffects.scent = scent, ScentAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_scentaffects(IN scent NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM ScentAffects
        WHERE ScentAffects.scent = scent AND ScentAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_scentaffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT scent, mood
        FROM ScentAffects
        WHERE ScentAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_scentaffects_scent(IN scent NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT scent, mood
        FROM ScentAffects
        WHERE ScentAffects.scent = scent
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_scentaffects_scent_mood(IN scent NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT scent, mood
        FROM ScentAffects
        WHERE ScentAffects.scent = scent AND ScentAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_scentaffects()
    READS SQL DATA
    BEGIN
        SELECT scent, mood
        FROM ScentAffects
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

CREATE OR REPLACE PROCEDURE put_coloraffects(IN color NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO ColorAffects (color, mood)
        VALUES (color, mood)
        ON DUPLICATE KEY UPDATE
            ColorAffects.color = color, ColorAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_coloraffects(IN color NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM ColorAffects
        WHERE ColorAffects.color = color AND ColorAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_coloraffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT color, mood
        FROM ColorAffects
        WHERE ColorAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_coloraffects_color(IN color NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT color, mood
        FROM ColorAffects
        WHERE ColorAffects.color = color
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_coloraffects_color_mood(IN color NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT color, mood
        FROM ColorAffects
        WHERE ColorAffects.color = color AND ColorAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_coloraffects()
    READS SQL DATA
    BEGIN
        SELECT color, mood
        FROM ColorAffects
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

CREATE OR REPLACE PROCEDURE put_shapeaffects(IN shape NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO ShapeAffects (shape, mood)
        VALUES (shape, mood)
        ON DUPLICATE KEY UPDATE
            ShapeAffects.shape = shape, ShapeAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_shapeaffects(IN shape NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM ShapeAffects
        WHERE ShapeAffects.shape = shape AND ShapeAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_shapeaffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT shape, mood
        FROM ShapeAffects
        WHERE ShapeAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_shapeaffects_shape(IN shape NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT shape, mood
        FROM ShapeAffects
        WHERE ShapeAffects.shape = shape
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_shapeaffects_shape_mood(IN shape NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT shape, mood
        FROM ShapeAffects
        WHERE ShapeAffects.shape = shape AND ShapeAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_shapeaffects()
    READS SQL DATA
    BEGIN
        SELECT shape, mood
        FROM ShapeAffects
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

CREATE OR REPLACE PROCEDURE put_mediaaffects(IN media NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO MediaAffects (media, mood)
        VALUES (media, mood)
        ON DUPLICATE KEY UPDATE
            MediaAffects.media = media, MediaAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_mediaaffects(IN media NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM MediaAffects
        WHERE MediaAffects.media = media AND MediaAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mediaaffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT media, mood
        FROM MediaAffects
        WHERE MediaAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mediaaffects_media(IN media NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT media, mood
        FROM MediaAffects
        WHERE MediaAffects.media = media
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mediaaffects_media_mood(IN media NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT media, mood
        FROM MediaAffects
        WHERE MediaAffects.media = media AND MediaAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_mediaaffects()
    READS SQL DATA
    BEGIN
        SELECT media, mood
        FROM MediaAffects
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

CREATE OR REPLACE PROCEDURE put_musicaffects(IN music NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO MusicAffects (music, mood)
        VALUES (music, mood)
        ON DUPLICATE KEY UPDATE
            MusicAffects.music = music, MusicAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_musicaffects(IN music NVARCHAR(255), IN mood NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM MusicAffects
        WHERE MusicAffects.music = music AND MusicAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_musicaffects_mood(IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT music, mood
        FROM MusicAffects
        WHERE MusicAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_musicaffects_music(IN music NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT music, mood
        FROM MusicAffects
        WHERE MusicAffects.music = music
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_musicaffects_music_mood(IN music NVARCHAR(255), IN mood NVARCHAR(255))
    READS SQL DATA
    BEGIN
        SELECT music, mood
        FROM MusicAffects
        WHERE MusicAffects.music = music AND MusicAffects.mood = mood
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_musicaffects()
    READS SQL DATA
    BEGIN
        SELECT music, mood
        FROM MusicAffects
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_admins()
    READS SQL DATA
    BEGIN
        SELECT id
        FROM Admin
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_admin(IN id INT)
    READS SQL DATA
    BEGIN
        SELECT id, permissions
        FROM Admin
        WHERE Admin.id = id
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_admin(IN id INT, IN permissions INT)
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Admin (id, permissions)
        VALUES (id, permissions)
            ON DUPLICATE KEY UPDATE
            Admin.id = id, Admin.permissions = permissions
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_admin(IN id INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Admin
        WHERE Admin.id = id
        ;
    END;
//    

CREATE OR REPLACE PROCEDURE get_clients()
    READS SQL DATA
    BEGIN
        SELECT id
        FROM Client
        ;
    END;
//

CREATE OR REPLACE PROCEDURE get_client(IN id INT)
    READS SQL DATA
    BEGIN
        SELECT id, birthday, email, displayName, bio
        FROM Client
        WHERE Client.id = id
        ;
    END;
//

CREATE OR REPLACE PROCEDURE put_client(IN id INT, IN birthday NVARCHAR(255), IN email NVARCHAR(255), IN displayName NVARCHAR(255), IN bio NVARCHAR(255))
    MODIFIES SQL DATA
    BEGIN
        INSERT INTO Client (id, birthday, email, displayName, bio)
        VALUES (id, birthday, email, displayName, bio)
            ON DUPLICATE KEY UPDATE
            Client.id = id, Client.birthday = birthday, Client.email = email, Client.displayName = displayName, Client.bio = bio
        ;
    END;
//

CREATE OR REPLACE PROCEDURE delete_client(IN id INT)
    MODIFIES SQL DATA
    BEGIN
        DELETE FROM Client
        WHERE Client.id = id
        ;
    END;
//    

