from sqlalchemy import text
from festiuto import cnx

def get_user_by_email(email):
    try:
        result = cnx.execute(text(f"select idU, nomU, prenomU, mailU, idR from UTILISATEUR where mailU = '{email}';"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise

def get_mdp_by_email(email):
    try:
        result = cnx.execute(text(f"select mdpU from UTILISATEUR where mailU = '{email}';"))
        result = result.first()
        return result[0]
    except:
        print("erreur de l'id")
        raise

def hasher_mdp(mdp):
    import hashlib
    return hashlib.sha256(mdp.encode()).hexdigest()

def get_all_concerts():
    try:
        result = cnx.execute(text("select * from CONCERT natural join GROUPE natural join STYLEMUSICAL order by dateDebC;"))
        data = []
        for row in result: data.append(row)
        return data
    except:
        raise

def get_groupe_by_idC(idC):
    try:
        result = cnx.execute(text(f"select * from CONCERT natural join GROUPE natural join STYLEMUSICAL where idC = {idC};"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise

def get_roles():
    try:
        result = cnx.execute(text("select * from ROLEUTI;"))
        data = []
        for row in result: data.append(row)
        return data
    except:
        raise

def get_last_idU():
    try:
        result = cnx.execute(text("select max(idU) from UTILISATEUR;"))
        result = result.first()
        return result[0]
    except:
        raise

def insert_user(mail,prenom,nom,mdp):
    try:
        idU = get_last_idU() + 1
        mailU = mail
        prenomU = prenom
        nomU = nom
        mdpU = mdp
        idR = 3
        cnx.execute(text("INSERT INTO UTILISATEUR (idU, nomU, prenomU, mailU, mdpU, idR) VALUES (" + str(idU) + ", '" + str(nomU) + "', '" + str(prenomU) + "', '" + str(mailU) + "', '" + str(mdpU) + "', " + str(idR) + ");"))
        cnx.commit()
        print(f"Utilisateur {idU} ajouté")
    except:
        print("Erreur lors de l'ajout de l'utilisateur")
        raise