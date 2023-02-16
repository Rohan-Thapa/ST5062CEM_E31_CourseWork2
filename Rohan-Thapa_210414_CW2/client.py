# Project from Rohan Thapa (Student ID: 210414). Remember to run this code in project directory as it may give path error while accessing files
from tkinter import *
from tkinter import ttk, messagebox
import hashlib
import socket
import subprocess

host = '127.0.0.1'
port = 1234

key = 15
characters = [' ', ',', '.', '-', '(', ')', '!', '_', '>', '<', '/', '\\', '|', '+', '=', '[', ']', ':', ';', '`', '~', '"']

def send_info(data):
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        messagebox.showerror("Error", str(e))
    ClientSocket.send(str.encode(data))
    Response = ClientSocket.recv(2048)
    response = decrypt(Response.decode('utf-8'))
    if response == 'ACK':
        ClientSocket.close()
    elif response == 'Login Failed!':
        messagebox.showerror("Login Failed!", "Login Failed due to incorrect credientials.")
    elif response.startswith('Login Success!'):
        user_interface(response)
    elif response.startswith('User Already Exists!'):
        messagebox.showerror("User does exist", "The user which you want to create does exists already in the server.")
    elif response.startswith('User Added!'):
        login()
    elif response.startswith('Error Occured on Deposit!'):
        messagebox.showerror("Error!", "The amount was unable to be added due to data corruption!")
    elif response.startswith('Amount Added!'):
        user_interface(response)
    elif response.startswith('Error Occured on Withdraw!'):
        messagebox.showerror("Error", "Unable to locate the data where to reduce the amount!")
    elif response.startswith('Amount Reduced!'):
        user_interface(response)
    elif response.startswith('Receiver or Sender Not Found!'):
        messagebox.showerror("Error", "The account of receiver or sender was not found!")
    elif response.startswith('Unable to Transfer!'):
        messagebox.showerror("Error", "We were unable to transfer the amount!")
    elif response.startswith('The Amount was Transfered!'):
        user_interface(response)
    elif response.startswith('Data'):
        account_detials = eval(response.split('->')[1])
        with open("./files/accounts.txt", "w") as start_file:
            start_file.write("Account Holder Name | Account Number\n")
        with open("./files/accounts.txt", "a+") as account_information:
            for accounts in account_detials:
                account_information.write(f"{accounts[0]} | {accounts[1]}\n")
        subprocess.Popen(["notepad.exe", "./files/accounts.txt"])
    else:
        pass

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

def clear_all():
    for widget in root.winfo_children():
        widget.destroy()

def contact_us(event):
    address = "Buddhanagar, New Baneshwor, Kathmandu, Nepal"
    email = "contact-us@banking.com.np"
    phone = "+977-01-2355319/2355320/2355321"
    messagebox.showinfo("Contact Us!", f"Please do contact us at:\n\nAddress: {address}\nEmail: {email}\nPhone: {phone}")

def validation():
    global verification_code
    uname = username_value.get()
    password = password_value.get()
    if uname != "" and password != "":
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        ver = uname+password_hash
        verification_code = hashlib.sha256(ver.encode('utf-8')).hexdigest()
        sending_info = f"Login->{uname}->{password_hash}->{verification_code}"
        enc_data = encrypt(sending_info)
        send_info(enc_data)
    else:
        error_label.config(text="Input was not given.")
        messagebox.showerror("Incomplete input", "The input was incomplete and the required input was left empty.")
        
