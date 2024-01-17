import base64
from sqlalchemy import func, null
from sqlalchemy.orm import joinedload, aliased
from festiuto.models import (Session, ACTIVITE_ANNEXE, ARTISTE, BILLET, CONCERT, FAVORIS, FESTIVAL, GROUPE, HEBERGEMENT,
                             IMAGER_GROUPE, INSTRUMENT, JOUER, LIEU, LOGER, PHOTO, RESEAU_SOCIAL, RESEAU_SOCIAL_GROUPE,
                             RESERVATION_ACTIVITE_ANNEXE, RESERVATION_CONCERT, ROLE_UTILISATEUR, STYLE_MUSICAL, TYPE_BILLET,
                             UTILISATEUR, VIDEO, VIDEO_GROUPE)

def get_user_by_email(email):
    try:
        session = Session()
        user = session.query(UTILISATEUR).filter(UTILISATEUR.mailU == email).first()
        return user
    except:
        print("L'utilisateur n'existe pas")
        raise
    finally:
        session.close()

def get_mdp_by_email(email):
    try:
        session = Session()
        user = session.query(UTILISATEUR).filter(UTILISATEUR.mailU == email).first()
        return user.mdpU
    except:
        print("L'utilisateur n'existe pas")
        raise
    finally:
        session.close()

def hasher_mdp(mdp):
    import hashlib
    return hashlib.sha256(mdp.encode()).hexdigest()

def get_all_concerts():
    try:
        session = Session()
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).order_by(CONCERT.dateDebC).all()
        return concerts
    except:
        raise
    finally:
        session.close()

def get_groupe_by_idC(idC):
    try:
        session = Session()
        groupe = session.query(CONCERT, GROUPE, STYLE_MUSICAL).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).filter(CONCERT.idC == idC).first()
        return groupe
    except:
        raise
    finally:
        session.close()

def get_roles():
    try:
        session = Session()
        roles = session.query(ROLE_UTILISATEUR).all()
        return roles
    except:
        raise
    finally:
        session.close()

def get_last_idU():
    try:
        session = Session()
        result = session.query(UTILISATEUR).order_by(UTILISATEUR.idU.desc()).first()
        if result is None:
            return 0
        return result.idU
    except:
        raise
    finally:
        session.close()

def get_last_idH():
    try:
        session = Session()
        result = session.query(HEBERGEMENT).order_by(HEBERGEMENT.idH.desc()).first()
        if result is None:
            return 0
        return result.idH
    except:
        raise
    finally:
        session.close()

def get_last_idB():
    try:
        session = Session()
        result = session.query(BILLET).order_by(BILLET.idB.desc()).first()
        if result is None:
            return 0
        return result.idB
    except:
        raise
    finally:
        session.close()

def get_last_idG():
    try:
        session = Session()
        result = session.query(GROUPE).order_by(GROUPE.idG.desc()).first()
        if result is None:
            return 0
        return result.idG
    except:
        raise
    finally:
        session.close()

def get_last_idA():
    try:
        session = Session()
        result = session.query(ARTISTE).order_by(ARTISTE.idA.desc()).first()
        if result is None:
            return 0
        return result.idA
    except:
        raise
    finally:
        session.close()

def get_last_idAct():
    try:
        session = Session()
        result = session.query(ACTIVITE_ANNEXE).order_by(ACTIVITE_ANNEXE.idAct.desc()).first()
        if result is None:
            return 0
        return result.idAct
    except:
        raise
    finally:
        session.close()

def get_last_idC():
    try:
        session = Session()
        result = session.query(CONCERT).order_by(CONCERT.idC.desc()).first()
        if result is None:
            return 0
        return result.idC
    except:
        raise
    finally:
        session.close()

