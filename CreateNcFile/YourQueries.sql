select * from parseddocument where   LetterType='training' and SentenceNumber<500;
select * from parseddocument where   LetterType='validation';
select * from parseddocument where   LetterType='testing';
SET NAMES 'utf8' COLLATE 'utf8_general_ci';
ALTER DATABASE mstdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

select distinct DiacritizedCharacter,TargetSequenceEncodedWords from parseddocument;

select * from encodedwords;

select * from undiaconehotencoding;
select * from UnDiacOneHotEncoding where UnDiacritizedCharacter='' or UnDiacritizedCharacter='.';

select * from diaconehotencoding;
select DiacritizedCharacter from diaconehotencoding;

select * from ListOfWordsAndSentencesInEachDoc where word = '' ;
ALTER TABLE ListOfWordsAndSentencesInEachDoc CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
select * from ListOfWordsAndSentencesInEachDoc;


SET SQL_SAFE_UPDATES = 0;
delete  from parseddocument;
SET SQL_SAFE_UPDATES = 0;
delete  from encodedwords;
SET SQL_SAFE_UPDATES = 0;
delete  from ListOfWordsAndSentencesInEachDoc;
SET SQL_SAFE_UPDATES = 0;
delete  from diaconehotencoding;
SET SQL_SAFE_UPDATES = 0;
delete  from undiaconehotencoding;
SET SQL_SAFE_UPDATES = 1;

CREATE TABLE new_foo LIKE parseddocument;
RENAME TABLE parseddocument TO old_foo, new_foo TO parseddocument;
DROP TABLE old_foo;

CREATE TABLE new_foo LIKE encodedwords;
RENAME TABLE encodedwords TO old_foo, new_foo TO encodedwords;
DROP TABLE old_foo;

CREATE TABLE new_foo LIKE ListOfWordsAndSentencesInEachDoc;
RENAME TABLE ListOfWordsAndSentencesInEachDoc TO old_foo, new_foo TO ListOfWordsAndSentencesInEachDoc;
DROP TABLE old_foo;

SET SQL_SAFE_UPDATES = 0;
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, ' ', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, '[', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, ']', '');
UPDATE diaconehotencoding SET DiacritizedCharacterOneHotEncoding = REPLACE(DiacritizedCharacterOneHotEncoding, '\n', '');


SET SQL_SAFE_UPDATES = 0;
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, ' ', '');
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, '[', '');
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, ']', '');


-- reset auto increment column
SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE diaconehotencoding SET idDiacritizedCharacter = @num := (@num+1);
ALTER TABLE diaconehotencoding AUTO_INCREMENT =1;