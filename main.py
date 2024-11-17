import advochat, sheetreader#, PredictionModel
import json
AdvoChat = advochat
SheetReader = sheetreader

print("form link: https://forms.gle/9CLpDPF8fzLHeUQB6 \n")

email = input("once form is co mpleted, provide email: ")

print("\n")

SheetReader.csv_json()
SheetReader.parse_json(email)

# with open(r"data\individual_form.json", "r") as file:
#     individual_form = json.load(file)

# SheetReader.combine_with_individual_form(individual_form)

#PredicitionModel.withJson()

#rediciton_json = 
#SheetReader.append_prediction(prediction_json)

print("------------Begin-Chat--------------")

AdvoChat.chat()
