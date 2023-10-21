delimiter |
create or replace function getNbAvailablePlacesFestival(idFestival int) returns int
begin
    declare nbPlacesTotalConcert int;
    declare nbPlacesTotalActiviteAnnexe int;
    declare nbPlacesUsed int;
    declare nbPlacesAvailable int;
    select sum(nbPlacesL) into nbPlacesTotalConcert from LIEU natural join CONCERT where idF = idFestival;
    select sum(nbPlacesL) into nbPlacesTotalActiviteAnnexe from LIEU natural join ACTIVITEANNEXE where idF = idFestival;
    select count(*) into nbPlacesUsed from BILLET where idF = idFestival;
    set nbPlacesAvailable = nbPlacesTotalConcert + nbPlacesTotalActiviteAnnexe - nbPlacesUsed;
    return nbPlacesAvailable;
end |
delimiter ;