def insert_user(mail,prenom,nom,mdp):
    try:
        session = Session()
        user = UTILISATEUR(idU=get_last_idU() + 1, nomU=nom, prenomU=prenom, mailU=mail, mdpU=mdp, idR=3)
        session.add(user)
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_billet_by_idU(idU):
    try:
        session = Session()
        session.query(BILLET).filter_by(idU=idU).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_user(idU):
    try:
        session = Session()
        session.query(UTILISATEUR).filter_by(idU=idU).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_billet(idT,idU,dateDebB, dateFinB, quantite):
    try:
        session = Session()
        for i in range(quantite):
            billet = BILLET(idB=get_last_idB() + i + 1, idT=idT, idU=idU, idF=1, dateDebB=dateDebB, dateFinB=dateFinB)
            session.add(billet)
        session.commit()
    except:
        raise
    finally:
        session.close()

def get_concerts_by_datetime(datetime):
    """Récupère tous les concerts en cours ou à l'horaire donné

    Args:
        datetime (datetime): Date et heure de début du concert (YYYY-MM-DD HH:MM:SS)

    Returns:
        List: Liste des concerts
    """
    try:
        session = Session()
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL).select_from(CONCERT).join(GROUPE).join(
            STYLE_MUSICAL).filter(CONCERT.dateDebC <= datetime).filter(CONCERT.dateFinC > datetime).all()
        return concerts
    except:
        raise
    finally:
        session.close()

def get_concerts_by_day(day):
    try:
        session = Session()
        all_concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL, LIEU).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).join(LIEU).order_by(CONCERT.dateDebC).all()
        concerts = []
        for concert in all_concerts:
            if concert.CONCERT.dateDebC.day == day:
                concerts.append(concert)
        return concerts
    except:
        raise
    finally:
        session.close()

def get_concerts_with_search(search):
    session = Session()
    try:
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL) \
            .options(joinedload(CONCERT.lieu), joinedload(CONCERT.groupe)) \
            .select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).filter(GROUPE.nomG.like("%" + search + "%")).order_by(CONCERT.dateDebC).all()
        for concert in concerts:
            _ = concert.CONCERT.festival
            _ = concert.CONCERT.reservation_concert_collection
            _ = concert.GROUPE.stylemusical
            _ = concert.GROUPE.utilisateur_collection
            _ = concert.GROUPE.reseausocial_collection
            _ = concert.GROUPE.concert_collection
            _ = concert.GROUPE.video_collection
            _ = concert.GROUPE.photo_collection
            _ = concert.GROUPE.artiste_collection
            _ = concert.GROUPE.loger_collection
            _ = concert.GROUPE.activiteannexe_collection
            _ = concert.STYLEMUSICAL.groupe_collection
        return concerts
    except:
        raise
    finally:
        session.close()

def get_concerts_with_id(id):
    try:
        session = Session()
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).filter(CONCERT.idC == id).first()
        return concerts
    except:
        raise
    finally:
        session.close()

def get_concerts_idC():
    try:
        session = Session()
        concerts = session.query(CONCERT.idC).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).all()
        return concerts
    except:
        raise
    finally:
        session.close()

def get_concerts_with_idG(idG):
    try:
        session = Session()
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL, LIEU).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).join(LIEU).filter(GROUPE.idG == idG).all()
        return concerts
    except:
        raise
    finally:
        session.close()

def get_activites_with_idG(idG):
    try:
        session = Session()
        activites = session.query(ACTIVITE_ANNEXE, GROUPE, STYLE_MUSICAL, LIEU).select_from(ACTIVITE_ANNEXE).join(GROUPE).join(STYLE_MUSICAL).join(LIEU).filter(ACTIVITE_ANNEXE.idG == idG).all()
        return activites
    except:
        raise
    finally:
        session.close()

def get_artistes_with_idG(idG):
    try:
        session = Session()
        artistes = session.query(ARTISTE).filter(ARTISTE.idG == idG).all()
        return artistes
    except:
        raise
    finally:
        session.close()

def get_groupe_with_idG(idG):
    try:
        session = Session()
        groupe = session.query(GROUPE,STYLE_MUSICAL).select_from(GROUPE).join(STYLE_MUSICAL).filter(GROUPE.idG == idG).first()
        return groupe
    except:
        raise
    finally:
        session.close()

def get_groupe_related(idG):
    try:
        style_musical = get_groupe_with_idG(idG).STYLEMUSICAL.idS
        session = Session()
        groupe = session.query(GROUPE).filter(GROUPE.idS == style_musical).filter(GROUPE.idG != idG).all() #.limit(2) pour limiter les résultats
        return groupe
    except:
        raise
    finally:
        session.close()

