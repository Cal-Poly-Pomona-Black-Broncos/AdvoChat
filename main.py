import advochat, sheetreader, app
import pandas as pd
import json
from hospitalRecommender import recommendedHospitals, hospitalDF, patientData  # Import the hospital recommender function

def main():
    # Remove previous data 
    SheetReader.remove_prev()

    print("Form link: https://forms.gle/9CLpDPF8fzLHeUQB6 \n")

    # Get the email address after form completion
    email = input("Once form is completed, provide email: ")

    print("\n")

    # Process the input using the SheetReader module
    SheetReader.main(email)

    json_file_path = r'data\individual_form.json'
    # Load patient data from the JSON file
    with open(json_file_path, 'r') as file:
        user_input = json.load(file)

    # Get the user's preferences (from the JSON or processed form)
    patient = user_input[0]

    # Get the maximum distance for the hospital recommendation
    max_distance = input("\nThe hospital should be within a _ mile radius:  ")
    max_distance = int(max_distance)

    # Get the recommended hospitals based on the patient's data
    recommended_hospitals = recommendedHospitals(patient, hospitalDF, max_distance)

    # If hospitals are recommended, append the results to a CSV or use as needed
    if recommended_hospitals is not None:
        print(f"\nRecommended Hospital(s) within {max_distance} miles: {recommended_hospitals}")
        SheetReader.append_predicted_class(str(recommended_hospitals))
    else:
        print("No recommended hospitals found.")

    print("------------Begin-Chat--------------")

    # Start the chat process 
    AdvoChat.chat()

# Module imports for the functions
AdvoChat = advochat
SheetReader = sheetreader

# Start the main execution
main()
