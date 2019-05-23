import mysql.connector 
from contextlib import closing


class MyMySql():

    def __init__(self, host, user, password, database) -> None:
        self._host = host
        self._user = user
        self._password = password
        self._database = database

    def fetch(self, query):
        mydb = mysql.connector.connect(
                host = self._host,
                user = self._user,
                passwd = self._password,
                database = self._database
                )

        with closing( mydb.cursor() ) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result


        mydb.close()




