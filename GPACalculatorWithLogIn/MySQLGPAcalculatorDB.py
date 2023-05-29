import mysql.connector


def getTable(tableName):
    """ Reads table as a 2 dimensional array. """
    connection = mysql.connector.connect(host='localhost',
                                         database='GPAcalculator',
                                         user='root',
                                         password='Macacocemrab0!')

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {tableName}")
    return cursor.fetchall()


def createQuery(query):
    # Check if appendToDatabase function can do it all without issues. If so, delete this method.
    connection = mysql.connector.connect(host='localhost',
                                         database='GPAcalculator',
                                         user='root',
                                         password='Macacocemrab0!')
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        print(cursor.rowcount, "Row impacted.")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))


class GPACalculatorDatabase:
    connection = None

    def __init__(self):

        self.connection = mysql.connector.connect(host='localhost',
                                                  database='GPAcalculator',
                                                  user='root',
                                                  password='Macacocemrab0!')

    def getClassTable(self, accountID):
        """ Reads table as a 2 dimensional array. """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM classeswithaccounts where accountID = {accountID}")
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
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO classeswithaccounts (accountID, classID, className, classGrade, classCredit) "
                           f"VALUES ({accountID}, {classID}, '{className}', {classGrade}, {classCredit}) ")
            self.connection.commit()
            print(cursor.rowcount, "modification completed successfully")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to perform action".format(error))

    def classesCount(self, accountID):
        return len(self.getClassTable(accountID))

    def rowCount(self, tableName):
        # counts the number of rows in a database
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        rows = cursor.fetchall()
        return len(rows)

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

                    cursor = self.connection.cursor()
                    query = "UPDATE classeswithaccounts " \
                            f"SET {columName} = '{newValue}' WHERE classID = {classNumber} and accountID = {accountID}"
                    cursor.execute(query)
                    self.connection.commit()

    def selectClassForDetails(self, accountID, ID):
        determiner = False
        for elements in self.getClassTable(accountID):
            if elements[1] == ID:
                print(f"1) Name: {elements[2]}\n"
                      f"2) Grade: {elements[3]}\n"
                      f"3) Credit: {elements[4]}\n")
                determiner = True
                return int(input("What would you like to change? ('0' to return to menu) "))


class LogIn:
    connection = None

    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                  database='GPAcalculator',
                                                  user='root',
                                                  password='Macacocemrab0!')

    def appendUser(self, Username, Password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO accountslogin (accountUserName, accountPassword) "
                           f"VALUES ('{Username}', '{Password}') ")
            self.connection.commit()
            print(cursor.rowcount, "modification completed successfully")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to perform action".format(error))

    def getUsersTable(self):
        """ Reads table as a 2 dimensional array. """
        return getTable("accountslogin")

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

    def validatePassword(self, accountID, password):
        accounts = self.getUsersTable()

        if accounts[accountID - 1][2] == password:
            return True
        else:
            return False
