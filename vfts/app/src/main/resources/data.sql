INSERT INTO WORD SELECT * FROM CSVREAD('classpath:data/word.csv');
INSERT INTO DEFINITION SELECT * FROM CSVREAD('classpath:data/definition.csv');
INSERT INTO SENTENCE SELECT * FROM CSVREAD('classpath:data/sentence.csv');