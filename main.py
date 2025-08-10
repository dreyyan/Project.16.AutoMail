''' IMPORTS: MAIN '''
import time, json, random, string, os, hashlib, re
from datetime import datetime

''' IMPORTS: EMAIL AUTOMATION '''
import smtplib
from email.message import EmailMessage

''' MODULES '''
from modules.character_delay_animation import character_delay_animation
from modules.clear_screen import clear_screen
from modules.delay import delay
from modules.display_format import display_format
from modules.display_function import display_function
from modules.display_header import display_header
from modules.display_line import  display_line
from modules.error_message import error_message
from modules.insert_spaces import insert_spaces
from modules.line_delay_animation import line_delay_animation
from modules.press_enter_to_continue import press_enter_to_continue
    
''' GLOBALS '''
email = None
password = None

# Load email and password
try:
    with open("settings.json", "r") as f:
        data = json.load(f)
        email = data.get("email", "")
        password = data.get("password", "")
except FileNotFoundError:
    email = ""
    password = ""
    
''' METHODS '''
def isValidEmail(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None
    
def isValidPassword(password):
    return re.match(r"^([a-z]{4} ){3}[a-z]{4}$", password) is not None    

# METHOD: Create Email
def createEmail():
    while True:
        # Display header
        clear_screen()
        insert_spaces(18)
        display_header("AutoMail", "CREATE EMAIL", '#', 18, False)
        
        # Prompt user to enter details for composing an email
        subject_input = input("Enter Subject: ").strip()
        recipient_input = input("Enter Recipient: ").strip()
        message_input = input("Enter Message: ").strip()
            
        # Review details
        display_line('#', 49)
        print()
        display_line(' ', 17)
        line_delay_animation(" EMAIL DETAILS ", 0.1)
        display_line('-', 49)
        print()
        line_delay_animation(f"  Subject: {subject_input}", 0.1)
        line_delay_animation(f"Recipient: {recipient_input}", 0.1)
        line_delay_animation(f"  Message:\n{message_input}", 0.1)
        display_line('#', 49)
        print()
        
        # Ask user to confirm sending email
        while True:
            user_confirmation = input("Send Email[y/n]?: ")[0]
            
            if user_confirmation == 'y':
                # 1. Set up the email
                msg = EmailMessage()
                msg["Subject"] = subject_input
                msg["From"] = email
                msg["To"] = recipient_input
                msg.set_content(message_input)

                # 2. Gmail SMTP server setup
                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                # 3. Send the email
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(str(email), str(password))
                    server.send_message(msg)
                    
                # Get current date and time
                now = datetime.now()

                # Format date and time to string
                current_time = now.strftime("%m-%d-%Y %H:%M")
                
                # 4. Upload email details to history
                data_to_insert = {
                    "date": current_time,
                    "subject": subject_input,
                    "sender": email,
                    "recipient": recipient_input,
                    "message": message_input
                }
                
                try:
                    # 1. Read existing data
                    with open("history.json", "r") as f:
                        history = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    history = []

                # 2. Append new data
                history.append(data_to_insert)

                # 3. Write back to the file
                with open("history.json", "w") as f:
                    json.dump(history, f, indent=4)

                line_delay_animation("* Email sent!", 2)
                
                # prompt user to create & send an email again
                user_choice = input("Would you like to create & send another email? [y/n]: ").lower().strip()
            
                if user_choice not in ['y', 'n']:
                    error_message("Invalid input, please enter 'y' for yes and 'n' for no", 2)
                else: break
                
            elif user_confirmation == 'n':
                line_delay_animation("* Email cancelled...", 2)
                goToMainMenu()
        
        if user_choice == 'y':
            continue
        elif user_choice == 'n':
            break

            
# METHOD: Check History
def checkHistory():
    # Display header
    clear_screen()
    insert_spaces(18)
    display_header("AutoMail", "CHECK HISTORY", '#', 18, True)
    
    # Read history
    with open("history.json", "r") as f:
        data = json.load(f)
        
    for email in data:
        print(f"[ {email['date']} ]\nSubject: {email['subject']}\nSender: {email['sender']}\nRecipient: {email['recipient']}\nMessage: {email['message']}")
        display_line('=', 49)
        print()
        
    press_enter_to_continue()

# NAVIGATION: MAIN MENU
def goToMainMenu():
    global email, password
    while True:
        clear_screen()
        # Display header
        insert_spaces(18)
        display_header("AutoMail", "MAIN  MENU", '#', 19, False)

        # Display functions
        display_function(1, "Create Email")
        display_function(2, "Check History")
        display_function(3, "Settings")
        display_function(4, "Exit")

        display_line('=', 49)
        print()

        # Prompt user to enter a choice
        while True:
            try:
                user_choice = int(input(">> ").strip())
                if user_choice not in range(1, 5):
                    error_message("Invalid input, please enter a valid choice[1-4]", 2)
                else: break
            except ValueError:
                error_message("Invalid input, please enter a valid choice[1-4]", 2)
                
        # [1] Create Email
        if user_choice == 1:
            createEmail()

        # [2] Check History
        elif user_choice == 2:
            checkHistory()

        # [3] Settings
        elif user_choice == 3:
            goToSettings()

        # [4] Exit
        elif user_choice == 4:
            line_delay_animation("* exiting system...", 1)
            exit(0)

def updateCredentials():
    global email, password
    
    while True:
        # Display header
        clear_screen()
        insert_spaces(18)
        display_header("AutoMail", "UPDATE CREDENTIALS", '#', 15, False)
        
        line_delay_animation(f"Email: {email}", 0.1)
        line_delay_animation(f"Password: {password}", 0.1)
        display_line('#', 49)
        print()
        line_delay_animation(f"NOTE: Make sure 2FA is enabled, and use an app\npassword instead of your actual password.", 0.1)
        display_line('#', 49)
        print()
        
        # Prompt user to enter new credentials
        while True:
            user_email = input("Enter new email: ").strip()
            if not isValidEmail(user_email):
                error_message("Invalid email", 2)
            else: break
        
        while True:
            user_password = input("Enter new password: ").strip()
            if not isValidPassword(user_password):
                error_message("Invalid password", 2)
            else: break
            
        # Update credentials
        data_to_insert = {
            "email": user_email,
            "password": user_password
        }
        
        with open("settings.json", "w") as f:
            json.dump(data_to_insert, f, indent=4)
        
        line_delay_animation("* Credentials successfully updated", 2)
        goToSettings()

# NAVIGATION: SETTINGS
def goToSettings():
    global email, password
    
    while True:   
        # Display header
        clear_screen() 
        insert_spaces(18)
        display_header("AutoMail", "SETTINGS", '#', 20, False)
        
        # Display current settings
        line_delay_animation(f"   Email: {email}", 0.1)
        line_delay_animation(f"Password: {password}", 0.1)
        display_line('#', 49)
        print()
        
        # Display functions
        display_function(1, "Update Credentials")
        display_function(2, "Return to Menu")

        display_line('=', 49)
        print()
        
        # Prompt user to enter a choice
        while True:
            try:
                user_choice = int(input(">> ").strip())
                if user_choice not in range(1, 3):
                    error_message("Invalid input, please enter a valid choice[1-2]", 2)
                else: break
            except ValueError:
                error_message("Invalid input, please enter a valid choice[1-21]", 2)
        
        if user_choice == 1:
            updateCredentials()
            
        elif user_choice == 2:
            goToMainMenu()

''' MAIN '''
goToMainMenu()