def user_register():
    #Register->username->account->dob->password
    name = username.get()
    pas = password.get()
    repas = repassword.get()
    acc = account.get()
    Dob = dob.get()
    detail_date = Dob.split('/')
    if pas != repas:
        messagebox.showerror("Error", "The Password and Re-typed password does not match!")
    elif name == "" and pas == "" and repas == "" and acc == "" and Dob == "":
        messagebox.showerror("Error", "The input was not filled properly! Please do fill it again.")
    elif not (detail_date[0].isdigit() and detail_date[1].isdigit() and detail_date[2].isdigit()):
        messagebox.showerror("Error", "The DOB was invalid!")
    elif (len(detail_date[0]) != 4) and ((len(detail_date[1]) != 2) or (len(detail_date[1]) != 1)) and ((len(detail_date[2]) != 2) or (len(detail_date[2]) != 1)):
        messagebox.showerror("Error", "The Date of Birth was not written in the asked format.")
    elif not ((0<int(detail_date[1])<=12) and (0<int(detail_date[2])<=31)):
        messagebox.showerror("Error", "There is the invalid value of month and day of the year.")
    elif not acc.isdigit():
        messagebox.showerror("Error", "The account number should be digit not a alpha-numeric value")
    else:
        hashed_password = hashlib.sha256(pas.encode('utf-8')).hexdigest()
        transfer_info = f"Register->{name}->{acc}->{Dob}->{hashed_password}"
        encrypted_info = encrypt(transfer_info)
        send_info(encrypted_info)

def amount_deposit():
    amount = deposit_amount.get()
    dd = amount.split('.')    # decimal_digits
    isintegers = False
    for i in dd:
        if i.isdigit():
            isintegers = True
        else:
            isintegers = False
            break
    if isintegers and (len(dd)==2 or len(dd)==1):        
        send_data = f"Deposit->{amount}->{verification_code}"
        encrypted = encrypt(send_data)
        send_info(encrypted)
    else:
        messagebox.showerror("Error", "The amount given for the deposit is not a numeric value.")

def amount_withdraw():
    amount = withdraw_amount.get()
    dd = amount.split('.')    # decimal_digits
    isinteger = False
    for i in dd:
        if i.isdigit():
            isinteger = True
        else:
            isinteger = False
            break
    if isinteger and (len(dd)==2 or len(dd)==1):
        if float(amount) <= balance:
            sending_data = f"Withdraw->{amount}->{verification_code}"
            encrypted_data = encrypt(sending_data)
            send_info(encrypted_data)
        else:
            messagebox.showerror("Error", "The withdraw amount is more than available balance!")
    else:
        messagebox.showerror("Error", "The amount given for the deposit must be a numeric value.")

def amount_transfer():
    account = holder_account.get()
    name = holder_name.get()
    amount = transfer_amount.get()
    dd = amount.split('.')   # decimal_digits
    isintegers = False
    for i in dd:
        if i.isdigit():
            isintegers = True
        else:
            isintegers = False
            break
    if account.isdigit() and isintegers and name != "" and (len(dd)==2 or len(dd)==1):
        if float(amount) <= balance:
            send_data = f"Transfer->{name}->{account}->{amount}->{verification_code}"
            encrypted_data = encrypt(send_data)
            send_info(encrypted_data)
        else:
            messagebox.showerror("Error", "The amount which you want to transfer exceeds your available balance!")
    else:
        messagebox.showerror("Error", "The input were invalid!")

def get_accounts(): send_info(encrypt("Get Data?"))

def update_content(selected_frame):
    detail_frame.grid_forget()
    deposit_frame.grid_forget()
    withdraw_frame.grid_forget()
    transfer_frame.grid_forget()
    if selected_frame == 'User Details':
        detail_frame.grid(row=2, column=0, columnspan=4, pady=20)
    elif selected_frame == 'Deposit':
        deposit_frame.grid(row=2, column=0, columnspan=4, pady=20)
    elif selected_frame == 'Withdraw':
        withdraw_frame.grid(row=2, column=0, columnspan=4, pady=20)
    elif selected_frame == 'Transfer':
        transfer_frame.grid(row=2, column=0, columnspan=4, pady=20)

