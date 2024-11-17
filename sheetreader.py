import requests
import os
import csv
import json


json_form = os.path.join("data", "questionnaire_form.json")


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
        
        #grab latest repsonse
        if filtered_data:
            latest_response = max(filtered_data, key=lambda x: x.get("Timestamp"))
            save_json([latest_response], "individual_form.json")

# csv_json()
# parse_json("brurh@gmail.com")