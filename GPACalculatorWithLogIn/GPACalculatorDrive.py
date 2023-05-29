from GPAcalculator import GPACalculator
from GPAcalculator import UserAccounts
from MySQLGPAcalculatorDB import GPACalculatorDatabase

calculator = GPACalculator()
connection = GPACalculatorDatabase()
logIn = UserAccounts()

decider = 0

while decider != '5':

    # program crashes after creating a new account.
    while True:
        loginValidation = logIn.validateLogIn()
        if loginValidation[0]:
            accountID = int(loginValidation[1])
            break

    while True:

        calculator.getMenu()
        decider = input()

        if decider == '1':
            calculator.addClass(accountID)
        elif decider == '2':
            calculator.getGPA(accountID)
        elif decider == '3':
            connection.changeClass(accountID)
        elif decider == '4':
            break
        elif decider == '5':
            break