def ajouter_favori(idU,idG):
    try:
        session = Session()
        session.execute(FAVORIS.insert().values(idU=idU,idG=idG))
        session.commit()
    except:
        raise
    finally:
        session.close()

def supprimer_favori(idU,idG):
    try:
        session = Session()
        session.query(FAVORIS).filter_by(idU=idU).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def is_favori(idU,idG):
    try:
        session = Session()
        all_fav = session.query(FAVORIS).filter_by(idU=idU).all()
        for fav in all_fav:
            if fav.idG == idG:
                return True
        return False
    except:
        raise
    finally:
        session.close()

def get_favoris(idU):
    try:
        session = Session()
        all_fav = session.query(FAVORIS).filter_by(idU=idU).all()
        favoris = []
        for fav in all_fav:
            favoris.append(get_groupe_with_idG(fav.idG))
        return favoris
    except:
        raise
    finally:
        session.close()

def get_billets_with_idU(idU):
    try:
        session = Session()
        billets = session.query(BILLET, TYPE_BILLET, func.count(BILLET.idB).label('quantite'), (func.count(BILLET.idB) * TYPE_BILLET.prixT).label('sous_total')).select_from(BILLET).join(TYPE_BILLET).filter(BILLET.idU == idU).group_by(BILLET.dateDebB, BILLET.idT).all()
        total = 0
        for billet in billets: total += billet[-1]
        return billets,total
    except:
        raise
    finally:
        session.close()

def get_user(idU):
    try:
        session = Session()
        user = session.query(UTILISATEUR).filter(UTILISATEUR.idU == idU).first()
        print(user)
        return user
    except:
        raise
    finally:
        session.close()

def get_total_panier(idU):
    try:
        session = Session()
        total = session.query(func.sum(BILLET.idB).label('total')).select_from(BILLET).join(TYPE_BILLET).filter(BILLET.idU == idU).first()
        return total
    except:
        raise
    finally:
        session.close()

def get_groupes():
    try:
        session = Session()
        groupes = session.query(GROUPE).all()
        return groupes
    except:
        raise
    finally:
        session.close()

def get_groupes_with_search(search):
    try:
        session = Session()
        groupes = session.query(GROUPE).filter(GROUPE.nomG.like("%" + search + "%")).all()
        return groupes
    except:
        raise
    finally:
        session.close()

def get_artistes():
    try:
        session = Session()
        artistes = session.query(ARTISTE).all()
        return artistes
    except:
        raise
    finally:
        session.close()

def get_artiste_with_search(search):
    try:
        session = Session()
        artistes = session.query(ARTISTE).filter(ARTISTE.nomA.like("%" + search + "%") | ARTISTE.prenomA.like("%" + search + "%")).all()
        return artistes
    except:
        raise
    finally:
        session.close()

def get_artiste_with_idA(idA):
    try:
        session = Session()
        artiste = session.query(ARTISTE).filter(ARTISTE.idA == idA).first()
        return artiste
    except:
        raise
    finally:
        session.close()

def get_spectateurs():
    try:
        session = Session()
        spectateurs = session.query(UTILISATEUR).filter(UTILISATEUR.idR == 3).all()
        return spectateurs
    except:
        raise
    finally:
        session.close()

def get_spectateurs_with_search(search):
    try:
        session = Session()
        spectateurs = session.query(UTILISATEUR).filter(UTILISATEUR.nomU.like("%" + search + "%") | UTILISATEUR.prenomU.like("%" + search + "%")).filter(UTILISATEUR.idR == 3).all()
        return spectateurs
    except:
        raise
    finally:
        session.close()

def get_hebergements():
    try:
        session = Session()
        hebergements = session.query(HEBERGEMENT).all()
        return hebergements
    except:
        raise
    finally:
        session.close()

def get_hebergement_with_idH(idH):
    try:
        session = Session()
        hebergement = session.query(HEBERGEMENT).filter(HEBERGEMENT.idH == idH).first()
        return hebergement
    except:
        raise
    finally:
        session.close()

