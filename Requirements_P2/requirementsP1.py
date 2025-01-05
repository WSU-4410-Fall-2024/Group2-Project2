import json
import os


# File name for the JSON file
FILE_NAME = 'requirementsP1.json'

def load_requirements():
    try:
        with open("requirementsP1.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle empty or non-existent file
        return []  # or {} if you're expecting a dictionary

# Save JSON data to file
def save_requirements(data):
    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=4)

# Add a new requirement
def add_requirement(data):
    print("Enter the following details for the new requirement:")
    date = input("Enter date (e.g., 9/27/24): ")
    phase = input("Enter Phase - Inception, Elicitation, Elaboration, Negotiation, Specification, Validation, Management: ")
    specific_requirement = input("Enter Specific Requirement [CORE/NER]: ")
    authored_by = input("Authored by: ")
    title = input("Requirement title: ")
    policy = input("Policy - Use Case - Business Justification: ")
    stakeholders = input("Stakeholders/Spearhead: ")
    approved_by = input("Approved By - and date: ")
    author_user = input("Enter the name of the authoring user: ")
    reference_number = input("Enter requirement reference number: ")

    # Generate an entry ID (random unique key)
    import random
    entry_id = str(random.randint(1000000000000000000, 9999999999999999999))

    # Add the new requirement to the data dictionary
    data[entry_id] = [
        date, phase, specific_requirement, authored_by, title, policy, stakeholders, approved_by
    ]

    print(f"\nRequirement added successfully with Entry ID: {entry_id}")
    print(f"The last reference number is: {reference_number}")
    return data

# Search for a requirement
def search_requirement(data):
    print("\nSelect the field to search for the keyword:")
    print("1. Requirement Title")
    print("2. Policy - Use Case - Business Justification")
    field_choice = int(input("Enter the number corresponding to your choice: "))
    keyword = input("Enter a keyword to search for: ")

    fields = ["Requirement Title", "Policy - Use Case - Business Justification"]
    field_index = field_choice - 1

    print("\nSearch Results:")
    found = False
    for entry_id, details in data.items():
        if keyword.lower() in details[field_index + 4].lower():  # Search in title or policy
            print(f"Requirement Number: {details[8] if len(details) > 8 else 'N/A'}")
            print(f"Entry ID: {entry_id}")
            print(f"Details: {details}\n")
            found = True

    if not found:
        print("No matching requirements found.")

# Main menu function
def main():
    data = load_requirements()
    last_reference_number = max(
        (int(details[8]) for details in data.values() if len(details) > 8), default=0
    )

    while True:
        print("\nChoose an option:")
        print("1. Add a new requirement")
        print("2. Search for a requirement")
        print("3. Exit")
        choice = input("Enter the number corresponding to your choice: ")

        if choice == '1':
            data = add_requirement(data)
            last_reference_number += 1
            save_requirements(data)
        elif choice == '2':
            search_requirement(data)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