def user_interface(user_info):
    clear_all()
    global detail_frame, deposit_frame, withdraw_frame, transfer_frame, deposit_amount, withdraw_amount, holder_account, holder_name, transfer_amount, balance
    user_data = eval(user_info.split(' as ')[1])
    Label(root, text=f"Welcome {user_data['name']}!", font=('Arial', 16), fg="green").grid(row=0, column=0, columnspan=4, padx=55, pady=10)

    Label(root, text="What to do?").grid(row=1, column=0, pady=10, padx=10)
    balance = user_data['balance']

    main_frame = ttk.Frame(root)
    main_frame.grid(row=1, column=1, columnspan=3, pady=10, padx=30)

    options = ['User Details', 'Deposit', 'Withdraw', 'Transfer']

    for option in options:
        ttk.Button(main_frame, text=option, command=lambda opt=option: update_content(opt)).pack(side='left', padx=5)
    
    detail_frame = ttk.Frame(root)
    Label(detail_frame, text=f"Personal Detials of {user_data['name']}", font=('Arial', 18)).grid(row=0, column=0, columnspan=3, pady=10)
    Label(detail_frame, text=f"Account Holder Name: {user_data['name']}", font=('Arial', 12)).grid(row=1, column=0, padx=15)
    Label(detail_frame, text=f"Account Number: {user_data['account']}", font=('Arial', 12)).grid(row=2, column=0, padx=15)
    Label(detail_frame, text=f"Balance: NRS. {user_data['balance']}", font=('Arial', 12)).grid(row=3, column=0, padx=15)
    Label(detail_frame, text=f"Date of Birth: {user_data['DOB']}", font=('Arial', 12)).grid(row=4, column=0, padx=15)

    deposit_frame = ttk.Frame(root)
    deposit_amount = StringVar()
    Label(deposit_frame, text="Deposit Amount", font=('Arial', 18)).grid(row=0, column=0, columnspan=3, pady=10)
    Label(deposit_frame, text=f"Account Holder Name: {user_data['name']}", font=('Arial', 12)).grid(row=1, column=0, padx=15, columnspan=3)
    Label(deposit_frame, text=f"Account Number: {user_data['account']}", font=('Arial', 12)).grid(row=2, column=0, padx=15, columnspan=3)
    Label(deposit_frame, text="Enter Amount (NRS)", font=('Arial', 12)).grid(row=3, column=0, padx=15)
    deposit = ttk.Entry(deposit_frame, width=20, textvariable=deposit_amount)
    deposit.grid(row=3, column=1, padx=10)
    ttk.Button(deposit_frame, text="Deposit", command=amount_deposit).grid(row=4, column=0, padx=20, columnspan=3, pady=5)

    withdraw_frame = ttk.Frame(root)
    withdraw_amount = StringVar()
    Label(withdraw_frame, text="Withdraw Amount", font=('Arial', 18)).grid(row=0, column=0, columnspan=3, pady=10)
    aa = Label(withdraw_frame, text=f"Username: {user_data['name']} / Acc. No. {user_data['account']}", font=('Arial', 12))
    aa.grid(row=1, column=0, columnspan=3)
    Label(withdraw_frame, text=f"Available Balance: NRS. {user_data['balance']}", font=('Arial', 12)).grid(row=2, column=0, columnspan=3, padx=15)
    Label(withdraw_frame, text="Enter Amount (NRS)", font=('Arial', 12)).grid(row=3, column=0, padx=15)
    withdraw = ttk.Entry(withdraw_frame, width=20, textvariable=withdraw_amount)
    withdraw.grid(row=3, column=1, padx=10)
    ttk.Button(withdraw_frame, text="Withdraw", command=amount_withdraw).grid(row=4, column=0, padx=20, pady=5, columnspan=3)

    transfer_frame = ttk.Frame(root)
    holder_name = StringVar()
    holder_account = StringVar()
    transfer_amount = StringVar()
    Label(transfer_frame, text="Transfer Amount", font=('Arial', 18)).grid(row=0, column=0, columnspan=3, pady=10)
    Label(transfer_frame, text="Account Holder Name:", font=('Arial', 12)).grid(row=1, column=0, padx=15)
    uname = ttk.Entry(transfer_frame, width=20, textvariable=holder_name)
    uname.grid(row=1, column=1, padx=10)
    Label(transfer_frame, text="Account Number:", font=('Arial', 12)).grid(row=2, column=0, padx=15)
    ac_nu = ttk.Entry(transfer_frame, width=20, textvariable=holder_account)
    ac_nu.grid(row=2, column=1, padx=10)
    Label(transfer_frame, text="Enter Amount:", font=('Arial', 12)).grid(row=3, column=0, padx=15)
    transfer = ttk.Entry(transfer_frame, width=20, textvariable=transfer_amount)
    transfer.grid(row=3, column=1, padx=10)
    ttk.Button(transfer_frame, text="Transfer", command=amount_transfer).grid(row=4, column=0, padx=20, pady=5)
    ttk.Button(transfer_frame, text="Account List", command=get_accounts).grid(row=4, column=1, padx=20, pady=5)

    update_content(options[0])

    buttons_frame = ttk.Frame(root)
    buttons_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    ttk.Button(buttons_frame, text="LogOut", command=first_time).pack(side=LEFT, padx=20)
    ttk.Button(buttons_frame, text="Quit", command=root.destroy).pack(side=LEFT, padx=20)

    message_text = "We, Our Banking Group is very delighted to serve you with our services\nHope to be with you for longer time."
    Label(root, text=message_text).grid(row=4, column=0, columnspan=3, padx=30, pady=15)

