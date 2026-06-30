import json
import os

DATABASE_FILE = "users_list.json"

# currency rates dictionary
rates_dict = {"EGP": 1,
              "USD": 50, 
              "SAR": 14, 
              "SDG": 2
              }

def separator():
    print("-" * 100)

def initialize_database():
    #Create the database file if it doesn't exist
    if not os.path.exists(DATABASE_FILE): 
        with open (DATABASE_FILE,'w') as file :
            json.dump ([],file,indent=4)

def load_database():
    #Load users from the JSON database
    with open(DATABASE_FILE, "r") as file:
        return json.load(file)

def save_database(users):
    """Save users to the JSON database."""
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file, indent=4)


def login(db_list):
    """Handle user login."""
    trying_counter = 0
    
    while True :
        print("************ Welcome to login page ************")
        # asking for user password and id to login
        input_id = input("Please enter your id: ")
        # can't sign if the id is not a number
        if not input_id.isdigit():
            print("ID must be a number")
            continue
        input_password = input("Please enter your password: ")
        separator()
        
        # searching in the data for the user according to the id and password
        for user in db_list:
            if user["ID"] == int(input_id) and user["Password"] == input_password:
                print("Login successfully!")
                # Return the logged-in user if found
                return user  
        else:
            print("wrong id or password")
            separator()

            # the counter increase in every wrong submission
            trying_counter += 1
            
            # if the user tried more than 3 times we assume that he don't have an account
            if trying_counter > 3:
                print("Are you sure you have an account?, if not you can register now!")

            back_to_main = input("1. Try again\n2. Back to previous list\nYour option: ")
            separator()
            if back_to_main == "1":
                continue
            elif back_to_main == "2":
                return None
            else:
                print("Choose a correct option!")
                continue        
        
def register(db_list):
    """Register a new user."""
    while True:

        print("************ Welcome to sign up page ************")
    
        # asking for user info
        while True:
            name = input("Please enter your name: ")#1
            separator()
            if len(name) < 3:
                    print("Name must be at least 3 characters long!\n")                    
                    continue
            else:
                break

        while True:
            password = input("Please enter your password: ")#2
            separator()
            if len(password) < 8:
                    print("Password must be at least 8 characters long!\n")
                    
                    continue 
            else:
                break

        while True:
            number = input("Please enter your phone number: ")#3
            separator()
            if not number.isdigit() or len(number) < 11:
                print("enter a valid phone number\n")
                continue
            else:
                break

        while True:
            mail = input("Please enter your mail: ")#4
            separator()

            if "@" not in mail or "." not in mail:
                print("enter a valid email\n")
                continue

            for user in db_list:
                if user["Mail"] == mail:
                    print("This mail is already registered!\n")
                    break
            else:
                break

        # making sure to choose valid gender
        while True:
            gender = input("Please choose your gender:\n1. Male\n2. Female\nYour option: ")
            separator()
            
            if gender == "1":
                gender = "Male"
                break
            elif gender == "2":
                gender = "Female"
                break
            else:
                print("Choose correct gender option!")
                continue
        while True:

            age = input("Please enter your age: ")
            separator()
            # can't sign up if the age is not a number
            if not age.isdigit():
                print("Age must be a number\n")
                continue

            age = int (age)
            if age < 18:
                print("Sorry you must be at least 18 years old to have an account \n")
                continue
            break

        city = input("Please enter your city: ")
        separator()
    

        # adding the new user info to a dictionary
        new_user = {
            "ID" : len(db_list) + 1,
            "Name" : name,
            "Password": password,
            "Number" : number,
            "Mail" : mail,
            "Gender" : gender,
            "Age" : age,
            "City" : city,
            "balance" : 0
        }
        
        return new_user
        

def deposit(current_user, db_list):
    """Handle deposit for the current user."""
    # Repeat until a valid transaction is completed or user exits
    retry=True

    while retry:   #to keep retrying the page if the user entered wrong input
        deposit_input = input("Please enter the amount you want to deposit and the currency in this format '10 USD' \nOr enter esc to return to menu\n Your entry : ").split() #splitting the input to a list to get the amount and the currency separately
        if not deposit_input:
            print("Please enter an amount.")
            separator()
            continue

        if deposit_input[0].lower() == 'esc' :
            separator()          
            break

        #check if the input in right form
        if len(deposit_input) == 2 and deposit_input[0].isdigit() and deposit_input[1].upper() in rates_dict :            
            amount = int(deposit_input[0]) #the amount to deposit ,its the 1st part of entered list
            currency = deposit_input[1].upper() #the currency of deposit,2nd part of entered list in upper case to match the dictionary keys

            #updating users balance
            current_user['balance'] += amount * rates_dict[currency]
            
            #Update the database
            save_database(db_list)

            print(f"{deposit_input[0]} {deposit_input[1]} was deposited successfully!!\n")
            print (f"Your balance is {current_user['balance']} EGP\n")
            separator()
            break
        else:
            print('please enter the amount in the right format ')
            separator()
            continue
    
