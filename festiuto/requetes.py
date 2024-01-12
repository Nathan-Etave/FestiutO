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

def insert_billet(idT,idU,dateDebB, dateFinB):
    try:
        session = Session()
        billet = BILLET(idB=get_last_idB() + 1, idT=idT, idU=idU, idF=1, dateDebB=dateDebB, dateFinB=dateFinB)
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
        concerts = session.query(CONCERT, GROUPE, STYLE_MUSICAL).select_from(CONCERT).join(GROUPE).join(STYLE_MUSICAL).filter(GROUPE.nomG.like("%" + search + "%")).order_by(CONCERT.dateDebC).all()
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
        style_musical = 3
        print("\n")
        # print(get_groupe_with_idG(idG).STYLEMUSICAL)
        print("\n")
        session = Session()
        groupe = session.query(GROUPE).filter(GROUPE.idS == style_musical).filter(GROUPE.idG != idG).all() #.limit(2) pour limiter les résultats
        return groupe
    except:
        raise
    finally:
        session.close()