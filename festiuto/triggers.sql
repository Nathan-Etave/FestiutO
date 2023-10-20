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
    declare nbConcertsMemeDate1 int;
    declare nbActiviteMemeDate1 int;

    declare nbConcertsMemeDate2 int;
    declare nbActivitesMemeDate2 int;

    declare hDebutC datetime;
    declare hFinC datetime;
    declare hDebutF datetime;
    declare hFinF datetime;

    select count(*) into nbConcertsMemeDate1 from CONCERT where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    select count(*) into nbActiviteMemeDate1 from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    if nbConcertsMemeDate1+nbActiviteMemeDate1>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="date de concert déjà prise dans ce lieu";
    end if;

    select count(*) into nbConcertsMemeDate2 from CONCERT where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinC+dureeDemontageC or new.dateFinC+new.dureeDemontageC<=dateDebC-dureeMontageC);
    select count(*) into nbActivitesMemeDate2 from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebC-new.dureeMontageC>=dateFinAct or new.dateFinC+new.dureeDemontageC<=dateDebAct);
    if nbConcertsMemeDate2+nbActivitesMemeDate2>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    end if;  

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
    declare nbConcertsMemeDate1 int;
    declare nbActivitesMemeDate1 int;

    declare nbConcertsMemeDate2 int;
    declare nbActivitesMemeDate2 int;

    declare hDebutA datetime;
    declare hFinA datetime;
    declare hDebutF datetime;
    declare hFinF datetime;

    select count(*) into nbConcertsMemeDate1 from CONCERT where idL=new.idL and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    select count(*) into nbActivitesMemeDate1 from ACTIVITEANNEXE where idL=new.idL and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    if nbConcertsMemeDate1+nbActivitesMemeDate1>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="date de concert déjà prise dans ce lieu";
    end if;

    select count(*) into nbConcertsMemeDate2 from CONCERT where idG=new.idG and not (new.dateDebAct>=dateFinC+dureeDemontageC or new.dateFinAct<=dateDebC-dureeMontageC);
    select count(*) into nbActivitesMemeDate2 from ACTIVITEANNEXE where idG=new.idG and not (new.dateDebAct>=dateFinAct or new.dateFinAct<=dateDebAct);
    if nbConcertsMemeDate2+nbActivitesMemeDate2>=1 then
        signal SQLSTATE '45000' set MESSAGE_TEXT="le groupe joue déjà à cette date";
    end if;  

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