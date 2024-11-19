import advochat, sheetreader, PredictionModel, app
# import json


def main():
    SheetReader.remove_prev()

    print("form link: https://forms.gle/9CLpDPF8fzLHeUQB6 \n")

    email = input("once form is completed, provide email: ")

    print("\n")

    SheetReader.main(email)

    # SheetReader.csv_json()
    # SheetReader.parse_json(email)

    json_file_path = r'data\individual_form.json'
    user_input = PredModel.load_user_input(json_file_path)
    csv_output_path = r'data\user_input_output.csv'
    PredModel.json_to_csv(user_input, csv_output_path, PredModel.expected_columns)


    predicted_class = PredModel.predict_hospital(PredModel.rf, PredModel.x_clean, user_input[0], PredModel.encoders)

    SheetReader.append_predicted_class(str(predicted_class))
    

    print("------------Begin-Chat--------------")

    AdvoChat.chat()

AdvoChat = advochat
SheetReader = sheetreader
PredModel = PredictionModel

main()