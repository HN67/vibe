USE vibe;

CREATE TABLE Mood (
    name NVARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE Taste (
    type NVARCHAR(255) NOT NULL,
    PRIMARY KEY (type)
);

CREATE TABLE Scent (
    name NVARCHAR(255) NOT NULL,
    family NVARCHAR(255),
    PRIMARY KEY (name)
);

CREATE TABLE Shape (
    name NVARCHAR(255) NOT NULL,
    sides INT,
    PRIMARY KEY (name)
);

CREATE TABLE Color (
    name NVARCHAR(255) NOT NULL,
    hue INT NOT NULL,
    saturation INT NOT NULL,
    brightness INT NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE MediaGenre (
    name NVARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE MusicGenre (
    name NVARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE User (
    id INT NOT NULL AUTO_INCREMENT,
    username NVARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE Admin (
    id INT NOT NULL,
    permissions INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id)
        REFERENCES User(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Client (
    id INT NOT NULL,
    birthday DATE,
    email NVARCHAR(255),
    displayName NVARCHAR(255),
    bio NVARCHAR(4095),
    PRIMARY KEY (id),
    FOREIGN KEY (id)
        REFERENCES User(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Result (
    clientId INT NOT NULL,
    number INT NOT NULL AUTO_INCREMENT,
    mood NVARCHAR(255),
    taste NVARCHAR(255),
    scent NVARCHAR(255),
    shape NVARCHAR(255),
    color NVARCHAR(255),
    media NVARCHAR(255),
    music NVARCHAR(255),
    PRIMARY KEY (number),
    FOREIGN KEY (clientId)
        REFERENCES Client(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (taste)
        REFERENCES Taste(type)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (scent)
        REFERENCES Scent(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (shape)
        REFERENCES Color(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (color)
        REFERENCES Color(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (media)
        REFERENCES MediaGenre(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (music)
        REFERENCES MusicGenre(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE TasteAffects (
    taste NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (taste, mood),
    FOREIGN KEY (taste)
        REFERENCES Taste(type)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE ScentAffects (
    scent NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (scent, mood),
    FOREIGN KEY (scent)
        REFERENCES Scent(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE ShapeAffects (
    shape NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (shape, mood),
    FOREIGN KEY (shape)
        REFERENCES Shape(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE ColorAffects (
    color NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (color, mood),
    FOREIGN KEY (color)
        REFERENCES Color(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE MediaAffects (
    media NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (media, mood),
    FOREIGN KEY (media)
        REFERENCES MediaGenre(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE MusicAffects (
    music NVARCHAR(255) NOT NULL,
    mood NVARCHAR(255) NOT NULL,
    PRIMARY KEY (music, mood),
    FOREIGN KEY (music)
        REFERENCES MusicGenre(name)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (mood)
        REFERENCES Mood(name)
        ON UPDATE CASCADE ON DELETE RESTRICT
);
