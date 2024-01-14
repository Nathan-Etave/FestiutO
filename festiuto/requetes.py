from sqlalchemy import func
from sqlalchemy.orm import joinedload
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
    try:
        session = Session()
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL) \
            .options(joinedload(CONCERT.lieu), joinedload(CONCERT.groupe), \
                     joinedload(CONCERT.festival), joinedload(CONCERT.reservation_concert_collection), \
                     joinedload(GROUPE.stylemusical), joinedload(GROUPE.utilisateur_collection),
                     joinedload(GROUPE.reseausocial_collection), joinedload(GROUPE.concert_collection), \
                     joinedload(GROUPE.video_collection), joinedload(GROUPE.photo_collection),
                     joinedload(GROUPE.artiste_collection), joinedload(GROUPE.loger_collection),
                     joinedload(GROUPE.activiteannexe_collection), joinedload(STYLE_MUSICAL.groupe_collection)) \
                                   .select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).filter(GROUPE.nomG.like("%" + search + "%")).order_by(CONCERT.dateDebC).all()
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
        print(total)
        return total
    except:
        raise
    finally:
        session.close()

def get_groupes():
    try:
        session = Session()
        groupes = session.query(GROUPE).all()
        print(groupes)
        return groupes
    except:
        raise
    finally:
        session.close()

def get_groupes_with_search(search):
    try:
        session = Session()
        groupes = session.query(GROUPE).filter(GROUPE.nomG.like("%" + search + "%")).all()
        print(groupes)
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
        artistes = session.query(ARTISTE).filter(ARTISTE.nomA.like("%" + search + "%")).all()
        return artistes
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

def get_hebergements():
    try:
        session = Session()
        hebergements = session.query(HEBERGEMENT).all()
        return hebergements
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

def insert_artiste(nomA,prenomA,idG):
    try:
        session = Session()
        artiste = ARTISTE(idA=get_last_idA() + 1, nomA=nomA, prenomA=prenomA, idP="", idG=idG)
        session.add(artiste)
        session.commit()
    except:
        raise
    finally:
        session.close()

def insert_concert(idG,idL,dateDebC,dateFinC,dureeMontageC,dureeDemontageC,estGratuit):
    try:
        session = Session()
        concert = CONCERT(idC=get_last_idC() + 1, idG=idG, idL=idL, dateDebC=dateDebC, dateFinC=dateFinC, dureeMontageC=dureeMontageC, dureeDemontageC=dureeDemontageC, estGratuit=estGratuit)
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