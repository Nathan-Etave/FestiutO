DROP TABLE ACTIVITEANNEXE CASCADE CONSTRAINTS;
DROP TABLE FAVORIS CASCADE CONSTRAINTS;
DROP TABLE CONCERT CASCADE CONSTRAINTS;
DROP TABLE GROUPE CASCADE CONSTRAINTS;
DROP TABLE JOUER CASCADE CONSTRAINTS;
DROP TABLE ARTISTE CASCADE CONSTRAINTS;
DROP TABLE UTILISATEUR CASCADE CONSTRAINTS;
DROP TABLE ROLEUTI CASCADE CONSTRAINTS;
DROP TABLE HEBERGEMENT CASCADE CONSTRAINTS;
DROP TABLE PHOTO CASCADE CONSTRAINTS;
DROP TABLE STYLEMUSICAL CASCADE CONSTRAINTS;
DROP TABLE INSTRUMENT CASCADE CONSTRAINTS;
DROP TABLE LIEU CASCADE CONSTRAINTS;
DROP TABLE FESTIVAL CASCADE CONSTRAINTS;


CREATE TABLE FESTIVAL(
    idF INT,
    nomF VARCHAR(50),
    dateDebF DATE,
    dateFinF DATE,
    descriptionF VARCHAR(150),
    PRIMARY KEY (idF)
);

CREATE TABLE LIEU(
    idL INT,
    nomL VARCHAR(50),
    adresseL VARCHAR(50),
    nbPlacesL INT,
    PRIMARY KEY (idL)
);

CREATE TABLE INSTRUMENT(
    idI INT,
    nomL VARCHAR(50),
    PRIMARY KEY (idI)
);

CREATE TABLE STYLEMUSICAL(
    idS INT,
    nomS VARCHAR(50),
    PRIMARY KEY (idS)
);

CREATE TABLE PHOTO(
    idP INT,
    img LONGBLOB,
    PRIMARY KEY(idP)
);

CREATE TABLE HEBERGEMENT(
    idH INT,
    nomH VARCHAR(50),
    adresseH VARCHAR(50),
    nbPlacesH INT,
    PRIMARY KEY (idH)
);

CREATE TABLE ROLEUTI(
    idR INT,
    nomS VARCHAR(50),
    PRIMARY KEY (idR)
);

CREATE TABLE UTILISATEUR(
    idU INT,
    nomU VARCHAR(50),
    prenomU VARCHAR(50),
    mailU VARCHAR(50),
    mdpU VARCHAR(50),
    idR INT,
    PRIMARY KEY (idU),
    FOREIGN KEY (idR) REFERENCES ROLE(idR)
);

CREATE TABLE ARTISTE(
    idA INT,
    nomA VARCHAR(50),
    prenomA VARCHAR(50),
    idP INT,
    PRIMARY KEY (idA),
    FOREIGN KEY (idP) REFERENCES PHOTO(idP)
);

CREATE TABLE JOUER(
    idA INT,
    idI INT,
    PRIMARY KEY (idA,idI)
)

CREATE TABLE GROUPE(
    idG INT,
    nomG VARCHAR(50),
    descriptionG VARCHAR(150),
    reseauxG VARCHAR(250),
    videosG VARCHAR(250),
    idH INT,
    PRIMARY KEY (idG),
    FOREIGN KEY (idH) REFERENCES HEBERGEMENT(idH)
);

CREATE TABLE FAVORIS(
    idU INT,
    idG INT,
    PRIMARY KEY (idU,idG)
    FOREIGN KEY (idU) REFERENCES UTILISATEUR(idU),
    FOREIGN KEY (idG) REFERENCES GROUPE(idG)
);

CREATE TABLE CONCERT(
    idC INT,
    idF INT,
    idG INT,
    idL INT,
    dateDebC DATE,
    dateFinC DATE,
    dureeMontageC TIME,
    dureeDemontageC TIME,
    PRIMARY KEY (idC),
    FOREIGN KEY (idF) REFERENCES FESTIVAL(idF),
    FOREIGN KEY (idG) REFERENCES GROUPE(idG),
    FOREIGN KEY (idL) REFERENCES LIEU(idL)
);

CREATE TABLE ACTIVITEANNEXE(
    idAct INT,
    nomAct VARCHAR(50),
    descriptionAct VARCHAR(150),
    dateDebAct DATE,
    dateFinAct DATE,
    idL INT,
    estPublique BOOLEAN,
    PRIMARY KEY (idAct),
    FOREIGN KEY (idL) REFERENCES LIEU(idL)
);

CREATE TABLE TYPEBILLET(
    idT INT,
    prixT FLOAT,
    descriptionT VARCHAR(150),
    PRIMARY KEY (idT)
);

CREATE TABLE BILLET(
    idB INT,
    idT INT,
    idU INT,
    idF INT,
    -- dateDebB date, ?
    -- dateFinB date, ?
    PRIMARY KEY (idB),
    FOREIGN KEY (idT) REFERENCES TYPEBILLET(idT),
    FOREIGN KEY (idU) REFERENCES UTILISATEUR(idU),
    FOREIGN KEY (idF) REFERENCES FESTIVAL(idF)
);
-- voir pour la date si elle est stockée dans le billet (pour ceux qui ne durent pas tout le festival)
-- selection dans un menu pendant l'achat et ajout de la date dans le billet ?

CREATE TABLE RESERVATION(
    idRes INT,
    idC INT,
    idU INT,
    PRIMARY KEY (idRes),
    FOREIGN KEY (idC) REFERENCES CONCERT(idC),
    FOREIGN KEY (idU) REFERENCES UTILISATEUR(idU),
);
-- 1 réservation par personne par concert ? -> clé primaire devient idC et idU et on peut enlever idRes

CREATE TABLE VIDEO(
    idV INT,
    lienV VARCHAR(250),
    PRIMARY KEY (idV)
);

CREATE TABLE RESEAUSOCIAL(
    idRs INT,
    lienRs VARCHAR(250),
    PRIMARY KEY (idRs)
);

-- 1 utilisateur peut réserver plusieurs places (pour des amis/famille/...) sur son compte ?
-- si oui autoriser plusieurs réservations ou indiquer un nombre de place dans la réservation