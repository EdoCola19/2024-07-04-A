from database.DB_connect import DBConnect
from model.Arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.`datetime`) as year
FROM sighting s
order by YEAR(s.`datetime`)desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
FROM sighting s 
WHERE s.shape != "unknown" and s.shape != ""
order by s.shape"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(shape, year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
FROM sighting s 
WHERE s.shape = %s and YEAR(s.`datetime` ) = %s"""
            cursor.execute(query,(shape,year))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(shape, year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
FROM (SELECT *
FROM sighting s 
WHERE s.shape = %s and YEAR(s.`datetime` ) = %s) as t, (SELECT s.id as id2, s.`datetime`as time2, s.city as city2, s.state as state2, s.country as country2, s.shape as shape2, s.duration as duration2, s.duration_hm as duration_hm2,s.comments as comments2, s.date_posted as date2, s.latitude as lat2, s.longitude as long2
FROM sighting s 
WHERE s.shape = %s and YEAR(s.`datetime` ) = %s) as t1
WHERE t.`datetime` <t1.time2 and t.state = t1.state2"""
            cursor.execute(query, (shape, year, shape, year))

            for row in cursor:
                s1 = Sighting(
                    id=row["id"],
                    datetime=row["datetime"],
                    city=row["city"],
                    state=row["state"],
                    country=row["country"],
                    shape=row["shape"],
                    duration=row["duration"],
                    duration_hm=row["duration_hm"],
                    comments=row["comments"],
                    date_posted=row["date_posted"],
                    latitude=row["latitude"],
                    longitude=row["longitude"]
                )
                s2 = Sighting(
                    id=row["id2"],
                    datetime=row["time2"],
                    city=row["city2"],
                    state=row["state2"],
                    country=row["country2"],
                    shape=row["shape2"],
                    duration=row["duration2"],
                    duration_hm=row["duration_hm2"],
                    comments=row["comments2"],
                    date_posted=row["date2"],
                    latitude=row["lat2"],
                    longitude=row["long2"]
                )
                result.append(Arco(Sighting1=s1, Sighting2=s2))
            cursor.close()
            cnx.close()
        return result