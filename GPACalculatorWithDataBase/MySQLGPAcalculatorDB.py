import mysql.connector


class GPACalculatorDatabase:
    connection = None

    def __init__(self):

        self.connection = mysql.connector.connect(host='localhost',
                                                  database='GPAcalculator',
                                                  user='root',
                                                  password='Macacocemrab0!')

    def selectClassFromMenu(self):
        classes = self.getTable("classes")
        for element in classes:
            print(f'{element[0]}) {element[1]}')
        print("\n")
        return int(input("Chose class number: "))

    def appendToDatabase(self, className, classGrade, classCredit):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO classes (className, classGrade, classCredit) "
                           f"VALUES ('{className}', {classGrade}, {classCredit}) ")
            self.connection.commit()
            print(cursor.rowcount, "modification completed successfully")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to perform action".format(error))

    def createQuery(self, query):
        # Check if appendToDatabase function can do it all without issues. If so, delete this method.
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            print(cursor.rowcount, "Row impacted.")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

    def rowCount(self, tableName):
        # counts the number of rows in a database
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        rows = cursor.fetchall()
        return len(rows)

    def getTable(self, tableName):
        """ Reads table as a 2 dimensional array. """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        return cursor.fetchall()

    def changeClassName(self):
        """Struggling to format query correctly. Works fine when ran at sql console,
        but not when executing through python"""
        classNumber = self.selectClassFromMenu()
        columNumberFromMenu = self.selectClassForDetails(classNumber)

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
        query = "UPDATE classes " \
                f"SET {columName} = '{newValue}' WHERE classID = {classNumber}"
        cursor.execute(query)
        self.connection.commit()

    def selectClassForDetails(self, ID):
        determiner = False
        for elements in self.getTable("classes"):
            if elements[0] == ID:
                print(f"1) Name: {elements[1]}\n"
                      f"2) Grade: {elements[2]}\n"
                      f"3) Credit: {elements[3]}\n")
                determiner = True
                return int(input("What would you like to change? "))
