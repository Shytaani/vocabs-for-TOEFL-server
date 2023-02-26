DROP TABLE IF EXISTS WORD;

CREATE TABLE WORD (
    ID INT NOT NULL PRIMARY KEY,
    WORD VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS DEFINITION;

CREATE TABLE DEFINITION (
    ID IDENTITY NOT NULL PRIMARY KEY,
    WORD_ID INT NOT NULL REFERENCES WORD(ID),
    DEFINITION VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS SENTENCE;

CREATE TABLE SENTENCE (
    ID IDENTITY NOT NULL PRIMARY KEY,
    WORD_ID INT NOT NULL REFERENCES WORD(ID),
    SENTENCE VARCHAR(255)
);