def login():
    clear_all()
    global username_value, password_value, error_label
    username_value = StringVar()
    password_value = StringVar()

    Label(root, text="LogIn to the System", font=("Times New Roman", 18, "bold")).grid(row=0, column=0, columnspan=3, padx=55, pady=15)
    Label(root, text="Username: *").grid(row=1, column=0, pady=10)
    username = ttk.Entry(root, width=25, textvariable=username_value)
    username.grid(row=1, column=1, pady=10)
    
    Label(root, text="Password: *").grid(row=2, column=0, pady=10)
    password = ttk.Entry(root, show='*', width=25, textvariable=password_value)
    password.grid(row=2, column=1, pady=10)
    
    def toggle_password_visibility():
        if password.cget('show') == '*':
            password.config(show='')
        else:
            password.config(show='*')

    visibility_checkbox = ttk.Checkbutton(root, text="Show password", command=toggle_password_visibility)
    visibility_checkbox.grid(row=2, column=2, padx=10, pady=10)
    error_label = Label(root, text="", fg="#CC0000")
    error_label.grid(row=3, column=1)
    ttk.Button(root, text="Go Back!", command=first_time).grid(row=4, column=0, padx=15, pady=5)
    ttk.Button(root, text="Login", command=validation).grid(row=4, column=1, pady=5)
    ttk.Button(root, text="Quit", command=root.destroy).grid(row=4, column=2, pady=5)
    text1 = '''Note: (*) is the required credentials.\n
    By logging in here you have agreed to our terms and conditions. Here, the credentials 
    are removed when starting the program or re-running it for the security reason.\n\n
    Please do consider to contact us if you have any questions or queries.'''
    Label(root, text=text1, fg="#505581").grid(row=5, column=0, padx=5, pady=10, columnspan=3) # here max length of the character is 95
    contact = Label(root, text="Contact us", fg="blue", cursor="hand2")
    contact.grid(row=6, column=1)
    contact.bind("<Button-1>", contact_us)
    Label(root, text="With Love and Care from Our Banking Group\nCopyright (c) - 2023").grid(row=7, column=0, padx=5, pady=10, columnspan=3)

