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
create or replace procedure addReservation (idConcert INT, idUtilisateur INT)
begin
    declare newIdReservation int;
    select max(idRes)+1 into newIdReservation from RESERVATION;
    insert into RESERVATION (idRes, idC, idU) values (newIdReservation, idConcert, idUtilisateur);
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
create or replace procedure deleteReservation (idReservation INT)
begin
    delete from RESERVATION where idRes=idReservation;
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