def withdraw(current_user, db_list):
    """Handle withdrawal for the current user."""
    retry = True #to retry the page if the user doesnt have enought money to send or he entered wrong receivers ID
    while retry :

        withdraw_input = input("Enter amount to withdraw : \nOr enter esc to return to menu\n Amount:")
    
        if withdraw_input.lower() == 'esc' :
            separator()
            break

        #checking users entry
        if  not withdraw_input.isdigit():
            print ("please enter a number to specify amount ")
            separator()
            continue
            
        withdraw_input = int (withdraw_input) #to avoid data type error

        #check if user have sufficient balance 
        if withdraw_input > current_user["balance"]:
            print("you dont have enough balance ")
            separator()
            continue
        else:
            #success
            #decreasing users balance
            current_user["balance"] -= withdraw_input
            retry = False

            #update the database
            save_database(db_list)           

            print("Withdrawal completed successfully ")
            print(f"your new balance is {current_user['balance']}")
            separator()

def transfer(current_user, db_list):
    retry = True #to retry the page if the user doesnt have enought money to send or he entered wrong receivers ID
    while retry:
        transfer_input = input("Please enter the amount you want to transfer \nOr enter esc to go back to main menu \n Amount : ")          
        if transfer_input.lower() == 'esc' :
            separator()
            break

        #checking users input
        if  not transfer_input.isdigit()  :
            print("transfer amount should be a number ")
            separator()
            continue

        transfer_input = int(transfer_input)
        receiver_id = input("Please enter the ID of the account you want to transfer money to \n Receviver's ID : ")

        if not receiver_id.isdigit():
            print("Receiver ID must be a number.")
            continue

        receiver_id = int(receiver_id)

        #checking a sufficient amount exist in user account
        if transfer_input > current_user['balance']:
            print("insufficient amount in your balance \n Try again")
            separator()
            continue
    
        #checking if the receiver exist
        receiver = None

        for user in db_list:
            if user["ID"] == receiver_id:
                receiver = user
                break

        if receiver is None:
            print("user doesnt exist or the id is invalid ")
            separator()
            continue

        if transfer_input <=0 :
            print ("please enter a valid amount to transfer ")
            separator()
            continue
            
        if receiver_id == current_user["ID"] :
            print ("you cant send money back to your account ")
            separator()
            continue

        #success
        receiver['balance'] += transfer_input
        #decraese sender's balance
        current_user['balance']-=transfer_input

        save_database(db_list)

        print(f"{transfer_input} EGP was successfully transfered to {receiver['Name']} ")
        print(f"your balance is {current_user['balance']}")
        separator()
        break

def delete_account(current_user, db_list):
    """Delete the current user's account."""
    confirmation = input("Are you sure you want to delete your account?\nThis action cannot be undone.\n(yes/no):")
    if confirmation.lower() == "yes":
        for user in db_list:
            if user["ID"] == current_user["ID"]:
                db_list.remove(user)
                break
        save_database(db_list)
        print("Your account has been deleted successfully.")
        separator()
        return True  # Indicate that the account was deleted
    else:
        print("Account deletion canceled.")
        separator()
        return False  # Indicate that the account was not deleted


def show_profile(current_user):
    """Display the current user's profile information."""
    print(f"Your personal information : \n Name : {current_user['Name']} \n ID : {current_user['ID']} \n Phone number : {current_user['Number']} \n Mail : {current_user['Mail']} \n Gender : {current_user['Gender']} \n Age : {current_user['Age']} \n City : {current_user['City']} \n Balance : {current_user['balance']} EGP")
    
    separator()

    while True:
        option = input(" [1]To edit your information \n [esc]To go back to main menu \n").lower()

        if option in ("1", "esc"):
            return option.lower()

        print("Invalid option.")
        separator()

