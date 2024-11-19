import requests
import os
import csv
import json


json_form = os.path.join("data", "questionnaire_form.json")

indiv_form = os.path.join("data", "individual_form.json")

#helper method to save json with data into ./data and with name
#input data -> raw json data
#input name -> name of json file being saved
def save_json(data, name):
    # Ensure the 'data' directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save the JSON data into the specified file
    with open(os.path.join("data", name), "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


#download form into json
def csv_json():
    response = requests.get("https://docs.google.com/spreadsheets/d/1iR1nPIQgCYTJ_I6YagPxfqCH3i5X6bOXtbyn9jIeYdc/gviz/tq?tqx=out:csv")
    if response.status_code == 200:
        csv_content = response.content.decode("utf-8")
        csv_reader = csv.DictReader(csv_content.splitlines())
        json_response = [row for row in csv_reader]

        save_json(json_response, "questionnaire_form.json")
    else:
        print(f"failed with code: {response.status_code} lol")


#parse json to only response with email
def parse_json(email):
    with open(json_form, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        filtered_data = [row for row in data if row.get("Email", "").strip().lower() == email.strip().lower()]
        
        #grab latest response
        if filtered_data:
            latest_response = max(filtered_data, key=lambda x: x.get("Timestamp"))
            save_json([latest_response], "individual_form.json")

def combine_with_individual_form(json_data: dict):
    try:
        # Load existing JSON data from the predefined file
        with open(indiv_form, 'r') as file:
            file_json = json.load(file)

        # Check if the loaded data is a list or dictionary
        if isinstance(file_json, list):
            # Append the new data if the file contains a list
            file_json.append(json_data)
        elif isinstance(file_json, dict):
            # Merge the dictionaries if the file contains a dictionary
            file_json = {**file_json, **json_data}
        else:
            raise ValueError("Unexpected JSON structure in the file.")

        # Write the updated JSON back to the predefined file
        with open(indiv_form, 'w') as output_file:
            json.dump(file_json, output_file, indent=2)

        print("Data merged and updated in 'individual_form.json' successfully.")

    except FileNotFoundError:
        print(f"Error: File '{indiv_form}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")

def append_predicted_class(predicted_class: str):
    
    try:
        # Load the JSON data from the predefined file
        with open(indiv_form, 'r') as file:
            data = json.load(file)

        # Ensure the file contains a list and has at least one dictionary entry
        if isinstance(data, list) and len(data) > 0:
            # Append the "Chosen Hospital" field to the last dictionary entry
            data[-1]["Chosen Hospital"] = predicted_class

            # Write the updated JSON data back to the file
            with open(indiv_form, 'w') as output_file:
                json.dump(data, output_file, indent=2)

            print("Predicted class added successfully to the JSON file.")

        else:
            print("Error: JSON data is not a list or is empty.")

    except FileNotFoundError:
        print(f"Error: File '{indiv_form}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def remove_prev():
    os.remove(indiv_form)

#startup funciton
def main(email):
    csv_json()
    parse_json(email)


# json_data = {
#     "name": "Alice",
#     "age": 25,
#     "hobbies": ["reading", "hiking"]
# }

# combine_with_individual_form(json_data)


# csv_json()
# parse_json("fun@gmail.com")

# append_predicted_class('Fungual Houses')