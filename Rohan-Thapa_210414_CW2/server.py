# Project from Rohan Thapa (Student ID: 210414). Remember to run this code in project directory as it may give path error while accessing files
import socket
import json
from datetime import datetime
import hashlib

def logs(data):
    current_time = str(datetime.now())
    with open('./files/logs.log', 'a+') as logs:
        logs.write(f"[{current_time}] {data}\n")

host = '127.0.0.1'
port = 1234

key = 15
characters = [' ', ',', '.', '-', '(', ')', '!', '_', '>', '<', '/', '\\', '|', '+', '=', '[', ']', ':', ';', '`', '~', '"']

def encrypt(message):
    encrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index + key) % 26 + ord('A')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index + key) % 26 + ord('a')
            character_new = chr(character_shift)
            encrypted += character_new
        elif character.isdigit():
            character_new = (int(character) + key) % 10
            encrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index + key) % len(characters)
            character_new = characters[character_shift]
            encrypted += character_new
        else:
            encrypted += character
    return encrypted

def decrypt(message):
    dencrypted = ""
    for character in message:
        if character.isupper():
            character_index = ord(character) - ord('A')
            character_shift = (character_index - key) % 26 + ord('A')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.islower():
            character_index = ord(character) - ord('a')
            character_shift = (character_index - key) % 26 + ord('a')
            character_new = chr(character_shift)
            dencrypted += character_new
        elif character.isdigit():
            character_new = (int(character) - key) % 10
            dencrypted += str(character_new)
        elif character in characters:
            character_index = characters.index(character)
            character_shift = (character_index - key) % len(characters)
            character_new = characters[character_shift]
            dencrypted += character_new
        else:
            dencrypted += character
    return dencrypted

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

