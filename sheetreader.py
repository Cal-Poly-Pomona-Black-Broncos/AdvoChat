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
    with open(os.path.join("data", name), "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)


#download form into json
def csv_json():
    response = requests.get("https://docs.google.com/spreadsheets/d/1Mt5Ep5oEZB3_Qj3sjaAaL5jmi6L3iqhcQx14keK6prI/gviz/tq?tqx=out:csv")
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
        filtered_data = [row for row in data if row.get("Email ", "").strip().lower() == email.strip().lower()]
        
        #grab latest response
        if filtered_data:
            latest_response = max(filtered_data, key=lambda x: x.get("Timestamp"))
            save_json([latest_response], "individual_form.json")

def append_prediction(data, other_json_path):

    #open both json
    with open(indiv_form, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    with open(other_json_path, 'r', encoding='utf-8') as other_file:
        other_json_data = json.load(other_file)

    #combine json    
    if isinstance(json_data, list) and isinstance(other_json_data, list):
        json_data.extend(other_json_data)
    elif isinstance(json_data, dict) and isinstance(other_json_data, dict):
        json_data.update(other_json_data)
    else:
        raise ValueError("Incompatible JSON structures: both must be lists or both must be dictionaries.")
    
    if isinstance(json_data, list):
        json_data.append(data)
    elif isinstance(json_data, dict):
        json_data.update(data)
    with open(indiv_form, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)



# csv_json()
# parse_json("Cmartin@cpp.edu")