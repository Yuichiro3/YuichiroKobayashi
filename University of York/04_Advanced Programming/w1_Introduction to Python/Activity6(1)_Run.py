# -*- coding: utf-8 -*-
"""Activity6_Modules_and_Classes_Run.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zL25AtW_fjbJ3hznX8Sdbsq_htHXuxgt

# Modules and Classes
## Exercise one
Write a module that provides the following conversions:

Length - feet (') and inches ('') to meters (m)
Mass - pounds (lbs) to kilograms (kg)
Temperature - Kelvin (K) to Celsius (oC)
Time - hours (h) and minutes(m) to seconds (s)
Each calculation should be within its own function, with the module, so you will write eight functions altogether. Write a program that provides a suitable menu system for your conversion functions. This program should import the module and access the functions (functions should not be defined in the same file as the user interface). You will need to carefully consider how the user enters information and the upper and lower bounds (valid range) for each type of conversion. For example, the temperature cannot go below 0o Kelvin.
"""

from Activity6_Converters import feet_inches_to_meters, pounds_to_kilograms, kelvin_to_celsius, hours_minutes_to_seconds

# Choose the one function and input data from users

# Function: Display menu
def display_menu():
    print("1. Feet and Inches to Meters")
    print("2. Pounds to Kilograms")
    print("3. Kelvin to Celsius")
    print("4. Hours and Minutes to Seconds")
    print("5. Exit")

# Get user input
while True:
    display_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        feet = float(input("Enter the number of feet: "))
        inches = float(input("Enter the number of inches: "))
        result = feet_inches_to_meters(feet, inches)

    elif choice == '2':
        pounds = float(input("Enter the weight in pounds: "))
        result = pounds_to_kilograms(pounds)

    elif choice == '3':
        kelvin = float(input("Enter the temperature in Kelvin: "))
        result = kelvin_to_celsius(kelvin)

    elif choice == '4':
        hours = float(input("Enter the number of hours: "))
        minutes = float(input("Enter the number of minutes: "))
        result = hours_minutes_to_seconds(hours, minutes)

    elif choice == '5':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.")
        continue

    print("Result:", result)







"""# EOF"""