-- RESERVATION
-- trigger vérication nombre de places dans un concert
delimiter |
create or replace trigger verifNbPlacesConcert before insert on RESERVATION for each row
begin
    declare nbPersonnesInscrites int;
    declare nbPersonnesBillet int;
    declare nbPlacesLieu int;
    select count(*) into nbPersonnesInscrites from RESERVATION where idC=new.idC;
    select count(*) into nbPersonnesBillet from BILLET NATURAL JOIN FESTIVAL NATURAL JOIN CONCERT where idC=new.idC and dateDebC>=dateDebB and dateFinC<=dateFinB;
    select nbPlacesL into nbPlacesLieu from LIEU where idL=new.idL;
    if nbPersonnesInscrites+nbPersonnesBillet>=nbPlacesLieu or nbPlacesLieu<0 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="trop de personnes pour ce concert";
    end if;
end |
demiliter ;

-- CONCERT
-- trigger vérication date de concert/act dans un meme lieu (pas de concert en meme temps dans un meme lieu)
delimiter |
create or replace trigger verifDateConcert before insert on CONCERT for each row
begin
    declare nbConcertsMemeDate int;
    select count(*) into nbConcertsMemeDate from CONCERT where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    select count(*) into nbConcertsMemeDate from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    if nbConcertsMemeDate>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="date de concert déjà prise dans ce lieu";
    end if;
end |
demiliter ;

-- trigger vérification date de concert dans un meme groupe (pas de concert/activité en meme temps dans un meme groupe)
delimiter |
create or replace trigger verifDateGroupe before insert on CONCERT for each row
begin
    declare nbConcertsMemeDate int;
    declare nbActivitesMemeDate int;
    select count(*) into nbConcertsMemeDate from CONCERT where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    select count(*) into nbConcertsMemeDate from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    if nbConcertsMemeDate+nbActivitesMemeDate>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    end if;
end |
demiliter ;

-- trigger vérification date de activité dans un meme groupe (pas de concert/activité en meme temps dans un meme groupe)
delimiter |
create or replace trigger verifDateGroupe before insert on CONCERT for each row
begin
    declare nbConcertsMemeDate int;
    declare nbActivitesMemeDate int;
    select count(*) into nbConcertsMemeDate from CONCERT where idG=new.idG and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    select count(*) into nbConcertsMemeDate from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    if nbConcertsMemeDate+nbActivitesMemeDate>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    end if;
end |
demiliter ;

--ACTIVITEANNEXE
-- trigger vérication date de concert/act dans un meme lieu (pas d'act en meme temps dans un meme lieu)
delimiter |
create or replace trigger verifDateConcert before insert on ACTIVITEANNEXE for each row
begin
    declare nbConcertsMemeDate int;
    select count(*) into nbConcertsMemeDate from CONCERT where idL=new.idL and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    select count(*) into nbConcertsMemeDate from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    if nbConcertsMemeDate>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="date de concert déjà prise dans ce lieu";
    end if;
end |
demiliter ;

--LOGER
-- trigger vérification assez de places pour un groupe dans un hébergement
delimiter |
create or replace trigger verifPlacesHebergement before insert on LOGER for each row -- pas fini
begin
    declare nbPersonnesHebergee int;
    declare nbPlacesHebergement int;
    select count(*) into nbPersonnesHebergement from GROUPE NATURAL JOIN ARTISTE where idG=new.idG;
    select nbPlacesH into nbPlacesHebergement from HEBERGEMENT where idH=new.idH;
    if nbPersonnesHebergement>nbPlacesHebergement then
        signal SQLSTATE '45000' set MESSAGE_TEXT="pas assez de places dans cet hébergement";
    end if;
end |
delimiter ;