def signup():
    clear_all()
    global username, password, repassword, account, dob
    username = StringVar()
    password = StringVar()
    repassword = StringVar()
    account = StringVar()
    dob = StringVar()

    Label(root, text="SignUp to the System", font=("Times New Roman", 16, "bold")).grid(row=0, column=0, columnspan=4, padx=55, pady=15)
    Label(root, text="Username:").grid(row=1, column=0, pady=10, padx=10)
    name = ttk.Entry(root, width=25, textvariable=username)
    name.grid(row=1, column=1, pady=10)

    Label(root, text="Account Number:").grid(row=2, column=0, pady=10, padx=10)
    acc = ttk.Entry(root, width=25, textvariable=account)
    acc.grid(row=2, column=1, pady=10)

    Label(root, text="Date of Birth:").grid(row=3, column=0, pady=10, padx=10)
    DOB = ttk.Entry(root, width=25, textvariable=dob)
    DOB.grid(row=3, column=1, pady=10)

    Label(root, text="Set Password:").grid(row=4, column=0, pady=10, padx=10)
    pas = ttk.Entry(root, width=25, show='*', textvariable=password)
    pas.grid(row=4, column=1, pady=10)

    def toggle_password_visibility():
        if pas.cget('show') == '*':
            pas.config(show='')
        else:
            pas.config(show='*')

    visibility_checkbox = ttk.Checkbutton(root, text="Show password", command=toggle_password_visibility)
    visibility_checkbox.grid(row=4, column=2, padx=10, pady=10)

    Label(root, text="Re-type Password:").grid(row=5, column=0, pady=10, padx=10)
    repas = ttk.Entry(root, width=25, show='*', textvariable=repassword)
    repas.grid(row=5, column=1, pady=10)

    def toggle_repassword_visibility():
        if repas.cget('show') == '*':
            repas.config(show='')
        else:
            repas.config(show='*')
    
    repass_visibility_checkbox = ttk.Checkbutton(root, text="Show repassword", command=toggle_repassword_visibility)
    repass_visibility_checkbox.grid(row=5, column=2, padx=15, pady=10)
    
    ttk.Button(root, text="Go Back!", command=first_time).grid(row=6, column=0, padx=15, pady=10)
    ttk.Button(root, text="SignUp", command=user_register).grid(row=6, column=1, pady=10)
    ttk.Button(root, text="Quit", command=root.destroy).grid(row=6, column=2, pady=10)

    notice = '''Notice: The Username is the full name of the user.\nAnd the Date of Birth should be written in the format of YYYY/MM/DD.\n
    With Love and Care from Our Banking Group\nCopyright (c) - 2023'''
    Label(root, text=notice).grid(row=7, column=0, columnspan=4, padx=5, pady=10)

def first_time():
    clear_all()
    Label(root, text="Welcome to the Banking System", font=('Arial', 18, 'bold')).grid(row=0, column=0, pady=5, padx=45, columnspan=2)
    Label(root, text="By Rohan Thapa").grid(row=1, column=0, padx=20, columnspan=2)
    
    ab = Label(root, text="Oops!\nThere seems you have been logged out!", font=("Roboto", 16, "italic"))
    ab.grid(row=2, column=0, padx=10, pady=50, columnspan=2)
    Label(root, text="Please do login again.", font=("Space Grotesk", 15)).grid(row=3, column=0, columnspan=2)
    
    ttk.Button(root, text="Login", command=login).grid(row=4, column=0, pady=45)
    ttk.Button(root, text="SignUp", command=signup).grid(row=4, column=1, padx=60, pady=45)
    Label(root, text="With Love and Care from Our Banking Group\nCopyright (c) - 2023").grid(row=5, column=0, padx=5, columnspan=3)

if __name__ == '__main__':
    root = Tk()
    
    root.title("Simple Banking System")
    root.geometry("500x400+580+200")
    root.resizable(0, 0)
    root.iconbitmap("./img/bank_icon.ico")

    first_time()

    root.mainloop()