def get_hebergements_with_search(search):
    try:
        session = Session()
        hebergements = session.query(HEBERGEMENT).filter(HEBERGEMENT.nomH.like("%" + search + "%")).all()
        return hebergements
    except:
        raise
    finally:
        session.close()

def insert_hebergement(nomH,adresseH,nbPlacesH):
    try:
        session = Session()
        hebergement = HEBERGEMENT(idH=get_last_idH() + 1, nomH=nomH, adresseH=adresseH, nbPlacesH=nbPlacesH)
        session.add(hebergement)
        session.commit()
    except:
        raise
    finally:
        session.close()

def get_lodging_with_idH(idH):
    try:
        session = Session()
        lodging = session.query(LOGER, GROUPE).select_from(LOGER).join(GROUPE).filter(LOGER.idH == idH).all()
        return lodging
    except:
        raise
    finally:
        session.close()


def get_billets():
    try:
        session = Session()
        billets = session.query(BILLET).all()
        return billets
    except:
        raise
    finally:
        session.close()

def insert_groupe(nomG,idS,descG):
    try:
        session = Session()
        groupe = GROUPE(idG=get_last_idG() + 1, idS=idS, nomG=nomG, descriptionG=descG)
        session.add(groupe)
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_groupe(idG):
    try:
        session = Session()
        session.query(GROUPE).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def get_last_idP():
    try:
        session = Session()
        result = session.query(PHOTO).order_by(PHOTO.idP.desc()).first()
        if result is None:
            return 0
        return result.idP
    except:
        raise
    finally:
        session.close()

def update_groupe(idG,nomG,idS,descG, images):
    try:
        session = Session()
        liste_images = [] 
        for image in images:
            photo = PHOTO(idP=get_last_idP() + 1, img=base64.b64encode(image.read()))
            liste_images.append(photo)
            session.add(photo)
            session.commit()
        session.query(IMAGER_GROUPE).filter_by(idG=idG).delete()
        session.commit()
        for image in liste_images:
            session.execute(IMAGER_GROUPE.insert().values(idG=idG,idP=image.idP))
        groupe = session.query(GROUPE).filter_by(idG=idG).first()
        groupe.nomG = nomG
        groupe.idS = idS
        groupe.descriptionG = descG
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_reservation(idH,idG,dateDeb,dateFin):
    try:
        session = Session()
        reservation = LOGER(idH=idH, idG=idG, dateDebH=dateDeb, dateFinH=dateFin)
        session.add(reservation)
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_artiste(nomA,prenomA,idG):
    try:
        session = Session()
        artiste = ARTISTE(idA=get_last_idA() + 1, nomA=nomA, prenomA=prenomA, idP=1, idG=idG)
        session.add(artiste)
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_artiste(idA):
    try:
        session = Session()
        session.query(ARTISTE).filter_by(idA=idA).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def update_artiste(idA,nomA,prenomA,idG):
    try:
        session = Session()
        artiste = session.query(ARTISTE).filter_by(idA=idA).first()
        artiste.nomA = nomA
        artiste.prenomA = prenomA
        artiste.idG = idG
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_activite(idG,nomA,descA,idL,dateDebA,dateFinA,estPublique):
    try:
        session = Session()
        activite = ACTIVITE_ANNEXE(idAct=get_last_idAct() + 1, nomAct=nomA, descriptionAct=descA, dateDebAct=dateDebA, dateFinAct=dateFinA, idL=idL, idF=1, idG=idG, estPublique=estPublique)
        session.add(activite)
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_concert(idG,idL,dateDebC,dateFinC,dureeMontageC,dureeDemontageC,estGratuit):
    try:
        session = Session()
        concert = CONCERT(idC=get_last_idC() + 1, idF=1, idG=idG, idL=idL, dateDebC=dateDebC, dateFinC=dateFinC, dureeMontageC=dureeMontageC, dureeDemontageC=dureeDemontageC, estGratuit=estGratuit)
        session.add(concert)
        session.commit()
    except:
        raise
    finally:
        session.close()

