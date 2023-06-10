import mysql.connector
import pyodbc

server = 'tcp:test2273.database.windows.net,1433'
database = 'GPA'
username = 'BrenoFlag'
password = 'Macacocemrab0!'
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnx = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
cursor = cnx.cursor()


def connectionString():
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    return 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'


def getTable(tableName):
    """ Reads table as a 2 dimensional array. """
    cursor.execute(f"SELECT * FROM {tableName}")
    return cursor.fetchall()


def createQuery(query):
    # Check if appendToDatabase function can do it all without issues. If so, delete this method.
    try:
        cursor.execute(query)
        print(cursor.rowcount, "Row impacted.")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


def rowCount(tableName):
    # counts the number of rows in a database
    cursor.execute(f"SELECT * FROM {tableName}")
    rows = cursor.fetchall()
    return len(rows)


class GPACalculatorDatabase:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pyodbc.connect(connectionString())
        self.cursor = self.connection.cursor()

    @staticmethod
    def getClassTable(accountID):
        """ Reads table as a 2 dimensional array. """
        cursor.execute(f"SELECT * FROM classes where accountID = {accountID}")
        return cursor.fetchall()

    def selectClassFromMenu(self, accountID):
        classes = self.getClassTable(accountID)
        for element in classes:
            print(f'{element[1]}) {element[2]}')
        print("\n")
        return int(input("Chose class number ('0' return to menu): "))

    def appendClass(self, accountID, className, classGrade, classCredit):

        classID = ((self.classesCount(accountID)) + 1)
        try:
            self.cursor.execute("INSERT INTO classes (accountID, classID, className, classGrade, classCredit) "
                           f"VALUES ({accountID}, {classID}, '{className}', {classGrade}, {classCredit}) ")
            self.connection.commit()
            print(self.cursor.rowcount, "modification completed successfully")

        except mysql.connector.Error as error:
            print("Failed to perform action".format(error))

    def classesCount(self, accountID):
        return len(self.getClassTable(accountID))

    def changeClass(self, accountID):
        """Struggling to format query correctly. Works fine when ran at sql console,
        but not when executing through python"""
        classAmount = self.classesCount(accountID)

        if classAmount == 0:
            print("Must add classes first!")
        else:
            classNumber = self.selectClassFromMenu(accountID)
            if classNumber > 0:

                columNumberFromMenu = self.selectClassForDetails(accountID, classNumber)
                if columNumberFromMenu > 0:

                    while True:
                        if columNumberFromMenu == 1:
                            columName = "className"
                            newValue = input("Enter new class name: ")
                            break
                        elif columNumberFromMenu == 2:
                            columName = "classGrade"
                            while True:
                                try:
                                    newValue = int(input("Enter new grade: "))
                                    break
                                except:
                                    print("Must be a number!")
                            break
                        elif columNumberFromMenu == 3:
                            columName = "classCredit"
                            while True:
                                try:
                                    newValue = int(input("Enter new credit amount: "))
                                    break
                                except:
                                    print("Must be a number!")
                            break
                        else:
                            "invalid choice"

                    self.cursor = self.connection.cursor()
                    query = "UPDATE classes " \
                            f"SET {columName} = '{newValue}' WHERE classID = {classNumber} and accountID = {accountID}"
                    self.cursor.execute(query)
                    self.connection.commit()

    def selectClassForDetails(self, accountID, ID):
        for elements in self.getClassTable(accountID):
            if elements[1] == ID:
                print(f"1) Name: {elements[2]}\n"
                      f"2) Grade: {elements[3]}\n"
                      f"3) Credit: {elements[4]}\n")
                return int(input("What would you like to change? ('0' to return to menu) "))


class LogIn:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pyodbc.connect(connectionString())
        self.cursor = self.connection.cursor()

    def appendUser(self, Username, Password):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("INSERT INTO accounts (username, password) "
                                f"VALUES ('{Username}', '{Password}') ")
            self.connection.commit()
            print(self.cursor.rowcount, "modification completed successfully")

        except mysql.connector.Error as error:
            print("Failed to perform action".format(error))

    @staticmethod
    def getUsersTable():
        """ Reads table as a 2 dimensional array. """
        return getTable("accounts")

    def getUserNames(self):
        accounts = self.getUsersTable()

        usernames = []
        for elements in accounts:
            usernames.append(elements[1])
        return usernames

    def validateUserName(self, UserName):
        accounts = self.getUsersTable()

        accountID = 0

        for elements in accounts:
            if elements[1] == UserName:
                accountID = elements[0]
                break

        if accountID == 0:
            return False
        else:
            return accountID

    def validatePassword(self, accountID, passwordInput):
        accounts = self.getUsersTable()

        if accounts[accountID - 1][2] == passwordInput:
            return True
        else:
            return False
