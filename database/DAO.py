from database.DB_connect import DBConnect
from model.Arco import Arco


class DAO():
    def __init__(self):
        pass

#DROPDOWN
    @staticmethod
    def getAllGenre():
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT name 
                               FROM genre """
            cursor.execute(query)
            res = []
            for row in cursor:
                res.append(row["name"])
            return res
        except Exception as e:
            print(f"Errore getAllGenre: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

#GRAFO
    @staticmethod
    def getAllNodes(genre):  #si selezionano tutti i nodi del grafo
                            #parametro di selezione
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT a.Name
                       FROM artist a, album al, track t, genre g
                        WHERE a.ArtistId=al.ArtistId 
                        and al.AlbumId=t.AlbumId 
                        and t.GenreId=g.GenreId
                        AND g.Name= %s """
            cursor.execute(query, (genre, ))
            res = []
            for row in cursor:    #cursor contiene i risultati della query
                                  #ogni row è un dizionario es. {"teamCode": "BOS"}
                res.append(row["Name"])  #seleziono i valori della chiave
                                             #row["teamCode"] prende il valore "BOS" e lo aggiunge alla lista res
            return res       #alla fine res è una lista di stringhe: ["BOS", "NYA", "CLE", ...]
        except Exception as e:
            print(f"Errore getAllNodes: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllEdges1(genre, idMapNames):  #archi da A a B
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT
       a1.Name AS nomeA,
       a2.Name AS nomeB,
       p1.popolarita + p2.popolarita AS peso
FROM artist a1,
     artist a2,
     invoice i1,
     invoice i2,
     invoiceline il1,
     invoiceline il2,
     track t1,
     track t2,
     album al1,
     album al2,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p1,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p2

WHERE a1.ArtistId<a2.ArtistId
AND p1.ArtistId=a1.ArtistId
AND p2.ArtistId=a2.ArtistId

AND il1.InvoiceId=i1.InvoiceId
AND il2.InvoiceId=i2.InvoiceId
AND i1.CustomerId=i2.CustomerId

AND il1.TrackId=t1.TrackId
AND il2.TrackId=t2.TrackId

AND t1.AlbumId=al1.AlbumId
AND t2.AlbumId=al2.AlbumId

AND al1.ArtistId=a1.ArtistId
AND al2.ArtistId=a2.ArtistId

AND t1.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
AND t2.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)

AND p1.popolarita>p2.popolarita;"""

            cursor.execute(query, (genre, genre, genre, genre))
            res = []
            for row in cursor:
                if row["nomeA"] in idMapNames and row["nomeB"] in idMapNames: #verifichiamo se i team sono nel grafo
                                                                              #stessi nomi del select
                    res.append(Arco(idMapNames[row["nomeA"]], idMapNames[row["nomeB"]], row["peso"]))
                                                    #idMapTeams[row["team1"]] prende il valore dal dizionario corrispondente alla chiave row["team1"].
                                                     #serve ad aggiungere un oggetto Arco alla lista res.
                                                     #Ogni Arco rappresenta un arco del grafo con i due team e il peso.
                                                     # Alla fine res è una lista di tutti gli archi trovati dalla query.
            return res
        except Exception as e:
            print(f"Errore getAllEdges: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllEdges2(genre, idMapNames): #archi da B a A
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT
       a1.Name AS nomeA,
       a2.Name AS nomeB,
       p1.popolarita + p2.popolarita AS peso
FROM artist a1,
     artist a2,
     invoice i1,
     invoice i2,
     invoiceline il1,
     invoiceline il2,
     track t1,
     track t2,
     album al1,
     album al2,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p1,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p2

WHERE a1.ArtistId<a2.ArtistId
AND p1.ArtistId=a1.ArtistId
AND p2.ArtistId=a2.ArtistId

AND il1.InvoiceId=i1.InvoiceId
AND il2.InvoiceId=i2.InvoiceId
AND i1.CustomerId=i2.CustomerId

AND il1.TrackId=t1.TrackId
AND il2.TrackId=t2.TrackId

AND t1.AlbumId=al1.AlbumId
AND t2.AlbumId=al2.AlbumId

AND al1.ArtistId=a1.ArtistId
AND al2.ArtistId=a2.ArtistId

AND t1.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
AND t2.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)

AND p1.popolarita<p2.popolarita;"""


            cursor.execute(query, (genre, genre, genre, genre))
            res = []
            for row in cursor:
                if row["nomeA"] in idMapNames and row["nomeB"] in idMapNames:  # verifichiamo se i team sono nel grafo
                    res.append(Arco(idMapNames[row["nomeA"]], idMapNames[row["nomeB"]], row["peso"]))
                    # idMapTeams[row["team1"]] prende il valore dal dizionario corrispondente alla chiave row["team1"].
                    # serve ad aggiungere un oggetto Arco alla lista res.
                    # Ogni Arco rappresenta un arco del grafo con i due team e il peso.
                    # Alla fine res è una lista di tutti gli archi trovati dalla query.
            return res
        except Exception as e:
            print(f"Errore getAllEdges: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllEdges3(genre, idMapNames):  #Archi da A a B e da B a A
        cnx = DBConnect.get_connection()
        try:
            cursor = cnx.cursor(dictionary=True, buffered=True)
            query = """SELECT DISTINCT
       a1.Name AS nomeA,
       a2.Name AS nomeB,
       p1.popolarita + p2.popolarita AS peso
FROM artist a1,
     artist a2,
     invoice i1,
     invoice i2,
     invoiceline il1,
     invoiceline il2,
     track t1,
     track t2,
     album al1,
     album al2,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p1,

     (SELECT al.ArtistId,
             COUNT(*) AS popolarita
      FROM invoiceline il,
           track t,
           album al
      WHERE il.TrackId=t.TrackId
      AND t.AlbumId=al.AlbumId
      AND t.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
      GROUP BY al.ArtistId) p2

WHERE a1.ArtistId<a2.ArtistId
AND p1.ArtistId=a1.ArtistId
AND p2.ArtistId=a2.ArtistId

AND il1.InvoiceId=i1.InvoiceId
AND il2.InvoiceId=i2.InvoiceId
AND i1.CustomerId=i2.CustomerId

AND il1.TrackId=t1.TrackId
AND il2.TrackId=t2.TrackId

AND t1.AlbumId=al1.AlbumId
AND t2.AlbumId=al2.AlbumId

AND al1.ArtistId=a1.ArtistId
AND al2.ArtistId=a2.ArtistId

AND t1.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)
AND t2.GenreId=(SELECT GenreId FROM genre WHERE Name=%s)

AND p1.popolarita=p2.popolarita;"""

            cursor.execute(query, (genre, genre, genre, genre ))
            res = []
            for row in cursor:
                if row["nomeA"] in idMapNames and row["nomeB"] in idMapNames:  # verifichiamo se i team sono nel grafo
                    res.append(Arco(idMapNames[row["nomeA"]], idMapNames[row["nomeB"]], row["peso"]))
                    # idMapTeams[row["team1"]] prende il valore dal dizionario corrispondente alla chiave row["team1"].
                    # serve ad aggiungere un oggetto Arco alla lista res.
                    # Ogni Arco rappresenta un arco del grafo con i due team e il peso.
                    # Alla fine res è una lista di tutti gli archi trovati dalla query.
            return res
        except Exception as e:
            print(f"Errore getAllEdges: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()



