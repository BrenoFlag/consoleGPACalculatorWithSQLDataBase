from MySQLGPAcalculatorDB import GPACalculatorDatabase

connection = GPACalculatorDatabase()


class GPACalculator:

    @staticmethod
    def getMenu():
        print("1) Create new class\n"
              "2) Get GPA\n"
              "3) See classes\n"
              "4) Quit\n")

    @staticmethod
    def getGPA():
        grades = []
        creditHours = []

        for elements in connection.getTable("classes"):
            if elements[2] >= 90:
                grades.append(4)
            elif elements[2] >= 80:
                grades.append(3)
            elif elements[2] >= 70:
                grades.append(2)
            creditHours.append(elements[3])

        i = 0
        totalGPACredit = 0
        totalCreditAmount = 0
        while i < len(grades):
            totalGPACredit += int(grades[i]) * int(creditHours[i])
            totalCreditAmount += int(creditHours[i])
            i += 1
        try:
            GPA = totalGPACredit / totalCreditAmount
            print(f"GPA: {GPA}")
        except ZeroDivisionError:
            print("GPA: Undefined")

    @staticmethod
    def addClass():  # updated to database
        connection.appendToDatabase(input("Enter the name of the class: "),
                                    int(input("Enter the Grade: ")),
                                    int(input("Enter the credit amount: ")))
