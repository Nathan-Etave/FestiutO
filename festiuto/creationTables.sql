CREATE TABLE FESTIVAL(
    idF INT,
    nomF VARCHAR(50),
    dateDebF DATE,
    dateFinF DATE,
    descriptionF VARCHAR(200),
    PRIMARY KEY (idF)
)ENGINE=InnoDB;

CREATE TABLE LIEU(
    idL INT,
    nomL VARCHAR(50),
    adresseL VARCHAR(50),
    nbPlacesL INT,
    PRIMARY KEY (idL)
)ENGINE=InnoDB;

CREATE TABLE INSTRUMENT(
    idI INT,
    nomI VARCHAR(50),
    PRIMARY KEY (idI)
)ENGINE=InnoDB;

CREATE TABLE STYLEMUSICAL(
    idS INT,
    nomS VARCHAR(50),
    PRIMARY KEY (idS)
)ENGINE=InnoDB;

CREATE TABLE PHOTO(
    idP INT,
    img LONGBLOB,
    PRIMARY KEY (idP)
)ENGINE=InnoDB;

CREATE TABLE HEBERGEMENT(
    idH INT,
    nomH VARCHAR(50),
    adresseH VARCHAR(50),
    nbPlacesH INT,
    PRIMARY KEY (idH)
)ENGINE=InnoDB;

CREATE TABLE ROLEUTI(
    idR INT,
    nomR VARCHAR(50),
    PRIMARY KEY (idR)
)ENGINE=InnoDB;

CREATE TABLE UTILISATEUR(
    idU INT,
    nomU VARCHAR(50),
    prenomU VARCHAR(50),
    mailU VARCHAR(50),
    mdpU VARCHAR(50),
    idR INT,
    PRIMARY KEY (idU),
    CONSTRAINT FK_Utilisateur FOREIGN KEY(idR) REFERENCES ROLEUTI(idR)
)ENGINE=InnoDB;

CREATE TABLE GROUPE(
    idG INT,
    nomG VARCHAR(50),
    descriptionG VARCHAR(150),
    idS INT,
    PRIMARY KEY (idG),
    CONSTRAINT FK_Groupe FOREIGN KEY(idS) REFERENCES STYLEMUSICAL(idS)
)ENGINE=InnoDB;

CREATE TABLE ARTISTE(
    idA INT,
    nomA VARCHAR(50),
    prenomA VARCHAR(50),
    idP INT,
    idG INT,
    PRIMARY KEY (idA),
    CONSTRAINT FK_Artiste_ph FOREIGN KEY(idP) REFERENCES PHOTO(idP),
    CONSTRAINT FK_Artiste_grp FOREIGN KEY(idG) REFERENCES GROUPE(idG)
)ENGINE=InnoDB;

CREATE TABLE JOUER(
    idA INT,
    idI INT,
    CONSTRAINT FK_Jouer_art FOREIGN KEY(idA) REFERENCES ARTISTE(idA),
    CONSTRAINT FK_Jouer_inst FOREIGN KEY(idI) REFERENCES INSTRUMENT(idI),
    PRIMARY KEY (idA, idI)
)ENGINE=InnoDB;

CREATE TABLE FAVORIS(
    idU INT,
    idG INT,
    PRIMARY KEY (idU,idG),
    CONSTRAINT FK_Favoris_uti FOREIGN KEY(idU) REFERENCES UTILISATEUR(idU),
    CONSTRAINT FK_Favoris_grp FOREIGN KEY(idG) REFERENCES GROUPE(idG)
)ENGINE=InnoDB;

CREATE TABLE CONCERT(
    idC INT,
    idF INT,
    idG INT,
    idL INT,
    dateDebC DATE,
    dateFinC DATE,
    dureeMontageC TIME,
    dureeDemontageC TIME,
    estGratuit BOOLEAN,
    PRIMARY KEY (idC),
    CONSTRAINT FK_Concert_fest FOREIGN KEY(idF) REFERENCES FESTIVAL(idF),
    CONSTRAINT FK_Concert_grp FOREIGN KEY(idG) REFERENCES GROUPE(idG),
    CONSTRAINT FK_Concert_lieu FOREIGN KEY(idL) REFERENCES LIEU(idL)
)ENGINE=InnoDB;

