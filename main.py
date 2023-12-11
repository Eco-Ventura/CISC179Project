#Imports the required libraries for working with files, date, and CSV.
import csv
import os
from datetime import datetime

#Main direction of all the clients.
client_directory = "clients"

def list_client_files(directory):
    """
    List all CSV files in the specified directory and return a mapping of file number to file path.
    """
    # Get a list of all files in the directory that end with '.csv'
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Create a dictionary where each file is assigned a unique number as a key
    # The enumeration starts from 1 for user-friendliness
    file_mapping = {str(i+1): file for i, file in enumerate(files)}

    return file_mapping

def extract_client_details_from_filename(filename):
    """
    Extracts the client ID and name from the file name.
    Assumes the file name format is using the client ID.'ClientName_ClientDate.csv'.
    """
    # Remove the file extension (.csv)
    name_without_extension = filename.split('.csv')[0]

    # Split the remaining string by the underscore
    # This will give you ['ClientID', 'ClientName']
    parts = name_without_extension.split('_')

    # Extract the client ID and name
    client_id = parts[0]
    client_name = parts[1]

    return client_id, client_name

def display_files_and_get_choice(file_mapping):
    """
    Display the files to the user and get their choice.
    """
    global client_directory
    # Print each file and its corresponding number
    for number, file in file_mapping.items():
        print(f"{number}: {file}")

    # Ask the user to choose a file by entering its number
    choice = input("Enter the number of the client file you want to work with: ")

    # Return the file path associated with the user's choice, along with the name and ID of the client for use in other functions
    selected_file = file_path = os.path.join(client_directory, file_mapping.get(choice, None))
    client_name, client_id = extract_client_details_from_filename(file_mapping.get(choice, None))

    return [selected_file, client_name, client_id]


def create_client_file(client_id, directory="clients"):
    """Creates a new CSV file for a client to store medication records."""
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Define the file path
    file_path = os.path.join(directory, f"{client_id}.csv")

    # Check if the file already exists to avoid overwriting
    if os.path.exists(file_path):
        print(f"File for client {client_id} already exists.")
        return

    # Define the headers for the CSV file
    headers = ["Medication", "Daily Dose", "Quantity", "Last Count Date"]

    # Create a new CSV file with the headers
    with open(file_path, mode='w', newline='') as file:
        # Declares the instance that will be used to write the headers
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

    print(f"New file created for client {client_id}: {file_path}")

    return file_path


def generate_unique_id(name):
    """
    Generates a unique ID for every client based on name and date+time
    """

    # Calls upon the now() function of datetime to give us the current date/time, then format it for use.
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Returns a combination of the client's name and the date + time the file was created as a way to give each client a unique ID
    return f"{name}_{timestamp}"


def load_medications(file_path):
    """
    Load medication data from a CSV file.
    If the file doesn't exist, returns an empty list.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print('Filepath not found.')
        return []

    # Open the file and read its contents
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)  # Convert the read data into a list and return it

def add_medication(medications):
    """
    Add a new medication entry to the list.
    Prompt the user for medication details and append this data to the list.
    """
    # Prompt the user for medication details
    medication_name = input("Enter medication name: ")
    daily_dose = input("Enter daily dose (In number of pills/capsules taken): ")
    quantity = input("Enter quantity: ")
    last_count_date = input("Enter last count date (YYYY-MM-DD): ")

    # Append the new medication data to the medications list
    medications.append({
        "Medication": medication_name,
        "Daily Dose": daily_dose,
        "Quantity": quantity,
        "Last Count Date": last_count_date
    })
def list_medications(medications):
    """
    Print all current medications in the list.
    """
    print("\nCurrent Medications:")
    # Loop through each medication and print its details
    for index, medication in enumerate(medications, start=1):
        print(
            f"{index}: {medication['Medication']}, Daily Dose: {medication['Daily Dose']}, Quantity: {medication['Quantity']}, Last Count Date: {medication['Last Count Date']}")

def save_medications(file_path, medications):
    """
    Save medication data to a CSV file.
    Writes the list of medications to the file with appropriate headers.
    """
    # Open the file in write mode
    with open(file_path, mode='w', newline='') as file:
        # Create a CSV DictWriter object with the appropriate field names
        writer = csv.DictWriter(file, fieldnames=medications[0].keys())
        writer.writeheader()  # Write the header row
        writer.writerows(medications)  # Write the medication data
def select_medication_to_edit(medications):
    """Allow the user to select a medication to edit."""
    list_medications(medications)
    choice = int(input("Enter the number of the medication to edit: ")) - 1
    # Checks to make sure that a valid input was provided before attempting to return the medication
    if 0 <= choice < len(medications):
        return choice
    else:
        print("Invalid selection.")
        return None


def update_medication(medications, index):
    """
    Update the selected medication's details.
    """
    # Prompt the user for new details of the medication
    medication_name = input("Enter new medication name (or press enter to keep current): ")
    daily_dose = input("Enter new daily dose (or press enter to keep current): ")
    quantity = input("Enter new quantity (or press enter to keep current): ")
    last_count_date = input("Enter new last count date (YYYY-MM-DD) (or press enter to keep current): ")
    print(f'New medication information: Medication Name: {medication_name} Daily Dose: {daily_dose} Quantity: {quantity} Last Count Date: {last_count_date}')

    # Update the medication details only if the user entered new information
    if medication_name:
        medications[index]['Medication'] = medication_name
    if daily_dose:
        medications[index]['Daily Dose'] = daily_dose
    if quantity:
        medications[index]['Quantity'] = quantity
    if last_count_date:
        medications[index]['Last Count Date'] = last_count_date

def remove_medication(medications, index):
    """Provides a way to remove a medication from a client's med log"""
    #First verifies that the user does want to remove the medication from the med log.
    print(f"Are you sure you want to remove {medications[index]} ?")
    print("1) Yes\n2) No")
    choice = input("Enter your choice: ")

    if choice == 1:
        # Deletes the row associated with the medication.
        del medications[index]
        print("Medication removed!")
    else:
        return

