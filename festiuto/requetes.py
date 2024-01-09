from sqlalchemy import text
from festiuto import cnx

def test():
    try:
        result = cnx.execute(text("select * from FESTIVAL;"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise

def get_all_concerts():
    try:
        result = cnx.execute(text("select * from CONCERT natural join GROUPE natural join STYLEMUSICAL order by idC;"))
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