while True:
    # Establish a connection with a client
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    logs(f"Connection from {str(addr)} was established!")

    # Receive data from the client
    data = decrypt(c.recv(2048).decode())

    # Process the received data and perform the necessary actions (e.g. account creation, login, money transfer)
    if data.startswith("Register"):
        # info = username->account->dob->password
        print("Registering the new user")
        logs(data)
        user_info = data.split('->')
        ver = user_info[1] + user_info[4]
        ver_code = hashlib.sha256(ver.encode('utf-8')).hexdigest()
        with open("./files/users.json", "r+") as content:
            user_data = {'name': user_info[1], 'account': user_info[2], 'DOB': user_info[3], 'password': user_info[4], 'balance': 0.0, 'ver': ver_code}
            data = json.load(content)['users']
            user_exist = False
            for user in data:
                if (user['name'] == user_info[1] and user['account'] == user_info[2]) or (user['account'] == user_info[2]):
                    user_exist = True
            if user_exist:
                print("User already exists which you are trying to create.")
                logs("The user does already exist!")
                c.send(encrypt("User Already Exists!").encode('utf-8'))
            else:
                data.append(user_data)
                with open("./files/users.json", "w") as file:
                    json_data = {'users': data}
                    json.dump(json_data, indent=4, fp=file)
                    print("User has been registered!")
                    logs("User was successfully added!")
                    c.send(encrypt("User Added!").encode('utf-8'))

    elif data.startswith("Login"):
        print("Trying to login to the system")
        logs(data)
        try:
            with open("./files/users.json", "r") as f:
                info = json.load(f)['users']
                obtained_data = data.split('->')
                # data = Login->account_holder->hashed_password->verification_code
                login_try = False
                for user in info:
                    if((user['name']==obtained_data[1]) and (user['password']==obtained_data[2])):
                        hey = f"Login successful as {user['name']}!"
                        logs(hey)
                        print(hey)
                        c.send(encrypt(f"Login Success! as {str(user)}").encode('utf-8'))
                        login_try = True
                        break
                if login_try == False:
                    logs("Invalid credentials were given!")
                    print("The login was unsuccessful!")
                    c.send(encrypt("Login Failed!").encode('utf-8'))
        except FileNotFoundError:
            logs("The user doesn't exist")
            c.send(encrypt("The user which you are trying to login is not registered!").encode('utf-8'))
    
    elif data.startswith("Transfer"):
        # Code for money transfer Data is Transfer->name->account->amount->verification_code
        print("Transfer of the money")
        logs(data)
        transfer_info = data.split('->')
        verification_code = transfer_info[-1]
        account_name = transfer_info[1]
        account_number = transfer_info[2]
        balance = float(transfer_info[3])
        data_updated = ""
        with open("./files/users.json", "r+") as content_value:
            datum = json.load(content_value)['users']
            receiver_found, sender_found = False, False
            for finding_users in datum:
                if finding_users['name'] == account_name and finding_users['account'] == account_number:
                    receiver_found = True
                elif finding_users['ver'] == verification_code:
                    sender_found = True
            if receiver_found and sender_found:
                balance_transfer = False
                for receiver_user in datum:
                    if receiver_user['name'] == account_name and receiver_user['account'] == account_number:
                        receiver_user['balance'] += balance
                        with open("./files/users.json", "w") as db:
                            json_info = {'users': datum}
                            json.dump(json_info, indent=4, fp=db)
                            balance_transfer = True
                            print(f"Amount {str(balance)} was added to the account of {account_name}!")
                            logs(f"Amount {str(balance)} was added to the account of {account_name}!")
                for another_user in datum:
                    if another_user['ver'] == verification_code and balance_transfer:
                        another_user['balance'] -= balance
                        with open("./files/users.json", "w") as files:
                            json_datum = {'users': datum}
                            json.dump(json_datum, indent=4, fp=files)
                            data_updated = another_user
                            print(f"Amount {str(balance)} was reduced to the account of {another_user['name']}!")
                            logs(f"Amount {str(balance)} was reduced to the account of {another_user['name']}!")
                if balance_transfer:
                    c.send(encrypt(f"The Amount was Transfered! as {data_updated}").encode('utf-8'))
                else:
                    print("Blance was unable to be transfered!")
                    logs("The Amount was unable to be transfered!")
                    c.send(encrypt("Unable to Transfer!").encode('utf-8'))
            else:
                print("The receiver or sender is not found!")
                logs("We didn't find the asked account of receiver or sender!")
                c.send(encrypt("Receiver or Sender Not Found!").encode('utf-8'))


    elif data.startswith("Deposit"):
        # Code for money depoist Data is Deposit->amount->verification_code
        print("Deposit of the money")
        logs(data)
        detial_info = data.split('->')
        ver_code = detial_info[-1]
        amount = float(detial_info[1])
        amount_added = False
        updated_data = ""
        with open("./files/users.json", "r+") as content:
            retriving_data = json.load(content)['users']
            for user_updated in retriving_data:
                if user_updated['ver'] == ver_code:
                    user_updated['balance'] += amount
                    with open("./files/users.json", "w") as file:
                        json_data = {'users': retriving_data}
                        json.dump(json_data, indent=4, fp=file)
                        amount_added = True
                        updated_data = user_updated
                        print(f"Amount {str(amount)} has been added to {user_updated['name']}!")
                        logs(f"Amount {str(amount)} has been added to {user_updated['name']}!")
        if amount_added:
            c.send(encrypt(f"Amount Added! as {updated_data}").encode('utf-8'))
        else:
            print("Couldn't add the amount!")
            logs("The amount was not added due to some error!")
            c.send(encrypt("Error Occured on Deposit!").encode('utf-8'))
    
    elif data.startswith("Withdraw"):
        # Code for money withdraw Data is Withdraw->amount->verification_code
        print("Withdraw of the money")
        logs(data)
        information = data.split('->')
        verification = information[-1]
        amount = float(information[1])
        amount_reduce = False
        changed_data = ""
        with open("./files/users.json", "r+") as contents:
            getting_data = json.load(contents)['users']
            for user_information in getting_data:
                if user_information['ver'] == verification:
                    user_information['balance'] -= amount
                    with open("./files/users.json", "w") as files:
                        json_datas = {'users': getting_data}
                        json.dump(json_datas, indent=4, fp=files)
                        amount_reduce = True
                        changed_data = user_information
                        print(f"Amount {str(amount)} has been added to {user_information['name']}!")
                        logs(f"Amount {str(amount)} has been added to {user_information['name']}!")
        if amount_reduce:
            c.send(encrypt(f"Amount Reduced! as {changed_data}").encode('utf-8'))
        else:
            print("Couldn't withdraw the amount!")
            logs("The amount was not withdrawn due to some error!")
            c.send(encrypt("Error Occured on Withdraw!").encode('utf-8'))
    
    elif data.startswith("Get Data?"):
        # Getting the User data
        print("Getting the User Data and Sending it.")
        logs("Obtaining the Data for Account List")
        with open("./files/users.json", "r+") as account_data:
            account_datum = json.load(account_data)['users']
            sending_data = []
            for account_info in account_datum:
                list_value = [account_info['name'], account_info['account']]
                sending_data.append(list_value)
        print("Sending the Data...")
        logs("The Account Name and Account Number were transfered!")
        c.send(encrypt(f"Data->{sending_data}").encode('utf-8'))

    # Send data back to the client
    c.send(encrypt("ACK").encode('utf-8'))

    # Close the connection with the client
    c.close()
