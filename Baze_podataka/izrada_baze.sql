DROP DATABASE IF EXISTS Projektni;
CREATE DATABASE Projektni;
USE Projektni;

DROP USER IF EXISTS app;
CREATE USER app@'%' IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON Projektni.* TO app@'%';


CREATE TABLE ovlasti (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ovlast VARCHAR(100)
);

INSERT INTO ovlasti (ovlast) VALUES
	('Administrator'),
    ('Korisnik');

CREATE TABLE kartice (
	id INT PRIMARY KEY AUTO_INCREMENT,
    rfid VARCHAR(50) NOT NULL
);

INSERT INTO kartice (rfid) VALUES
	('16 fc de 12'),
    ('0c 10 db 2b'),
    ('94 24 09 1e'),
    ('75 ed e7 2b'),
    ('67 64 e8 2b');

CREATE TABLE korisnik (
	id INT PRIMARY KEY AUTO_INCREMENT,
    ime CHAR(50) NOT NULL,
    prezime CHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password BINARY(32) NOT NULL,
    id_ovlasti INT,
    id_kartice INT,
    FOREIGN KEY (id_ovlasti) REFERENCES ovlasti(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (id_kartice) REFERENCES kartice(id) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO korisnik (ime, prezime, username, password, id_ovlasti, id_kartice) VALUES
	('Marko', 'Antolić', 'mantolic', UNHEX(SHA2('qwer', 256)), 1, 1),
    ('Fran', 'Orlović', 'forlovic', UNHEX(SHA2('asdf', 256)), 1, 2),
    ('Pero', 'Perić', 'pperic', UNHEX(SHA2('1234', 256)), 2, 3),
    ('Ivo', 'Ivić', 'iivic', UNHEX(SHA2('4321', 256)), 2, 4),
    ('Stipe', 'Stipić', 'sstipic', UNHEX(SHA2('0000', 256)), 2, 5);

CREATE TABLE vrata (
	id INT PRIMARY KEY AUTO_INCREMENT,
    prostorija CHAR(100) NOT NULL
);

INSERT INTO vrata (prostorija) VALUES
	('Laboratorij'),
    ('Skladište');

CREATE TABLE dozvole_korisnika (
	id_korisnika INT NOT NULL,
    id_vrata INT NOT NULL,
    FOREIGN KEY (id_korisnika) REFERENCES korisnik(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_vrata) REFERENCES vrata(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (id_korisnika, id_vrata)
);

INSERT INTO dozvole_korisnika (id_korisnika, id_vrata) VALUES
	(1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 1),
    (5, 2);

CREATE TABLE rezultat (
	id INT PRIMARY KEY AUTO_INCREMENT,
    odobrenje CHAR(100) NOT NULL
);

INSERT INTO rezultat (odobrenje) VALUES
	('Dozvoljeno'),
    ('Odbijeno');

CREATE TABLE status_korisnika (
	id INT PRIMARY KEY AUTO_INCREMENT,
	id_korisnika INT NOT NULL,
    id_vrata INT NOT NULL,
    datum DATETIME,
    id_rezultata INT NOT NULL,
    FOREIGN KEY (id_korisnika) REFERENCES korisnik(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_vrata) REFERENCES vrata(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_rezultata) REFERENCES rezultat(id) ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO status_korisnika (id_korisnika, id_vrata, datum, id_rezultata) VALUES
	(3, 2, '2024-01-10 08:01:12', 1),
	(1, 1, '2024-01-10 08:40:13', 1),
    (1, 1, '2024-01-10 10:07:46', 1),
    (3, 2, '2024-01-10 16:04:32', 1),
    (3, 1, '2024-01-10 16:12:51', 2),
    (4, 2, '2024-01-11 07:49:13', 2),
    (4, 1, '2024-01-11 07:58:55', 1),
    (4, 1, '2024-01-11 14:41:59', 1),
    (2, 2, '2024-01-12 07:58:51', 1),
    (5, 2, '2024-01-12 08:04:42', 1),
    (2, 2, '2024-01-12 11:32:02', 1),
    (5, 2, '2024-01-12 15:43:01', 1),
    (1, 2, '2024-01-13 12:37:59', 1),
    (1, 2, '2024-01-13 12:48:42', 1),
    (5, 1, '2024-01-17 07:59:43', 2),
    (2, 1, '2024-01-17 09:14:14', 1),
    (1, 1, '2024-01-17 09:18:16', 1),
    (2, 1, '2024-01-17 10:57:25', 1),
    (1, 1, '2024-01-17 12:32:44', 1),
    (2, 2, '2024-01-17 11:17:03', 1),
    (2, 2, '2024-01-17 12:01:51', 1),
    (5, 1, '2024-01-18 08:32:33', 1),
    (5, 1, '2024-01-18 16:27:52', 1);
    

