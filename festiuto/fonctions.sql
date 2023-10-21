-- Inutile car les reservations concert/act annexe sont séparées
-- delimiter |
-- create or replace function getNbAvailablePlacesFestival(idFestival int) returns int
-- begin
--     declare nbPlacesTotalConcert int;
--     declare nbPlacesTotalActiviteAnnexe int;
--     declare nbPlacesUsed int;
--     declare nbPlacesAvailable int;
--     select sum(nbPlacesL) into nbPlacesTotalConcert from LIEU natural join CONCERT where idF = idFestival;
--     select sum(nbPlacesL) into nbPlacesTotalActiviteAnnexe from LIEU natural join ACTIVITEANNEXE where idF = idFestival;
--     select count(*) into nbPlacesUsed from BILLET where idF = idFestival;
--     set nbPlacesAvailable = nbPlacesTotalConcert + nbPlacesTotalActiviteAnnexe - nbPlacesUsed;
--     return nbPlacesAvailable;
-- end |
-- delimiter ;

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