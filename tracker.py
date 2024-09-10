#!/usr/bin/env python3
import csv
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

LOG_FILE = 'income_log.csv'
HEADERS = ['type', 'amount', 'date', 'notes']

def init_file():
    """Start the CSV file if it doesn't exist"""
    try:
        with open(LOG_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
    except FileExistsError:
        pass

def add_income():
    """Add a new income entry"""
    while True:
        income_type = input("Cash or Deposit (c/d): ").strip().lower()
        if income_type in ['c', 'd']:
            break
        print("Invalid input. Please enter 'c' for Cash or 'd' for Deposit.")
    
    while True:
        try:
            amount = float(input("Amount of money? "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    
    notes = input("Any notes? ").strip()
    
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([income_type, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), notes])

def display_total():
    """Display totals"""
    total_cash = 0
    total_deposit = 0

    try:
        with open(LOG_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['type'] == 'c':
                    total_cash += float(row['amount'])
                elif row['type'] == 'd':
                    total_deposit += float(row['amount'])
    except FileNotFoundError:
        print("No data found. Start making money!")
        return

    print(Style.BRIGHT + Fore.BLUE + f"Total Cash: ${total_cash:.2f}")
    print(Style.BRIGHT + Fore.YELLOW + f"Total Direct Deposit: ${total_deposit:.2f}")
    print(Style.BRIGHT + Fore.GREEN + f"Subtotal: ${total_cash + total_deposit:.2f}")

def display_all_logs():
    """Display all income logs"""
    try:
        with open(LOG_FILE, 'r') as file:
            reader = csv.DictReader(file)
            print(Style.BRIGHT + "All income entries:")
            for row in reader:
                date_obj = datetime.fromisoformat(row['date'])
                formatted_date = date_obj.strftime('%Y-%m-%d')
                print(Style.BRIGHT + f"Type: {row['type']} - Amount: ${float(row['amount']):.2f} - Date: {formatted_date} - Notes: {row['notes']}")
    except FileNotFoundError:
        print(Style.BRIGHT + "No data found. Please start logging some income.")

def main():
    """Main function to run the income tracker"""
    init_file()
    print(Fore.GREEN + Style.BRIGHT + "Welcome to Your Personal Income Tracker")
    while True:
        print("\nOptions:")
        print(Style.BRIGHT + Fore.RED + "1. Add income")
        print(Style.BRIGHT + Fore.RED + "2. Show total income")
        print(Style.BRIGHT + Fore.RED + "3. Display previous logs")
        print(Style.BRIGHT + Fore.RED + "4. Exit")
        choice = input(Style.BRIGHT + Fore.YELLOW + "Pick 1-4: ")
        if choice == '1':
            add_income()
        elif choice == '2':
            display_total()
        elif choice == '3':
            display_all_logs()
        elif choice == '4':
            print(Style.BRIGHT + Fore.GREEN + "Exiting.")
            break
        else:
            print(Fore.BLUE + "Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
