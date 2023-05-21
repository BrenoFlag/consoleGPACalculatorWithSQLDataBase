from MySQLGPAcalculatorDB import GPACalculatorDatabase

connection = GPACalculatorDatabase()


def seeClassesDB():
    classes = connection.getTable('classes')
    for element in classes:
        print(f'{element[0]}) {element[1]}')
    print("\n")


class GPACalculator:

    def seeClasses(self):
        """ Allows user to visualize existing data and modify it if desired """
        classes = self.ClassesContent.splitlines()

        # Prints a menu with all classes
        x = 1
        for i in classes:
            print(f"{x}) {i}")
            x += 1

        while True:
            try:
                determiner = int(input("Select a class number to see details/modify\n"
                                       "\'0\' to return to main menu\n"))
                if 0 <= determiner <= len(classes):
                    break
                else:
                    print("Enter a valid number!")
            except ValueError:
                print("Input must be a valid number!")

        if determiner != 0:
            grades = self.ClassGradeContent.splitlines()
            creditHour = self.CreditAmountContent.splitlines()

            print(f"1) Class name: {classes[determiner - 1]}\n"
                  f"2) Credit amount: {creditHour[determiner - 1]}\n"
                  f"3) Grade: {grades[determiner - 1]}\n")

            while True:
                # prints details of selected class.
                try:
                    selector = int(input("What would you like to modify?\n"
                                         "Select \'0\' to go back to main menu\n"))
                    if 0 <= selector < 4:
                        break
                    else:
                        print("Enter a valid number")
                except ValueError:
                    print("Enter a valid number!")

            if selector == 1:
                classes[determiner - 1] = input("Enter new class name: ")

                content = ""
                for elements in classes:
                    content += f"{elements}\n"

                self.toClasses.write_text(content)

            elif selector == 2:
                while True:
                    try:
                        creditHour[determiner - 1] = int(input("Enter new credit amount: "))
                        break
                    except ValueError:
                        print("Input must be a number")

                content = ""
                for elements in creditHour:
                    content += f"{elements}\n"

                self.toCreditAmount.write_text(content)

            elif selector == 3:
                while True:
                    try:
                        grades[determiner - 1] = int(input("Enter new grade: "))
                        break
                    except ValueError:
                        print("Input must be a number!")

                content = ""
                for elements in grades:
                    content += f"{elements}\n"

                self.toClassGrade.write_text(content)

    @staticmethod
    def getMenu():
        print("1) Create new class\n"
              "2) Get GPA\n"
              "3) See classes\n"
              "4) Quit\n")

    def getGPA(self):
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

    def addClass(self):  # updated to database
        connection.appendToDatabase(input("Enter the name of the class: "),
                                    int(input("Enter the Grade: ")),
                                    int(input("Enter the credit amount: ")))
