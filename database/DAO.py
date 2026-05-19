from database.DB_connect import DBConnect


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct t.year
                from teams t 
                where t.`year`  >= 1980
                """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadre(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                    select  distinct t.teamCode as team
                    from teams t 
                    where t.`year` =%s
                    """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["team"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalarioSquadra(teamCode, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT SUM(s.salary) as totale
                FROM salaries s
                JOIN teams t ON s.teamID = t.ID
                WHERE t.teamCode = %s AND t.year = %s
                
                """
        cursor.execute(query, (teamCode, anno))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row["totale"] if row["totale"] is not None else 0

    @staticmethod
    def getNomeSquadre(teamcode, anno):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.name as name
                    from teams t 
                    where t.teamCode =%s and t.`year` =%s
                    LIMIT 1   """
        # LIMIT 1 --> restituisce al max una riga del database
        # la stessa squadra potrebbe avere nomi diversi in anni diversi nella tabella teams
        # FETCHONE recupera una sola riga dal risultato della query, restituendola come dizionario
        # {"name": "Los Angeles Dodgers"}
        cursor.execute(query, (teamcode,anno))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row["name"] if row is not None else teamcode