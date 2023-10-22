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
    img MEDIUMBLOB,
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
    lienV VARCHAR(150),
    PRIMARY KEY (idV)
)ENGINE=InnoDB;

CREATE TABLE RESEAUSOCIAL(
    idRs INT,
    lienRs VARCHAR(150),
    PRIMARY KEY (idRs)
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

CREATE TABLE RESEAUSOCIAL_GROUPE(
    idG INT,
    idRs INT,
    CONSTRAINT FK_ReseauSocialGroupe FOREIGN KEY(idG) REFERENCES GROUPE(idG),
    CONSTRAINT FK_ReseauSocialReseauSocial FOREIGN KEY(idRs) REFERENCES RESEAUSOCIAL(idRs),
    PRIMARY KEY (idG,idRs)
)ENGINE=InnoDB;

delimiter |
create or replace procedure addGroup (nomGroupe VARCHAR(50), descriptionGroupe VARCHAR(150), idStyle INT)
begin
    declare newIdG int;
    select max(idG)+1 into newIdG from GROUPE;
    insert into GROUPE (idG, nomG, descriptionG, idS) values (newIdG, nomGroupe, descriptionGroupe, idStyle);
end |
delimiter ;

delimiter |
create or replace procedure addArtist (nomArtiste VARCHAR(50), prenomArtiste VARCHAR(50), idPhoto INT, idGroupe INT)
begin
    declare newIdA int;
    select max(idA)+1 into newIdA from ARTISTE;
    if idPhoto is null then
        insert into ARTISTE (idA, nomA, prenomA, idP, idG) values (newIdA, nomArtiste, prenomArtiste, null, idGroupe);
    else
        insert into ARTISTE (idA, nomA, prenomA, idP, idG) values (newIdA, nomArtiste, prenomArtiste, idPhoto, idGroupe);
    end if;
end |
delimiter ;

delimiter |
create or replace procedure addInstrumentToArtist (idArtiste INT, idInstrument INT)
begin
    insert into JOUER (idA, idI) values (idArtiste, idInstrument);
end |

delimiter |
create or replace procedure addAnnexActivity (nomActivite VARCHAR(50), descriptionActivite VARCHAR(150), dateDebActivite DATE, dateFinActivite DATE, idLieu INT, ifFestival INT, idGroupe INT, estPublique BOOLEAN)
begin
    declare newIdActivite int;
    select max(idAct)+1 into newIdActivite from ACTIVITEANNEXE;
    if idGroupe is null then
        insert into ACTIVITEANNEXE (idAct, nomAct, descriptionAct, dateDebAct, dateFinAct, idL, idF, idG, estPublique) values (newIdActivite, nomActivite, descriptionActivite, dateDebActivite, dateFinActivite, idLieu, ifFestival, null, estPublique);
    else
        insert into ACTIVITEANNEXE (idAct, nomAct, descriptionAct, dateDebAct, dateFinAct, idL, idF, idG, estPublique) values (newIdActivite, nomActivite, descriptionActivite, dateDebActivite, dateFinActivite, idLieu, ifFestival, idGroupe, estPublique);
    end if;
end |
delimiter ;

delimiter |
create or replace procedure sellTicket (idTypeBillet INT, idUtilisateur INT, idFestival INT, dateDebBillet DATE, dateFinBillet DATE)
begin
    declare newIdBillet int;
    select max(idB)+1 into newIdBillet from BILLET;
    insert into BILLET (idB, idT, idU, idF, dateDebB, dateFinB) values (newIdBillet, idTypeBillet, idUtilisateur, idFestival, dateDebBillet, dateFinBillet);
end |
delimiter ;

delimiter |
create or replace procedure addUser (nomUtilisateur VARCHAR(50), prenomUtilisateur VARCHAR(50), mailUtilisateur VARCHAR(50), mdpUtilisateur VARCHAR(50), idRole INT)
begin
    declare newIdUtilisateur int;
    select max(idU)+1 into newIdUtilisateur from UTILISATEUR;
    insert into UTILISATEUR (idU, nomU, prenomU, mailU, mdpU, idR) values (newIdUtilisateur, nomUtilisateur, prenomUtilisateur, mailUtilisateur, mdpUtilisateur, idRole);
end |
delimiter ;

delimiter |
create or replace procedure addGroupVideo (lienVideo VARCHAR(150), idGroupe INT)
begin
    declare newIdVideo int;
    select max(idV)+1 into newIdVideo from VIDEO;
    insert into VIDEO (idV, lienV) values (newIdVideo, lienVideo);
    insert into VIDEO_GROUPE (idG, idV) values (idGroupe, newIdVideo);
end |
delimiter ;

delimiter |
create or replace procedure addGroupPhoto (photo VARCHAR(150), idGroupe INT)
begin
    declare newIdPhoto int;
    select max(idP)+1 into newIdPhoto from PHOTO;
    insert into PHOTO (idP, img) values (newIdPhoto, photo);
    insert into IMAGER_GROUPE (idG, idP) values (idGroupe, newIdPhoto);
end |
delimiter ;

delimiter |
create or replace procedure addGroupSocialNetwork (lienSocialNetwork VARCHAR(150), idGroupe INT)
begin
    declare newIdSocialNetwork int;
    select max(idRs)+1 into newIdSocialNetwork from RESEAUSOCIAL;
    insert into RESEAUSOCIAL (idRs, lienRs) values (newIdSocialNetwork, lienSocialNetwork);
    insert into RESEAUSOCIAL_GROUPE (idG, idRs) values (idGroupe, newIdSocialNetwork);
end |
delimiter ;

delimiter |
create or replace procedure addFestival (nomFestival VARCHAR(50), dateDebFestival DATE, dateFinFestival DATE, descriptionFestival VARCHAR(200))
begin
    declare newIdFestival int;
    select max(idF)+1 into newIdFestival from FESTIVAL;
    insert into FESTIVAL (idF, nomF, dateDebF, dateFinF, descriptionF) values (newIdFestival, nomFestival, dateDebFestival, dateFinFestival, descriptionFestival);
end |
delimiter ;

delimiter |
create or replace procedure addConcert (idFestival INT, idGroupe INT, idLieu INT, dateDebConcert DATE, dateFinConcert DATE, dureeMontage TIME, dureeDemontage TIME, estGratuit BOOLEAN)
begin
    declare newIdConcert int;
    select max(idC)+1 into newIdConcert from CONCERT;
    insert into CONCERT (idC, idF, idG, idL, dateDebC, dateFinC, dureeMontageC, dureeDemontageC, estGratuit) values (newIdConcert, idFestival, idGroupe, idLieu, dateDebConcert, dateFinConcert, dureeMontage, dureeDemontage, estGratuit);
end |
delimiter ;

delimiter |
create or replace procedure addReservationConcert (idConcert INT, idUtilisateur INT)
begin
    declare newIdReservation int;
    select max(idRes)+1 into newIdReservation from RESERVATION_CONCERT;
    insert into RESERVATION_CONCERT (idRes, idC, idU) values (newIdReservation, idConcert, idUtilisateur);
end |
delimiter ;

delimiter |
create or replace procedure addReservationAnnexActivity (idActivite INT, idUtilisateur INT)
begin
    declare newIdReservation int;
    select max(idRes)+1 into newIdReservation from RESERVATION_ACTIVITEANNEXE;
    insert into RESERVATION_ACTIVITEANNEXE (idRes, idAct, idU) values (newIdReservation, idActivite, idUtilisateur);
end |
delimiter ;

delimiter |
create or replace procedure addTypeBillet (nomTypeBillet VARCHAR(50), prixTypeBillet FLOAT, descriptionTypeBillet VARCHAR(150))
begin
    declare newIdTypeBillet int;
    select max(idT)+1 into newIdTypeBillet from TYPEBILLET;
    insert into TYPEBILLET (idT, nomT, prixT, descriptionT) values (newIdTypeBillet, nomTypeBillet, prixTypeBillet, descriptionTypeBillet);
end |
delimiter ;

delimiter |
create or replace procedure updateGroup (idGroupe INT, nomGroupe VARCHAR(50), descriptionGroupe VARCHAR(150), idStyle INT)
begin
    update GROUPE set nomG=nomGroupe, descriptionG=descriptionGroupe, idS=idStyle where idG=idGroupe;
end |
delimiter ;

delimiter |
create or replace procedure updateArtist (idArtiste INT, nomArtiste VARCHAR(50), prenomArtiste VARCHAR(50), idPhoto INT, idGroupe INT)
begin
    if idPhoto is null then
        update ARTISTE set nomA=nomArtiste, prenomA=prenomArtiste, idP=null, idG=idGroupe where idA=idArtiste;
    else
        update ARTISTE set nomA=nomArtiste, prenomA=prenomArtiste, idP=idPhoto, idG=idGroupe where idA=idArtiste;
    end if;
end |

delimiter |
create or replace procedure updateInstrumentToArtist (idArtiste INT, idInstrument INT)
begin
    update JOUER set idI=idInstrument where idA=idArtiste;
end |

delimiter |
create or replace procedure updateAnnexActivity (idActivite INT, nomActivite VARCHAR(50), descriptionActivite VARCHAR(150), dateDebActivite DATE, dateFinActivite DATE, idLieu INT, ifFestival INT, idGroupe INT, estPublique BOOLEAN)
begin
    if idGroupe is null then
        update ACTIVITEANNEXE set nomAct=nomActivite, descriptionAct=descriptionActivite, dateDebAct=dateDebActivite, dateFinAct=dateFinActivite, idL=idLieu, idF=ifFestival, idG=null, estPublique=estPublique where idAct=idActivite;
    else
        update ACTIVITEANNEXE set nomAct=nomActivite, descriptionAct=descriptionActivite, dateDebAct=dateDebActivite, dateFinAct=dateFinActivite, idL=idLieu, idF=ifFestival, idG=idGroupe, estPublique=estPublique where idAct=idActivite;
    end if;
end |
delimiter ;

delimiter |
create or replace procedure updateUser (idUtilisateur INT, nomUtilisateur VARCHAR(50), prenomUtilisateur VARCHAR(50), mailUtilisateur VARCHAR(50), mdpUtilisateur VARCHAR(50), idRole INT)
begin
    update UTILISATEUR set nomU=nomUtilisateur, prenomU=prenomUtilisateur, mailU=mailUtilisateur, mdpU=mdpUtilisateur, idR=idRole where idU=idUtilisateur;
end |
delimiter ;

delimiter |
create or replace procedure updateGroupVideo (idVideo INT, lienVideo VARCHAR(150), idGroupe INT)
begin
    update VIDEO set lienV=lienVideo where idV=idVideo;
    update VIDEO_GROUPE set idG=idGroupe where idV=idVideo;
end |
delimiter ;

delimiter |
create or replace procedure updateGroupPhoto (idPhoto INT, photo VARCHAR(150), idGroupe INT)
begin
    update PHOTO set img=photo where idP=idPhoto;
    update IMAGER_GROUPE set idG=idGroupe where idP=idPhoto;
end |
delimiter ;

delimiter |
create or replace procedure updateGroupSocialNetwork (idSocialNetwork INT, lienSocialNetwork VARCHAR(150), idGroupe INT)
begin
    update RESEAUSOCIAL set lienRs=lienSocialNetwork where idRs=idSocialNetwork;
    update RESEAUSOCIAL_GROUPE set idG=idGroupe where idRs=idSocialNetwork;
end |
delimiter ;

delimiter |
create or replace procedure updateFestival (idFestival INT, nomFestival VARCHAR(50), dateDebFestival DATE, dateFinFestival DATE, descriptionFestival VARCHAR(200))
begin
    update FESTIVAL set nomF=nomFestival, dateDebF=dateDebFestival, dateFinF=dateFinFestival, descriptionF=descriptionFestival where idF=idFestival;
end |
delimiter ;

delimiter |
create or replace procedure updateConcert (idConcert INT, idFestival INT, idGroupe INT, idLieu INT, dateDebConcert DATE, dateFinConcert DATE, dureeMontage TIME, dureeDemontage TIME, estGratuit BOOLEAN)
begin
    update CONCERT set idF=idFestival, idG=idGroupe, idL=idLieu, dateDebC=dateDebConcert, dateFinC=dateFinConcert, dureeMontageC=dureeMontage, dureeDemontageC=dureeDemontage, estGratuit=estGratuit where idC=idConcert;
end |
delimiter ;

delimiter |
create or replace procedure deleteGroup (idGroupe INT)
begin
    delete from GROUPE where idG=idGroupe;
end |
delimiter ;

delimiter |
create or replace procedure deleteArtist (idArtiste INT)
begin
    delete from ARTISTE where idA=idArtiste;
end |
delimiter ;

delimiter |
create or replace procedure deleteInstrumentToArtist (idArtiste INT, idInstrument INT)
begin
    delete from JOUER where idA=idArtiste and idI=idInstrument;
end |
delimiter ;

delimiter |
create or replace procedure deleteAnnexActivity (idActivite INT)
begin
    delete from ACTIVITEANNEXE where idAct=idActivite;
end |
delimiter ;

delimiter |
create or replace procedure deleteUser (idUtilisateur INT)
begin
    delete from UTILISATEUR where idU=idUtilisateur;
end |
delimiter ;

delimiter |
create or replace procedure deleteGroupVideo (idVideo INT)
begin
    delete from VIDEO where idV=idVideo;
    delete from VIDEO_GROUPE where idV=idVideo;
end |
delimiter ;

delimiter |
create or replace procedure deleteGroupPhoto (idPhoto INT)
begin
    delete from PHOTO where idP=idPhoto;
    delete from IMAGER_GROUPE where idP=idPhoto;
end |
delimiter ;

delimiter |
create or replace procedure deleteGroupSocialNetwork (idSocialNetwork INT)
begin
    delete from RESEAUSOCIAL where idRs=idSocialNetwork;
    delete from RESEAUSOCIAL_GROUPE where idRs=idSocialNetwork;
end |
delimiter ;

delimiter |
create or replace procedure deleteFestival (idFestival INT)
begin
    delete from FESTIVAL where idF=idFestival;
end |
delimiter ;

delimiter |
create or replace procedure deleteConcert (idConcert INT)
begin
    delete from CONCERT where idC=idConcert;
end |
delimiter ;

delimiter |
create or replace procedure deleteReservationConcert (idReservation INT)
begin
    delete from RESERVATION_CONCERT where idRes=idReservation;
end |
delimiter ;

delimiter |
create or replace procedure deleteReservationAnnexActivity (idReservation INT)
begin
    delete from RESERVATION_ACTIVITEANNEXE where idRes=idReservation;
end |
delimiter ;

delimiter |
create or replace procedure updateTicketDate (idBillet INT, dateDebBillet DATE, dateFinBillet DATE)
begin
    update BILLET set dateDebB=dateDebBillet, dateFinB=dateFinBillet where idB=idBillet;
end |
delimiter ;

delimiter |
create or replace procedure rentAccomodation (idHebergement INT, idGroupe INT, dateDebHebergement DATE, dateFinHebergement DATE)
begin
    insert into LOGER (idH, idG, dateDebH, dateFinH) values (idHebergement, idGroupe, dateDebHebergement, dateFinHebergement);
end |
delimiter ;

delimiter |
create or replace procedure addAccomodation (nomHebergement VARCHAR(50), adresseHebergement VARCHAR(150), nbPlacesHebergement INT)
begin
    declare newIdHebergement int;
    select max(idH)+1 into newIdHebergement from HEBERGEMENT;
    insert into HEBERGEMENT (idH, nomH, adresseH, nbPlacesH) values (newIdHebergement, nomHebergement, adresseHebergement, nbPlacesHebergement);
end |
delimiter ;

delimiter |
create or replace procedure updateAccomodation (idHebergement INT, nomHebergement VARCHAR(50), adresseHebergement VARCHAR(150), nbPlacesHebergement INT)
begin
    update HEBERGEMENT set nomH=nomHebergement, adresseH=adresseHebergement, nbPlacesH=nbPlacesHebergement where idH=idHebergement;
end |
delimiter ;

delimiter |
create or replace procedure deleteAccomodation (idHebergement INT)
begin
    delete from HEBERGEMENT where idH=idHebergement;
end |
delimiter ;

delimiter |
create or replace procedure addPlace (nomLieu VARCHAR(50), adresseLieu VARCHAR(150), nbPlacesLieu INT)
begin
    declare newIdLieu int;
    select max(idL)+1 into newIdLieu from LIEU;
    insert into LIEU (idL, nomL, adresseL, nbPlacesL) values (newIdLieu, nomLieu, adresseLieu, nbPlacesLieu);
end |
delimiter ;

delimiter |
create or replace procedure updatePlace (idLieu INT, nomLieu VARCHAR(50), adresseLieu VARCHAR(150), nbPlacesLieu INT)
begin
    update LIEU set nomL=nomLieu, adresseL=adresseLieu, nbPlacesL=nbPlacesLieu where idL=idLieu;
end |
delimiter ;

delimiter |
create or replace procedure deletePlace (idLieu INT)
begin
    delete from LIEU where idL=idLieu;
end |
delimiter ;

delimiter |
create or replace procedure addStyle (nomStyle VARCHAR(50))
begin
    declare newIdStyle int;
    select max(idS)+1 into newIdStyle from STYLEMUSICAL;
    insert into STYLEMUSICAL (idS, nomS) values (newIdStyle, nomStyle);
end |
delimiter ;

delimiter |
create or replace procedure updateStyle (idStyle INT, nomStyle VARCHAR(50))
begin
    update STYLEMUSICAL set nomS=nomStyle where idS=idStyle;
end |
delimiter ;

delimiter |
create or replace procedure deleteStyle (idStyle INT)
begin
    delete from STYLEMUSICAL where idS=idStyle;
end |
delimiter ;

delimiter |
create or replace procedure addInstrument (nomInstrument VARCHAR(50))
begin
    declare newIdInstrument int;
    select max(idI)+1 into newIdInstrument from INSTRUMENT;
    insert into INSTRUMENT (idI, nomI) values (newIdInstrument, nomInstrument);
end |
delimiter ;

delimiter |
create or replace procedure updateInstrument (idInstrument INT, nomInstrument VARCHAR(50))
begin
    update INSTRUMENT set nomI=nomInstrument where idI=idInstrument;
end |
delimiter ;

delimiter |
create or replace procedure deleteInstrument (idInstrument INT)
begin
    delete from INSTRUMENT where idI=idInstrument;
end |
delimiter ;

delimiter |
create or replace procedure addFavorite (idUtilisateur INT, idGroupe INT)
begin
    insert into FAVORIS (idU, idG) values (idUtilisateur, idGroupe);
end |
delimiter ;

delimiter |
create or replace procedure deleteFavorite (idUtilisateur INT, idGroupe INT)
begin
    delete from FAVORIS where idU=idUtilisateur and idG=idGroupe;
end |
delimiter ;

delimiter |
create or replace function getNbAvailablePlacesConcert(idConcert int) returns int
begin
    declare nbPlacesTotal int;
    declare nbPlacesUsed int;
    declare nbPlacesAvailable int;
    select nbPlacesL into nbPlacesTotal from LIEU natural join CONCERT where idC = idConcert;
    select count(*) into nbPlacesUsed from RESERVATION_CONCERT where idC = idConcert;
    set nbPlacesAvailable = nbPlacesTotal - nbPlacesUsed;
    return nbPlacesAvailable;
end |
delimiter ;

delimiter |
create or replace function getNbAvailablePlacesActiviteAnnexe(idActiviteAnnexe int) returns int
begin
    declare nbPlacesTotal int;
    declare nbPlacesUsed int;
    declare nbPlacesAvailable int;
    select nbPlacesL into nbPlacesTotal from LIEU natural join ACTIVITEANNEXE where idAct = idActiviteAnnexe;
    select count(*) into nbPlacesUsed from RESERVATION_ACTIVITEANNEXE where idAct = idActiviteAnnexe;
    set nbPlacesAvailable = nbPlacesTotal - nbPlacesUsed;
    return nbPlacesAvailable;
end |
delimiter ;

delimiter |
create or replace function getTicketPrice(idTicket int) returns float
begin
    declare price float;
    select prixT into price from TYPEBILLET where idT = idTicket;
    return price;
end |
delimiter ;

delimiter |
create or replace function getListUserReservationsConcert(idUser int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idC) into list from RESERVATION_CONCERT where idU = idUser;
    return list;
end |
delimiter ;

delimiter |
create or replace function getListUserReservationsActiviteAnnexe(idUser int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idAct) into list from RESERVATION_ACTIVITEANNEXE where idU = idUser;
    return list;
end |
delimiter ;

delimiter |
create or replace function getListUserTickets(idUser int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idB) into list from BILLET where idU = idUser;
    return list;
end |
delimiter ;

delimiter |
create or replace function getListUserFavoris(idUser int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idG) into list from FAVORIS where idU = idUser;
    return list;
end |
delimiter ;

delimiter |
create or replace function getArtistPicture(idArtist int) returns mediumblob
begin 
    declare picture mediumblob;
    select img into picture from PHOTO natural join ARTISTE where idA = idArtist;
    return picture;
end |
delimiter ;

delimiter |
create or replace function getConcertsFestival(idFestival int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idC) into list from CONCERT where idF = idFestival;
    return list;
end |
delimiter ;

delimiter |
create or replace function getActivitesAnnexesFestival(idFestival int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idAct) into list from ACTIVITEANNEXE where idF = idFestival;
    return list;
end |
delimiter ;

delimiter |
create or replace function getListUserReservationsConcertFestival(idUser int, idFestival int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idC) into list from RESERVATION_CONCERT natural join CONCERT where idU = idUser and idF = idFestival;
    return list;
end |
delimiter ;

delimiter |
create or replace function getListUserReservationsActiviteAnnexeFestival(idUser int, idFestival int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idAct) into list from RESERVATION_ACTIVITEANNEXE natural join ACTIVITEANNEXE where idU = idUser and idF = idFestival;
    return list;
end |
delimiter ;

delimiter |
create or replace function getFestivalsGroupParticipates(idGroup int) returns varchar(1000)
begin 
    declare list varchar(1000);
    select group_concat(idF) into list from CONCERT where idG = idGroup;
    return list;
end |
delimiter ;

delimiter |
create or replace function getFestivalRemainingTime(idFestival int) returns varchar(1000)
begin 
    declare remainingTime varchar(1000);
    select datediff(dateFinF, now()) into remainingTime from FESTIVAL where idF = idFestival;
    return remainingTime;
end |
delimiter ;

delimiter |
create or replace function getConcertRemainingTime(idConcert int) returns varchar(1000)
begin 
    declare remainingTime varchar(1000);
    select datediff(dateFinC, now()) into remainingTime from CONCERT where idC = idConcert;
    return remainingTime;
end |
delimiter ;

delimiter |
create or replace function getActiviteAnnexeRemainingTime(idActiviteAnnexe int) returns varchar(1000)
begin 
    declare remainingTime varchar(1000);
    select datediff(dateFinAct, now()) into remainingTime from ACTIVITEANNEXE where idAct = idActiviteAnnexe;
    return remainingTime;
end |
delimiter ;

delimiter |
create or replace function getGroupSocialNetwork(idGroup int) returns varchar(1000)
begin 
    declare socialNetwork varchar(1000);
    select group_concat(lienRs) into socialNetwork from RESEAUSOCIAL_GROUPE RG natural join RESEAUSOCIAL where RG.idG = idGroup;
    return socialNetwork;
end |
delimiter ;

-- RESERVATION_CONCERT
-- trigger vérication nombre de places dans un concert
delimiter |
create or replace trigger verifNbPlacesConcert before insert on RESERVATION_CONCERT for each row
begin
    declare nbPersonnesInscrites int;
    declare nbPersonnesBillet int;
    declare nbPlacesLieu int;
    select count(*) into nbPersonnesInscrites from RESERVATION_CONCERT where idC=new.idC;
    select count(*) into nbPersonnesBillet from BILLET NATURAL JOIN FESTIVAL NATURAL JOIN CONCERT where idC=new.idC and dateDebC>=dateDebB and dateFinC<=dateFinB;
    select nbPlacesL into nbPlacesLieu from LIEU natural join CONCERT where idC=new.idC;
    if nbPersonnesInscrites+nbPersonnesBillet>=nbPlacesLieu or nbPlacesLieu<0 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="trop de personnes pour ce concert";
    end if;
end |
delimiter ;

-- affiner les triggers /!\

-- CONCERT
-- trigger vérication date de concert/act dans un meme lieu (pas de concert en meme temps dans un meme lieu)
delimiter |
create or replace trigger verifDateConcertCon before insert on CONCERT for each row
begin
    -- declare nbConcertsMemeDate1 int;
    -- declare nbActiviteMemeDate1 int;

    -- declare nbConcertsMemeDate2 int;
    -- declare nbActivitesMemeDate2 int;

    declare hDebutC datetime;
    declare hFinC datetime;
    declare hDebutF datetime;
    declare hFinF datetime;

    -- select count(*) into nbConcertsMemeDate1 from CONCERT where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    -- select count(*) into nbActiviteMemeDate1 from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    -- if nbConcertsMemeDate1+nbActiviteMemeDate1>=1 then
    --     signal SQLSTATE '45000' set MESSAGE_TEXT="lieu déjà pris à cette date";
    -- end if;

    -- select count(*) into nbConcertsMemeDate2 from CONCERT where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    -- select count(*) into nbActivitesMemeDate2 from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    -- if nbConcertsMemeDate2+nbActivitesMemeDate2>=1 then
    --     signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    -- end if;  

    select dateDebC, dateFinC into hDebutC, hFinC from CONCERT where idC = new.idC;
    select dateDebF, dateFinF into hDebutF, hFinF from FESTIVAL where idF = new.idF;
    if hDebutC < hDebutF or hFinC > hFinF then
        signal SQLSTATE '45000' set MESSAGE_TEXT="Le concert n'est pas compris dans les horaires du festival";
    end if;

end |
delimiter ;

--ACTIVITEANNEXE
-- trigger vérication date de concert/act dans un meme lieu (pas d'act en meme temps dans un meme lieu)

delimiter |
create or replace trigger verifDateConcertAct before insert on ACTIVITEANNEXE for each row
begin
    -- declare nbConcertsMemeDate1 int;
    -- declare nbActivitesMemeDate1 int;

    -- declare nbConcertsMemeDate2 int;
    -- declare nbActivitesMemeDate2 int;

    declare hDebutA datetime;
    declare hFinA datetime;
    declare hDebutF datetime;
    declare hFinF datetime;

    -- select count(*) into nbConcertsMemeDate1 from CONCERT where idL=new.idL and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    -- select count(*) into nbActivitesMemeDate1 from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    -- if nbConcertsMemeDate1+nbActivitesMemeDate1>=1 then
    --     signal SQLSTATE '45000' set MESSAGE_TEXT="lieu déjà pris à cette date";
    -- end if;

    -- select count(*) into nbConcertsMemeDate2 from CONCERT where idG=new.idG and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    -- select count(*) into nbActivitesMemeDate2 from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    -- if nbConcertsMemeDate2+nbActivitesMemeDate2>=1 then
    --     signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    -- end if;  

    select dateDebAct, dateFinAct into hDebutA, hFinA from ACTIVITEANNEXE where idAct = new.idAct;
    select dateDebF, dateFinF into hDebutF, hFinF from FESTIVAL where idF = new.idF;
    if hDebutA < hDebutF or hFinA > hFinF then
        signal SQLSTATE '45000' set MESSAGE_TEXT="L'activitée n'est pas compris dans les horaires du festival";
    end if;
end |
delimiter ;

--LOGER
-- trigger vérification assez de places pour un groupe dans un hébergement
delimiter |
create or replace trigger verifPlacesHebergement before insert on LOGER for each row -- pas fini
begin
    declare nbPersonnesHebergee int;
    declare nbPlacesHebergement int;
    declare nbPersonnesGroupe int;
    select count(*) into nbPersonnesGroupe from GROUPE NATURAL JOIN ARTISTE where idG=new.idG;
    select count(*) into nbPersonnesHebergee from ARTISTE natural join LOGER where idH=new.idH;
    select nbPlacesH into nbPlacesHebergement from HEBERGEMENT where idH=new.idH;
    if nbPersonnesHebergee+nbPersonnesGroupe>nbPlacesHebergement then
        signal SQLSTATE '45000' set MESSAGE_TEXT="pas assez de places dans cet hébergement";
    end if;
end |
delimiter ;

-- Concert
-- Festival
-- Hebergement
-- Billet
-- Activite

delimiter |
create or replace trigger verifDateConcert before insert on CONCERT for each row
begin
    if new.dateDebC < NOW() then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le concert ne peux pas débuter antérieurement";
    elseif new.dateDebC > new.dateFinC then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le concert ne peux pas être terminer avant d'avoir commencé";
    end if;
end |
delimiter ;

delimiter |
create or replace trigger verifDateFestival before insert on FESTIVAL for each row
begin
    if new.dateDebF < NOW() then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le festival ne peux pas débuter antérieurement";
    elseif new.dateDebF > new.dateFinF then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le festival ne peux pas être terminer avant d'avoir commencé";
    end if;
end |
delimiter ;