select  SentenceNumber from parseddocument where LetterType='testing' limit 1;

select * from parseddocument where   LetterType='training' ;
select * from parseddocument where   LetterType='validation';
select * from parseddocument where   LetterType='testing' and SentenceNumber = 4592 ;

select distinct word from parseddocument where   LetterType='testing' order by idCharacterNumber asc;
select Word from parseddocument where LetterType='testing' order by idCharacterNumber asc;
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


insert into dictionary (DiacritizedWord,UnDiacritizedWord)(select word, UnDiacritizedWord from parseddocument group by word order by UnDiacritizedWord asc);
select * from dictionary;

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
SET SQL_SAFE_UPDATES = 0;
delete from alldiacriticsinalldocuments;
SET SQL_SAFE_UPDATES = 0;
delete from distinctdiacritics;
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

SET SQL_SAFE_UPDATES = 0;
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ' ', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, '[', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ']', '');

-- reset auto increment column
SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE distinctdiacritics SET id = @num := (@num+1);
ALTER TABLE distinctdiacritics AUTO_INCREMENT =1;

insert into diaconehotencoding (idDiacritizedCharacter, DiacritizedCharacter) values (422, 'عًّ');

delete from diaconehotencoding where idDiacritizedCharacter = 422;

select * from alldiacriticsinalldocuments;
insert into alldiacriticsinalldocuments (Diacritics) values ('عًّ');
select distinct * from alldiacriticsinalldocuments group by Diacritics;
select * from alldiacriticsinalldocuments where id=7236;
UPDATE alldiacriticsinalldocuments SET Diacritics = SUBSTR(Diacritics, 1);

select * from distinctdiacritics;
select * from parseddocument where   LetterType='testing';
SET SQL_SAFE_UPDATES = 0;
delete from parseddocument where DocName = 'Ala7adWeAlmathany';
-- delete from ListOfWordsAndSentencesInEachDoc where DocName = 'Ala7adWeAlmathany';
delete from EncodedWords where docName = 'Ala7adWeAlmathany';

select * from diaconehotencoding where DiacritizedCharacter='عًّ';


select distinct diacritics from parseddocument;

delete from distinctdiacritics where id = 2
