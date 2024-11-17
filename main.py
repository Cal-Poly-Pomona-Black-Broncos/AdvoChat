import advochat, sheetreader

AdvoChat = advochat
SheetReader = sheetreader

print("form link: https://forms.gle/9CLpDPF8fzLHeUQB6 \n")

email = input("once form is completed, provide email: ")

print("\n")

SheetReader.csv_json()
SheetReader.parse_json(email)


print("------------Begin-Chat--------------")

AdvoChat.chat()
