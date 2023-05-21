from GPAcalculator import GPACalculator
from MySQLGPAcalculatorDB import GPACalculatorDatabase

calculator = GPACalculator()
connection = GPACalculatorDatabase()

while True:

    calculator.getMenu()
    decider = input()

    if decider == '1':
        calculator.addClass()
    elif decider == '2':
        calculator.getGPA()
    elif decider == '3':
        connection.changeClassName()
    elif decider == '4':
        break