CREATE TABLE ACTIVITEANNEXE(
    idAct INT,
    nomAct VARCHAR(50),
    descriptionAct VARCHAR(150),
    dateDebAct DATE,
    dateFinAct DATE,
    idL INT,
    idF INT,
    idG INT,
    estPublique BOOLEAN,
    PRIMARY KEY (idAct),
    CONSTRAINT FK_ActiviteAnnexe_lieu FOREIGN KEY(idL) REFERENCES LIEU(idL),
    CONSTRAINT FK_ActiviteAnnexe_fest FOREIGN KEY(idF) REFERENCES FESTIVAL(idF),
    CONSTRAINT FK_ActiviteAnnexe_groupe FOREIGN KEY(idG) REFERENCES GROUPE(idG)
)ENGINE=InnoDB;

CREATE TABLE TYPEBILLET(
    idT INT,
    prixT FLOAT,
    descriptionT VARCHAR(150),
    PRIMARY KEY (idT)
)ENGINE=InnoDB;

CREATE TABLE BILLET(
    idB INT,
    idT INT,
    idU INT,
    idF INT,
    dateDebB date,
    dateFinB date,
    PRIMARY KEY (idB),
    CONSTRAINT FK_Billet_typeB FOREIGN KEY(idT) REFERENCES TYPEBILLET(idT),
    CONSTRAINT FK_Billet_uti FOREIGN KEY(idU) REFERENCES UTILISATEUR(idU),
    CONSTRAINT FK_Billet_fest FOREIGN KEY(idF) REFERENCES FESTIVAL(idF)
)ENGINE=InnoDB;

CREATE TABLE RESERVATION_CONCERT(
    idRes INT,
    idC INT,
    idU INT,
    PRIMARY KEY (idRes),
    CONSTRAINT FK_Reservation_conc FOREIGN KEY(idC) REFERENCES CONCERT(idC),
    CONSTRAINT FK_Reservation_uti_c FOREIGN KEY(idU) REFERENCES UTILISATEUR(idU)
)ENGINE=InnoDB;

CREATE TABLE RESERVATION_ACTIVITEANNEXE(
    idRes INT,
    idAct INT,
    idU INT,
    PRIMARY KEY (idRes),
    CONSTRAINT FK_Reservation_act FOREIGN KEY(idAct) REFERENCES ACTIVITEANNEXE(idAct),
    CONSTRAINT FK_Reservation_uti_an FOREIGN KEY(idU) REFERENCES UTILISATEUR(idU)
)ENGINE=InnoDB;

CREATE TABLE VIDEO(
    idV INT,
    lienV VARCHAR(250),
    PRIMARY KEY (idV)
)ENGINE=InnoDB;

CREATE TABLE RESEAUSOCIAL(
    idRs INT,
    idG INT,
    lienRs VARCHAR(250),
    PRIMARY KEY (idRs),
    CONSTRAINT FK_ReseauSocial FOREIGN KEY(idG) REFERENCES GROUPE(idG)
)ENGINE=InnoDB;

CREATE TABLE LOGER(
    idH INT,
    idG INT,
    dateDebH DATE,
    dateFinH DATE,
    PRIMARY KEY (idH,idG),
    CONSTRAINT FK_Loger_heb FOREIGN KEY(idH) REFERENCES HEBERGEMENT(idH),
    CONSTRAINT FK_Loger_grp FOREIGN KEY(idG) REFERENCES GROUPE(idG)
)ENGINE=InnoDB;

CREATE TABLE IMAGER_GROUPE(
    idG INT,
    idP INT,
    CONSTRAINT FK_ImagerGroupe FOREIGN KEY(idG) REFERENCES GROUPE(idG),
    CONSTRAINT FK_ImagerPhoto FOREIGN KEY(idP) REFERENCES PHOTO(idP),
    PRIMARY KEY (idG,idP)
)ENGINE=InnoDB;

CREATE TABLE VIDEO_GROUPE(
    idG INT,
    idV INT,
    CONSTRAINT FK_VideoGroupe FOREIGN KEY(idG) REFERENCES GROUPE(idG),
    CONSTRAINT FK_VideoVideo FOREIGN KEY(idV) REFERENCES VIDEO(idV),
    PRIMARY KEY (idG,idV)
)ENGINE=InnoDB;