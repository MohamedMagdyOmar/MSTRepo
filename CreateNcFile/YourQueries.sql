select  * from parseddocument where LetterType='testing' limit 290;
select  * from parseddocument where idCharacterNumber < 1172930;
select * from parseddocument where UnDiacritizedCharacter = '+';
select distinct DocName from parseddocument where   LetterType='training';
select * from parseddocument where   LetterType='training' ;
select * from parseddocument where   LetterType='validation';
select * from parseddocument where   LetterType ='testing' and SentenceNumber <= 5102  ;
select distinct word from parseddocument where   LetterType='testing' order by idCharacterNumber asc;
select Word from parseddocument where LetterType='testing' order by idCharacterNumber asc;
select * from dictionary;
select distinct DiacritizedCharacter,TargetSequenceEncodedWords from parseddocument;
select * from encodedwords;
select * from undiaconehotencoding;
select * from UnDiacOneHotEncoding where UnDiacritizedCharacter='' or UnDiacritizedCharacter='.';
select * from diaconehotencoding;
select DiacritizedCharacter from diaconehotencoding;
select * from ListOfWordsAndSentencesInEachDoc where word = '' ;
select * from ListOfWordsAndSentencesInEachDoc;
select * from distinctdiacritics;
select * from parseddocument where   LetterType='testing';
select * from diaconehotencoding where DiacritizedCharacter='عًّ';
select distinct diacritics from parseddocument;
select distinct * from alldiacriticsinalldocuments group by Diacritics;
select * from alldiacriticsinalldocuments where id=7236;
select * from alldiacriticsinalldocuments;
select * from dictionary where UnDiacritizedWord = 'إنا';
SET NAMES 'utf8' COLLATE 'utf8_general_ci';
ALTER DATABASE mstdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- reset auto increment column
SET SQL_SAFE_UPDATES = 0;
SET  @num := 0;
UPDATE parseddocument SET idCharacterNumber = @num := (@num+1);
ALTER TABLE parseddocument AUTO_INCREMENT =1;


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
SET SQL_SAFE_UPDATES = 0;
delete from dictionary;
delete from parseddocument where DocName = 'Ala7adWeAlmathany';
delete from EncodedWords where docName = 'Ala7adWeAlmathany';
delete from distinctdiacritics where id = 2;
delete from diaconehotencoding where idDiacritizedCharacter = 422;
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
UPDATE undiaconehotencoding SET UnDiacritizedCharacterOneHotEncoding = REPLACE(UnDiacritizedCharacterOneHotEncoding, '\n', '');

SET SQL_SAFE_UPDATES = 0;
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ' ', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, '[', '');
UPDATE distinctdiacritics SET encoding = REPLACE(encoding, ']', '');



ALTER TABLE ListOfWordsAndSentencesInEachDoc CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

insert into diaconehotencoding (idDiacritizedCharacter, DiacritizedCharacter) values (422, 'عًّ');
insert into alldiacriticsinalldocuments (Diacritics) values ('عًّ');
UPDATE alldiacriticsinalldocuments SET Diacritics = SUBSTR(Diacritics, 1);
insert into dictionary (DiacritizedWord,UnDiacritizedWord)(select word, UnDiacritizedWord from parseddocument group by word order by UnDiacritizedWord asc);


select distinct SentenceNumber, DocName from listofwordsandsentencesineachdoc;

update parseddocument Set LetterType = 'training' where idCharacterNumber < 1172931;

update parseddocument Set LetterType = 'testing' where idCharacterNumber >= 1172931;

select distinct DocName, SentenceNumber from parseddocument where LetterType = 'testing' order by  idCharacterNumber asc;

select * from 
listofwordsandsentencesineachdoc where DocName='ANN20021015.0100.txt'



