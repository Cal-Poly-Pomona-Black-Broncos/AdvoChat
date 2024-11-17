import advochat, sheetreader, PredictionModel
import json
AdvoChat = advochat
SheetReader = sheetreader
PredModel = PredictionModel
print("form link: https://forms.gle/9CLpDPF8fzLHeUQB6 \n")

email = input("once form is co mpleted, provide email: ")

print("\n")

SheetReader.csv_json()
SheetReader.parse_json(email)

json_file_path = r'data\individual_form.json'
user_input = PredModel.load_user_input(json_file_path)


csv_output_path = r'data\user_input_output.csv'
PredModel.json_to_csv(user_input, csv_output_path, PredModel.expected_columns)


predicted_class = PredModel.predict_hospital(PredModel.rf, PredModel.x_clean, user_input[0], PredModel.encoders)
print(f"Prediction for the user input: {predicted_class}")

# with open(r"data\individual_form.json", "r") as file:
#     individual_form = json.load(file)

# SheetReader.combine_with_individual_form(individual_form)

#PredicitionModel.withJson()

#rediciton_json = 
#SheetReader.append_prediction(prediction_json)

print("------------Begin-Chat--------------")

AdvoChat.chat()
