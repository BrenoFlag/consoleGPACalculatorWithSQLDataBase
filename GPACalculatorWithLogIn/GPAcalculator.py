from MySQLGPAcalculatorDB import GPACalculatorDatabase
from MySQLGPAcalculatorDB import LogIn

classesConnection = GPACalculatorDatabase()
usersConnection = LogIn()


class GPACalculator:

    @staticmethod
    def getMenu():
        print("1) Create new class\n"
              "2) Get GPA\n"
              "3) See classes\n"
              "4) LogOut\n"
              "5) Quit\n")

    @staticmethod
    def getGPA(accountID):
        grades = []
        creditHours = []

        for elements in classesConnection.getClassTable(accountID):
            if elements[3] >= 90:
                grades.append(4)
            elif elements[3] >= 80:
                grades.append(3)
            elif elements[3] >= 70:
                grades.append(2)
            creditHours.append(elements[4])

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
    def addClass(accountID):  # updated to database
        classesConnection.appendClass(accountID,
                                      input("Enter the name of the class: "),
                                      int(input("Enter the Grade: ")),
                                      int(input("Enter the credit amount: ")))


class UserAccounts:
    @staticmethod
    def createAccount():
        decider = input("Would you like to create an account? (Y/N)")

        if decider.title() == 'Y':
            usersConnection.appendUser(input("Enter Username: "),
                                       input("Enter password: "))

    def validateLogIn(self):
        usernameValidation = usersConnection.validateUserName(input("Enter username: "))

        if not usernameValidation:
            self.createAccount()
            return [False, False]
        else:
            passwordValidation = usersConnection.validatePassword(usernameValidation, input("Enter password: "))
            if passwordValidation:
                return [True, usernameValidation]
            if not passwordValidation:
                print("Invalid password")
                return [False, False]