def parse_date(date_str):
    """Converts a date string to a datetime.date object."""
    # Gives the program a workable object to be able to compare today's date and the date the medication was last counted.
    return datetime.strptime(date_str, "%Y-%m-%d").date()
def days_until_refill_needed(last_count_date, daily_dose, quantity):
    """
    Calculates the number of days until a refill is needed for a medication using today's date.
    Returns the number of days of medication a client has left.
    """
    #Takes the current date and uses it to determine how long it has been since the medication has been counted.
    today = datetime.now().date()
    days_since_last_count = (today - last_count_date).days

    # Calculate the total remaining doses
    total_remaining_doses = quantity - (daily_dose * days_since_last_count)

    if total_remaining_doses <= 0:
        return 0  # Indicates that the medication has already run out. Prevents divide by 0 error.

    # Calculate how many days the remaining doses will last
    days_until_refill = total_remaining_doses / daily_dose
    return days_until_refill

def check_refill_needs_for_all(directory):
    """
    Check all client files in a directory to find medications that need a refill then prints out the dictionary list.

    """
    #Empty dict to hold all of the information.
    refill_needs = {}
    #Go through all the files in the directory, finding the ones that end with csv. If they do, run the individual client
    # Through check_refill_needs.
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            client_name, client_id = extract_client_details_from_filename(filename)
            file_path = os.path.join(directory, filename)
            meds_needing_refill = check_refill_needs(file_path)

            #Saves the returned list to the dictionary under the client's name.
            if meds_needing_refill:
                refill_needs[client_name] = meds_needing_refill

    print(refill_needs)

def check_refill_needs(file_path):
    """
    Check if any medications in a CSV file need a refill within the next week, returning a list of all the medications
    that do to be used by the check all function.
    """
    #Empty list to store the medications that will run out within the next 7 days.
    meds_needing_refill = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # For loop to run through each row of the csv file.
        for row in reader:
            last_count_date = parse_date(row['Last Count Date'])
            daily_dose = int(row['Daily Dose'])
            quantity = int(row['Quantity'])
            # Takes all the needed information then sends it to days_until_refill_needed.
            if days_until_refill_needed(last_count_date, daily_dose, quantity) <= 7:
                meds_needing_refill.append(row['Medication'])

    return meds_needing_refill
def medication_menu(file_path, name):
    """
    Allows the user to add, show, and save medications to a client's file
    """
    # Load existing medication data
    medications = load_medications(file_path)

    while True:
        # Display the menu options
        print(f"\n{name}'s Medication Menu")
        print("1. Add a new medication")
        print("2. Print all current medications")
        print("3. Edit a medication.")
        print("4. Remove medication.")
        print("5. Save and return to main menu")
        print('6. Return to main menu without saving.')
        # Get the user's choice
        choice = input("Enter your choice: ")

        # Handle the user's choice
        if choice == '1':
            add_medication(medications)
        elif choice == '2':
            list_medications(medications)
        elif choice == '3':

            update_medication(medications, select_medication_to_edit(medications))
        elif choice == '4':

            remove_medication(medications, select_medication_to_edit(medications))
        elif choice == '5':
            save_medications(file_path, medications)
            print("Data saved. Returning to Main Menu")
            break  # Exit the loop to end the program
        elif choice == '6':
            print('Returning to Main Menu without saving..')
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


def main_menu():
    """
    Function for displaying the main menu that is used to navigate the program.
    """
    global client_directory
    # while True keeps the menu running until the user selects the option to exit the program.
    while True:
        print("\nMedication Tracking System Main Menu")
        print("1. Create a new client file")
        print("2. Add/Remove/Modify a medication record in a client file")
        print("3. View a client's medication records")
        print("4. Calculate refills needed for all clients")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            client_name = input("What is the client's name?")
            #Asks for the client name then passed it to the generate unique ID function.
            client_id = generate_unique_id(client_name)
            # Passes the ID to the create client file method to be used as a file name.
            new_client_filepath = create_client_file(client_id)
            # Asks the user if they would like to start adding medications for the newly created client.
            print(f"\nWould you like to start adding medications for {client_name}?")
            print("1. Yes")
            print("2. No")
            add_medications_choice = input("Enter your choice: ")
            if add_medications_choice == '1':
                # Uses the newly created filepath and name to send to the medication menu.
                medication_menu(new_client_filepath, client_name)
            else:
                pass
        elif choice == '2':
            print()
            client_choice = display_files_and_get_choice(list_client_files(client_directory))
            medication_menu(client_choice[0],client_choice[1])
        elif choice == '3':
            client_choice = display_files_and_get_choice(list_client_files(client_directory))
            list_medications(load_medications(client_choice[0]))
        elif choice == '4':
            check_refill_needs_for_all(client_directory)

        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == '__main__':

    main_menu()

