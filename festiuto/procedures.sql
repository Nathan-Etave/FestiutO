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