from dataclasses import dataclass
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import sys
import os
import re

CALORIE_GOAL_LIMIT = 1800 # kcal
PROTEIN_GOAL = 180 # grams
FAT_GOAL = 40 # grams
CARBOHYDRATE_GOAL = 180 # grams

today = []


@dataclass
class Food:
    Name: str
    Calories: int
    Proteins: int
    Fats: int
    Carbohydrates: int

def filecreate(FilePath, Name, Calories, Proteins, Fats, Carbohydrates):
    # open the file in the write mode
    f = open(FilePath, 'a')

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    #writer.writerow(row)
    writer.writerow([str(Name), str(Calories), str(Proteins), str(Fats), str(Carbohydrates)])

    # close the file
    f.close()


if __name__ == '__main__':
    now = datetime.now()
    print('CurrentDateTime:', now)

    current_date = now.date()
    print('Date:', current_date)
    print("Year:", now.year)
    print("Month:", now.month)
    print("Day =", now.day)

    file_name_day = ''.join('Nutrition Record-')
    file_name_day += str(now.year)
    file_name_day += "-"
    file_name_day += str(now.month)
    file_name_day += "-"
    file_name_day += str(now.day)
    file_name_day += ".csv"
    print("Filename:  ", file_name_day)

    date_time_cell = ''
    date_time_cell += str(now.day)
    date_time_cell += "-"
    date_time_cell += str(now.month)
    date_time_cell += "-"
    date_time_cell += str(now.year)
    #

    done = False

    while not done:
        print("""
               (1) Add a New Food Item
               (2) Track Progress
               (3) List Data Files
               (4) Generate Report
               (q) Quit
               """)

        choice = input("Choose an option: ")



        if choice == "1":
            print("Adding food item")
            Name = input("Name: ")
            Calories = int(float(input("Calories: ")))
            Proteins = int(float(input("Proteins: ")))
            Fats = int(float(input("Fats: ")))
            Carbohydrates = int(float(input("Carbohydrates: ")))
            food = Food(Name, Calories, Proteins, Fats, Carbohydrates)
            today.append(food)

            #Add row to CSV file for Export
            filecreate(file_name_day, Name, Calories, Proteins, Fats, Carbohydrates)

            print("New food item added")
        elif choice == "2":
            Calories_sum = sum(food.Calories for food in today)
            Proteins_sum = sum(food.Proteins for food in today)
            Fats_sum = sum(food.Fats for food in today)
            Carbohydrates_sum = sum(food.Carbohydrates for food in today)

            # Prompt the User to choose a file
            #filename = input("Enter the name of the CSV file you want to use")

            fig, axs = plt.subplots(2, 2)
            axs[0, 0].pie([Proteins_sum, Fats_sum, Carbohydrates_sum], labels=["Proteins", "Fats", "Carbohydrates"], autopct="%1.1f%%")
            axs[0, 0].set_title("Macronutrient Allocation")
            axs[0, 1].bar([0, 1, 2], [Proteins_sum, Fats_sum, Carbohydrates_sum], width=0.4)
            axs[0, 1].bar([0.5, 1.5, 2.5], [PROTEIN_GOAL, FAT_GOAL, CARBOHYDRATE_GOAL], width=0.4)
            axs[0, 1].set_ylabel("Consumption")
            axs[0, 1].set_xlabel("Macronutrients")
            axs[0, 1].set_title("Macronutrient Goal Progress")
            axs[1, 0].pie([Calories_sum, CALORIE_GOAL_LIMIT - Calories_sum], labels=["Calories Consumed", "Calories Remaining"], autopct="%1.1f%%")
            axs[1, 0].set_title("Calorie Consumption Tracker")
            axs[1, 1].plot(list(range(len(today))), np.cumsum([food.Calories for food in today]), label="Calories Consumed")
            axs[1, 1].plot(list(range(len(today))), [CALORIE_GOAL_LIMIT] * len(today), label="Calorie Goal")
            axs[1, 1].legend()
            axs[1, 1].set_title("Cumulative Calorie Progress")

            fig.tight_layout()
            plt.show()

        elif choice == "3":
            directory = "."
            # for static path input path as directory value
            for currentRoot, dirList, fileList in os.walk(directory):
                for nextFile in fileList:
                    fullPath = os.path.join(currentRoot, nextFile)
                    absPath = os.path.abspath(fullPath)
                    if os.path.isfile(absPath):
                        if re.search('.csv', absPath):
                            print("Displaying all CSV files in Current Directory:  ", absPath)
                            # we have a CSV file

                            # process it
                            file = open(absPath, "r")

                            # read data into a list
                            data = list(csv.reader(file, delimiter=","))
                            file.close()
                            print(data)
        elif choice == "4":
            print("Generating Report")
            if os.path.isfile(file_name_day):
                if re.search('.csv', file_name_day):
                    print("We have a CSV file:  ", file_name_day)
                    # we have a CSV file

                    # process it
                    file = open(file_name_day, "r")

                    # read data into a list
                    data = list(csv.reader(file, delimiter=","))
                    file.close()
                    #print(data)
            report_file_name_day = ''.join('Report-')
            report_file_name_day += str(now.year)
            report_file_name_day += "-"
            report_file_name_day += str(now.month)
            report_file_name_day += "-"
            report_file_name_day += str(now.day)
            report_file_name_day += ".csv"
            #Prompt the User to choose a file
            filename = input("Enter the name of the CSV file you want to use")
            #Open the CSV file and read its contents with
                open(filename, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
            #Print Headers for each column
            print("{:<30} {:<15} {:<15} {:<15} {:<15}".format('Name', 'Calories', 'Proteins', 'Fats', 'Carbohydrates'))
            #Loop through data and print to the screen
            for row in data:
                print("{:<30} {:<15} {:<15} {:<15} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))



        elif choice == "q":
            done = True

        else :
            print("Invalid Response")