def edit_profile(current_user, db_list):
    """Edit the current user's profile information."""
    while True:
        print("************ Edit your personal information ************")
        print("Choose the field you want to edit:\n[1] Name\n[2] Password\n[3] Phone number\n[4] Mail\n[esc] to go back to main menu")
        input_option = input("Your option: ")
        separator()

        #Name
        if input_option == "1":
            while True:
                new_name = input("Enter your new name: ")
                separator()
                if new_name == current_user["Name"]:
                    print("You must enter a different name.\n")
                    continue
                if len(new_name) < 3:
                        print("Name must be at least 3 characters long!\n")                    
                        continue
                else:
                    current_user["Name"] = new_name
                    break

        #Password
        elif input_option == "2":
            while True:
                new_password = input("Enter your new password: ")
                separator()
                if new_password == current_user["Password"]:
                    print("You must enter a different password.\n")
                    continue
                if len(new_password) < 8:
                    print("Password must be at least 8 characters long!\n")
                    continue
                else:
                    current_user["Password"] = new_password
                    break
        
        #Phone number
        elif input_option == "3":
            while True:
                new_number = input("Enter your new phone number: ")
                separator()
                if new_number == current_user["Number"]:
                    print("You must enter a different phone number.")
                    continue

                if not new_number.isdigit() or len(new_number) < 11:
                    print("enter a valid phone number\n")
                    continue
                else:
                    current_user["Number"] = new_number
                    break
        
        #Mail
        elif input_option == "4":
            while True:
                new_mail = input("Enter your new mail: ")
                separator()
                if new_mail == current_user["Mail"]:
                    print("You must enter a different email.")
                    continue
                if "@" not in new_mail or "." not in new_mail:
                    print("enter a valid email\n")
                    continue
                for user in db_list:
                    if user["Mail"] == new_mail and user["ID"] != current_user["ID"]:
                        print("This mail is already registered!\n")
                        break      
                else:
                    current_user["Mail"] = new_mail
                    break

        #Exit
        elif input_option == "esc":
            break
        
        #Invalid input
        else:
            print("Invalid option. Please try again.")
        
        # Save the updated user information to the database
        save_database(db_list)
        print("Information updated successfully\nDo you want to edit another field?")
        while True:
            choice = input(" [1]Yes\n [2]No,go back to main menu\nYour option: ").lower()
            separator()
            if choice == "1":
                break
            elif choice == "2":
                return
            else:
                print("Invalid option. Please try again.")
        separator()


def main():

    initialize_database()
    db_list = load_database()


    # if the user could sign/register it will be "True"
    logged_in = False
    while not logged_in:#home page loop
        print("\n***************** Welcome to SIC bank management system *****************")
        # saving the user login/sign up option in (sign_option) variable
        sign_option = input("Choose an option:\n1. (Login) if you already have an accont\n2. (Register) if you don't have an accont\n3. (Exit)\nYour option: ")
        separator()

        # login part***********
        if sign_option == "1":
            current_user = login(db_list)
            if current_user:
                logged_in = True
                break    
                
        # register part********
        elif sign_option == "2":
            new_user = register(db_list)
            db_list.append(new_user)
            # loading the new user to the data
            save_database(db_list)
            print(f"Signed up successfully!, your id is: {new_user['ID']}\nPlease remeber your id and password to login next time")
            separator()
            logged_in = True
            current_user = new_user 
            break

        # exit part ************
        elif sign_option == "3":
            print("Goodbye \n See you soon ")
            break
        # invalid input part ***
        else:
            print("Please choose a correct option \n")
            separator()
            continue        


    while logged_in:
        print(f"*********** Welcome {current_user['Name']} ***********")

        # we must put the rest of the bank management system here ___________________________________________________________
        menu_choice = input(f"Please enter your choice : \n[0]Deposit\n[1]Withdraw\n[2]Transfer\n[3]check balance & personal info\n[4]Delete Account\n[5]Exit\nyour choice : ")
        separator()
        
        #checking for invalid inputs(letters,symbols)
        if not menu_choice.isdigit():
            print("please enter avalid choice ")
            separator()
            continue
        menu_choice = int(menu_choice) #to avoid errors


        #Deposit
        if menu_choice == 0 :
            deposit(current_user, db_list)  
            continue

        #withdraw
        elif menu_choice == 1 :
            withdraw(current_user, db_list)           
            continue    

        #transfer
        elif menu_choice == 2 :
            transfer(current_user, db_list)             
            continue

        elif menu_choice ==3 :
            choice = show_profile(current_user)
            if choice == "1":
                edit_profile(current_user, db_list)
                continue
            elif choice == "esc":
                continue

        #delete account
        elif menu_choice == 4 :
            if delete_account(current_user, db_list):
                break #exit the loop after deleting the account
            else:
                continue #if the user cancels the deletion, show the menu again

        #exit
        elif menu_choice == 5 :
            print("good bye \n see you soon ")
            break

        #invalid input
        else: 
            print( "invalid key , please enter a number from 0 to 5 \n ")
            continue #shows menu again


if __name__ == "__main__":
    main()