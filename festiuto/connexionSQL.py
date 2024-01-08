import sqlalchemy  
from .loginSQL import *  # importe les paramètres de connexion à la BD
import pymysql

pymysql.install_as_MySQLdb()
# sudo apt-get update 
# sudo apt-get install python3-sqlalchemy
# pip3 install mysql-connector-python
def ouvrir_connexion():
    """
    ouverture d'une connexion MySQL
    paramètres:
       user     (str) le login MySQL de l'utilsateur
       passwd   (str) le mot de passe MySQL de l'utilisateur
       host     (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL
       database (str) le nom de la base de données à utiliser
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé
    """
    try:
        login=getLogin()
        passwd=getPasswd()
        serveur=getServeur()
        bd=getBd()
        #creation de l'objet gérant les interactions avec le serveur de BD
        engine=sqlalchemy.create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)
        #creation de la connexion
        cnx = engine.connect()
    except Exception as err:
        print(err)
        raise err
    print("connexion réussie")
    return cnx