def get_billet_by_idB(idB):
    try:
        session = Session()
        billet = session.query(BILLET).filter(BILLET.idB == idB).first()
        return billet
    except:
        raise
    finally:
        session.close()

def is_user_billet(idU, idB):
    try:
        session = Session()
        billet = session.query(BILLET).filter(BILLET.idB == idB).first()
        if billet.idU == idU:
            return True
        return False
    except:
        raise
    finally:
        session.close()

def remove_billet_from_panier(idU, idT, dateDebB, dateFinB):
    try:
        session = Session()
        billets = session.query(BILLET).filter(BILLET.idU == idU).filter(BILLET.idT == idT).filter(BILLET.dateDebB == dateDebB).filter(BILLET.dateFinB == dateFinB).all()
        session.delete(billets[0])
        session.commit()
        return len(billets) - 1, billets[1].idB if len(billets) > 1 else None
    except:
        return 0
    finally:
        session.close()

def add_billet_to_panier(idU, idT, dateDebB, dateFinB):
    try:
        session = Session()
        billet = BILLET(idB=get_last_idB() + 1, idT=idT, idU=idU, idF=1, dateDebB=dateDebB, dateFinB=dateFinB)
        session.add(billet)
        session.commit()
        return len(session.query(BILLET).filter(BILLET.idU == idU).filter(BILLET.idT == idT).filter(BILLET.dateDebB == dateDebB).filter(BILLET.dateFinB == dateFinB).all()), billet.idB
    except:
        raise
    finally:
        session.close()

def get_prix_billet(idT):
    try:
        session = Session()
        billet = session.query(TYPE_BILLET).filter(TYPE_BILLET.idT == idT).first()
        return billet.prixT
    except:
        raise
    finally:
        session.close()

def get_styles():
    try:
        session = Session()
        styles = session.query(STYLE_MUSICAL).all()
        return styles
    except:
        raise
    finally:
        session.close()

def get_lieux():
    try:
        session = Session()
        lieux = session.query(LIEU).all()
        return lieux
    except:
        raise
    finally:
        session.close()

def nb_artiste_with_idG(idG):
    try:
        session = Session()
        nb_artiste = session.query(ARTISTE).filter(ARTISTE.idG == idG).count()
        return nb_artiste
    except:
        raise
    finally:
        session.close()

def get_instruments():
    try:
        session = Session()
        instruments = session.query(INSTRUMENT).all()
        return instruments
    except:
        raise
    finally:
        session.close()

def get_instrument_with_idA(idA):
    try:
        session = Session()
        instrument_alias = aliased(INSTRUMENT)
        instruments = session.query(JOUER, instrument_alias).select_from(JOUER).join(instrument_alias, JOUER.c.idI == instrument_alias.idI).filter(JOUER.c.idA == idA).all()
        return instruments
    except:
        raise
    finally:
        session.close()

def delete_instrument(idA,idI):
    try:
        session = Session()
        session.query(JOUER).filter_by(idA=idA,idI=idI).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_instrument(idA,idI):
    try:
        session = Session()
        session.execute(JOUER.insert().values(idA=idA,idI=idI)) 
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_concert_with_idG(idG):
    try:
        session = Session()
        session.query(CONCERT).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_activites_with_idG(idG):
    try:
        session = Session()
        session.query(ACTIVITE_ANNEXE).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_artistes_with_idG(idG):
    try:
        session = Session()
        session.query(ARTISTE).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_revervation_with_idG(idG):
    try:
        session = Session()
        session.query(LOGER).filter_by(idG=idG).delete()
        session.commit()
    except:
        raise
    finally:
        session.close()

def delete_favoris_with_idG(idG):
    try:
        session = Session()
        session.execute(FAVORIS.delete().values(idG=idG))
        session.commit()
    except:
        raise
    finally:
        session.close()

def get_images_with_idG(idG):
    try:
        session = Session()
        photo_alias = aliased(PHOTO)
        images = session.query(IMAGER_GROUPE, photo_alias).select_from(IMAGER_GROUPE).join(photo_alias, IMAGER_GROUPE.c.idP == photo_alias.idP).filter(IMAGER_GROUPE.c.idG == idG).all()
        return images
    except:
        raise
    finally:
        session.close()