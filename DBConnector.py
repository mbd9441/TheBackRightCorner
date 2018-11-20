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

    def querydictlist(self, query, columns):
        queryresult = self.makequery(query)
        queryarray=[]
        for i in range(0,len(queryresult)):
            row = queryresult[i]
            rowdict={}
            for j in range(0,len(row)):
                rowdict[columns[j]]=str(row[j])
            queryarray.append(rowdict)
        return queryarray

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()