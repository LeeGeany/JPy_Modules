import mysql.connector
from mysql.connector import errorcode

class CMySQL:
    def __init__(self, _ip : str,  _port : str, _user : str, _password : str, _database=None):
        self.config = {
            'user': _user,
            'password': _password,
            'host': _ip,
            'port': _port,
            'raise_on_warnings': True,
            'autocommit': False,
            'charset': 'utf8'
        }

        self.cnx = None
        self.cursor = None


    def mysql_open(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor(buffered=True) # fatch 전까지 결과를 메모리에 저장

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print(err)


    def mysql_close(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except mysql.connector.Error as err:
            print(err)

    def mysql_query(self, _query):
        try:
            self.cursor.execute(_query)
            self.cnx.commit()
        except mysql.connector.Error as err:
            self.cnx.rollback()
            print(err)

    def mysql_many_query(self, _query, _params):
        try:
            self.cursor.execute(_query, _params)
            self.cnx.commit()
        except mysql.connector.Error as err:
            self.cnx.rollback()
            print(err)


if __name__ == '__main__':
    mysql_ = CMySQL(_ip="192.168.122.123", _port="3306", _user="User", _password="root", _database="testdb")
    mysql_.mysql_open()

    mysql_.mysql_close()
