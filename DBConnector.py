import psycopg2

class dbconnector:
    connection=None
    
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='p32003g' user='p32003g' host='reddwarf.cs.rit.edu' password='Pheicothaequ7aeghohG'")
            print("Connection Successful")
        except:
            print("Connection Error")
    
    def __enter__(self):
        return self

    def makequery(self, query):
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()