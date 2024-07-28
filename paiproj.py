import sys
import random
import os
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont, QColor



class GameApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game App')
        self.setGeometry(200, 200, 300, 200)
        self.setFixedSize(700, 250)
        color = QColor.fromHsv(190, 255, 255)  # Hue: 180, Saturation: 135, Value: 255
        self.setStyleSheet(f"background-color: {color.name()};")

        self.username_label = QLabel('Username:', self)
        self.username_label.move(220, 50)
        self.username_text = QLineEdit(self)
        self.username_text.move(320, 50)

        self.password_label = QLabel('Password:', self)
        self.password_label.move(220, 80)
        self.password_text = QLineEdit(self)
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.move(320, 80)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        self.login_button.move(260, 135)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)
        self.register_button.move(370, 135)

        self.game1_button = QPushButton('Number Guessing Game', self)
        self.game1_button.clicked.connect(self.start_number_guessing_game)
        self.game1_button.move(265, 90)
        self.game1_button.hide()

        self.game2_button = QPushButton('Hangman', self)
        self.game2_button.clicked.connect(self.start_hangman_game)
        self.game2_button.move(320, 120)
        self.game2_button.hide()

        self.game3_button = QPushButton('Tic Tac Toe', self)
        self.game3_button.clicked.connect(self.start_tic_tac_toe_game)
        self.game3_button.move(315, 150)
        self.game3_button.hide()

        self.game4_button = QPushButton('Rock-Paper-Scissors', self)
        self.game4_button.clicked.connect(self.start_Rock_Paper_Scissors)
        self.game4_button.move(280, 180)
        self.game4_button.hide()

        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.move(610, 220)
        self.logout_button.hide()

        self.delete_button = QPushButton('Account delete', self)
        self.delete_button.clicked.connect(self.confirm_delete_account)
        self.delete_button.move(20, 220)
        self.delete_button.hide()

        self.loan_button = QPushButton('L\nO\nA\nN', self)
        self.loan_button.clicked.connect(self.loan)
        self.loan_button.move(20, 100)
        self.loan_button.hide()
        self.username = None
        self.loan_attempts = 0
        self.loan_amount = 0# Initialize loan_attempts to 0

        self.login_message1 = QLabel('Login now and let the excitement begin!!', self)
        self.login_message1.move(250, 180)
        self.login_message1.setFont(QFont("Arial", 10.5))  # Set the font to smaller size

        self.login_message2 = QLabel('Don\'t have an account? Just register the desired username and password and you\'re good to go!', self)
        self.login_message2.setFont(QFont("Arial", 10.5))
        self.login_message2.move(100, 200)
        
        self.username = None
        self.loan_attempts = self.read_loan_attempts(self.username)
        self.loan_amount = 0
      
        self.update_login_page_messages()
        self.remaining_attempts = 3

        
  # Update the initial login page messages
        
    def loan(self):
    # Read loan attempts from the loan_attempts.txt file
        loan_attempts = self.read_loan_attempts(self.username)
        loan_amount = self.read_loan(self.username)
    
        # Create loan amount input field
        loan_amount_input = QLineEdit(self)
        loan_amount_input.setPlaceholderText("Enter loan amount")
        loan_amount_input.setGeometry(20, 20, 200, 30)
    
        # Create take loan button
        take_loan_button = QPushButton("Take Loan", self)
        take_loan_button.setGeometry(20, 60, 100, 30)
    
        # Create repay loan button
        repay_loan_button = QPushButton("Repay Loan", self)
        repay_loan_button.setGeometry(140, 60, 100, 30)
    
        # Create loan label to display the current loan amount
        loan_label = QLabel(f'Loan: {loan_amount}', self)
        loan_label.setGeometry(20, 100, 150, 30)
    
        # Create attempts label to display the remaining loan attempts
        attempts_label = QLabel(f"Attempts: {loan_attempts}", self)
        attempts_label.setGeometry(180, 100, 150, 30)
        
        # Connect the take_loan() function to the take loan button
        take_loan_button.clicked.connect(lambda: self.take_loan(loan_amount_input.text(), loan_amount_input, take_loan_button, repay_loan_button, loan_label, attempts_label))


        # Connect the repay_loan() function to the repay loan button
        repay_loan_button.clicked.connect(lambda: self.repay_loan(loan_amount_input.text(), loan_amount_input, take_loan_button, repay_loan_button, loan_label, attempts_label))
    
        loan_amount_input.show()
        take_loan_button.show()
        repay_loan_button.show()
        loan_label.show()
        attempts_label.show()
        self.username_label.hide()
        self.username_text.hide()
        self.password_label.hide()
        self.password_text.hide()
        self.login_button.hide()
        self.register_button.hide()
        self.game1_button.hide()
        self.game2_button.hide()
        self.game3_button.hide()
        self.game4_button.hide()
        self.logout_button.hide()
        self.delete_button.hide()
        self.welcome_label.hide()
        self.tokens_label.hide()
        self.loan_button.hide()
    
    def take_loan(self,loan_amount, loan_amount_input, take_loan_button, repay_loan_button, loan_label, attempts_label):
        
    # Check if the user already has an active loan
        if self.has_active_loan(self.username):
            QMessageBox.warning(self, "Active Loan", "You already have an active loan.")
            return
    
        # Check if the loan amount is valid
        try:
            loan_amount = int(loan_amount)
            if loan_amount <= 0:
                QMessageBox.warning(self, "Invalid Loan Amount", "Please enter a valid loan amount.")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Loan Amount", "Please enter a valid loan amount.")
            return
    
        # Check if the user has reached the maximum number of loan attempts
        loan_attempts = self.read_loan_attempts(self.username)
        if loan_attempts == 0:
            QMessageBox.warning(self, "Loan Attempts Exceeded", "You have reached the maximum number of loan attempts.")
            return
    
        # Check if the requested loan amount exceeds the maximum loan limit
        if loan_amount > 2000:
            QMessageBox.warning(self, "Loan Limit Exceeded", "The requested loan amount exceeds the maximum limit.")
            return    
        # Update the loan amount for the user
        
        user_loan = self.read_loan(self.username)
        user_loan += loan_amount
        self.update_loan(user_loan, self.username)  # Update loan in loans.txt
        self.update_tokens(loan_amount, self.username)  # Add the repaid loan amount to the user's tokens in tokens.txt
        # Decrement the loan attempts
        self.decrement_loan_attempts(self.username)
    
        # Update the loan label
        self.update_loan_label(loan_label, attempts_label)
    
        # Display success message
        QMessageBox.information(self, "Loan Taken", "Congratulations! You have successfully taken a loan.")
    
        
    def repay_loan(self,system_tokens, loan_amount, loan_amount_input, take_loan_button, repay_loan_button, loan_label, attempts_label):
        # Check if the loan amount is valid
        try:
            loan_amount = int(loan_amount)
            if loan_amount <= 0:
                QMessageBox.warning(self, "Invalid Loan Amount", "Please enter a valid loan amount.")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Loan Amount", "Please enter a valid loan amount.")
            return
    
        # Check if the user has an active loan to repay
        loan_balance = self.read_loan(self.username)
        if loan_balance == 0:
            QMessageBox.warning(self, "No Active Loan", "You don't have an active loan to repay.")
            return
    
        # Check if the loan amount is greater than the loan balance
        if loan_amount > loan_balance:
            QMessageBox.warning(self, "Invalid Repayment Amount", "You cannot repay more than the loan balance.")
            return
     
        # Deduct the loan amount from the user's loan
        loan_balance -= loan_amount
        self.update_tokensmin(loan_amount, self.username)
        self.update_loan(loan_balance, self.username)  # Update loan in loans.txt
        
    
        # Check if the user has used all their loan attempts
        loan_attempts = self.read_loan_attempts(self.username)
        if loan_attempts >= 3:
            # Reset the loan attempts to 3
            self.reset_loan_attempts(self.username)
        else:
            # Increment the loan attempts by the number of loans repaid
            self.increment_loan_attempts(3 - loan_attempts, self.username)
    
        # Update the loan label and attempts label
        self.update_loan_label(loan_label, attempts_label)
    
        # Enable the take loan button after repaying the loan
        take_loan_button.setEnabled(True)
    
        # Disable the repay loan button after repaying the loan
        repay_loan_button.setEnabled(True)
    
        # Clear the loan amount input field
        loan_amount_input.clear()
    
        # Display success message
        QMessageBox.information(self, "Loan Repaid", "Your loan has been repaid successfully.")

    def increment_loan_attempts(self, count, username):
    # Read loan attempts from the loan_attempts.txt file
        loan_attempts = self.read_loan_attempts(username)
    
        # Increment the loan attempts by the specified count
        loan_attempts += count
    
        # Update the loan attempts in the loan_attempts.txt file
        with open("loan_attempts.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                line_parts = line.strip().split(":")
                if len(line_parts) == 2:
                    u, attempts = line_parts
                    if u == username:
                        file.write(f"{u}:{loan_attempts}\n")
                    else:
                        file.write(line)
                else:
                    file.write(line)
            file.truncate()

    
        # Update the loan attempts in the loan_attempts.txt file
        with open("loan_attempts.txt", "r+") as file:
            data = file.readlines()
            file.seek(0)
            for line in data:
                if line.startswith(username):
                    file.write(f"{username}:{loan_attempts}\n")
                else:
                    file.write(line)
            file.truncate()
    
    def reset_loan_attempts(self, username):
        # Reset the loan attempts to 0 in the loan_attempts.txt file
        with open("loan_attempts.txt", "r+") as file:
            data = file.readlines()
            file.seek(0)
            for line in data:
                if line.startswith(username):
                    file.write(f"{username}:0\n")
                else:
                    file.write(line)
            file.truncate()
    
    def read_loan_attempts(self, username):
        try:
            with open("loan_attempts.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line_parts = line.strip().split(":")
                    if len(line_parts) == 2:
                        u, attempts = line_parts
                        if u == username:
                            return int(attempts)
                return 0
        except FileNotFoundError:
            return 0
    
    def read_loan(self, username):
        try:
            with open("loans.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line_username, amount = line.strip().split(":")
                    if line_username == username:
                        return int(amount)
                return 0
        except FileNotFoundError:
            return 0
    
    def has_active_loan(self, username):
        loan_attempts = self.read_loan_attempts(username)
        return loan_attempts == 0
    
    def decrement_loan_attempts(self, username):
    # Read loan attempts from the loan_attempts.txt file
        loan_attempts = self.read_loan_attempts(username)
    
        # Decrement the loan attempts
        loan_attempts -= 1
    
        # Update the loan attempts in the loan_attempts.txt file
        with open("loan_attempts.txt", "r+") as file:
            data = file.readlines()
            file.seek(0)
            for line in data:
                if line.startswith(username):
                    file.write(f"{username}:{loan_attempts}\n")
                else:
                    file.write(line)
            file.truncate()
        
    def read_tokens(self):
        try:
            with open("tokens.txt", "r") as file:
                lines = file.readlines()
                tokens = {}
                for line in lines:
                    username, amount = line.strip().split(":")
                    tokens[username] = int(amount)
                return tokens
        except FileNotFoundError:
            return {}
    
    def update_loan_attempts(self, attempts, username):
        with open("loan_attempts.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                line_username, _ = line.strip().split(":")
                if line_username == username:
                    file.write(f"{username}:{attempts}\n")
                else:
                    file.write(line)
            file.truncate()
    
    def get_loan_amount(self):
        with open("loans.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                username, loan = line.strip().split(":")
                if username == self.username:
                    return int(loan)
        return 0
    
    def update_loan(self, loan_amount, username):
        with open("loans.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                line_username, _ = line.strip().split(":")
                if line_username == username:
                    file.write(f"{username}:{loan_amount}\n")
                else:
                    file.write(line)
            file.truncate()
            
    def update_tokens(self, token_difference, username):
        tokens = self.read_tokens()
    
        user_tokens = tokens.get(username, 0)
        user_tokens = int(user_tokens)
        user_tokens += token_difference
    
        tokens[username] = str(user_tokens)
        os.chmod("tokens.txt", 0o777)
        with open("tokens.txt", "w") as file:
            for username, token_value in tokens.items():
                file.write(f"{username}:{token_value}\n")
                
    def update_tokensmin(self, token_difference, username):
        tokens = self.read_tokens()
    
        user_tokens = tokens.get(username, 0)
        user_tokens = int(user_tokens)
        user_tokens -= token_difference
    
        tokens[username] = str(user_tokens)
        os.chmod("tokens.txt", 0o777)
        with open("tokens.txt", "w") as file:
            for username, token_value in tokens.items():
                file.write(f"{username}:{token_value}\n")                
    
    def update_loan_label(self, loan_label, attempts_label):
        loan_amount = self.read_loan(self.username)
        loan_label.setText(f"Loan: {loan_amount}")
        attempts = self.read_loan_attempts(self.username)
        attempts_label.setText(f"Attempts: {attempts}")

    def update_login_page_messages(self):
        if self.username is None:
            self.login_message1.show()
            self.login_message2.show()
        else:
            self.login_message1.hide()
            self.login_message2.hide()

    def login(self):
     username = self.username_text.text()
     password = self.password_text.text()

     if username == '' and password == '':
        QMessageBox.warning(self, 'Login', 'Please enter both username and password!')
        return
     elif username == '':
        QMessageBox.warning(self, 'Login', 'Please enter the username!')
        return
     elif password == '':
        QMessageBox.warning(self, 'Login', 'Please enter the password!')
        return

     if self.authenticate(username, password):
        self.username = username
        self.show_game_selection()
        self.update_login_page_messages()
     else:
        QMessageBox.warning(self, 'Login', 'Invalid username or password!')
    
    
    def add_tokens(self, username, tokens):
    # Temporarily remove the read-only attribute
     os.chmod('tokens.txt', 0o777)

    # Read the existing tokens from the tokens file
     with open('tokens.txt', 'r') as file:
        token_lines = file.readlines()

    # Update the tokens for the user
     updated_tokens = f"{username}:{tokens}\n"
     for i, line in enumerate(token_lines):
        if line.startswith(username + ':'):
            token_lines[i] = updated_tokens
            break
     else:
        token_lines.append(updated_tokens)

    # Write the updated tokens back to the tokens file
     with open('tokens.txt', 'w') as file:
        file.writelines(token_lines)

    # Restore the read-only attribute
    os.chmod('tokens.txt', 0o444)
    
    def add_loan(self, username, loans):
    # Temporarily remove the read-only attribute
     os.chmod('loans.txt', 0o777)

    # Read the existing tokens from the tokens file
     with open('loans.txt', 'r') as file:
        loans_lines = file.readlines()

    # Update the tokens for the user
     updated_loan = f"{username}:{loans}\n"
     for i, line in enumerate(loans_lines):
        if line.startswith(username + ':'):
            loans_lines[i] = updated_loan
            break
     else:
        loans_lines.append(updated_loan)

    # Write the updated tokens back to the tokens file
     with open('loans.txt', 'w') as file:
        file.writelines(loans_lines)

    # Restore the read-only attribute
    os.chmod('loans.txt', 0o444)
    def add_loan_attempts(self, username, loan_attempts):
    # Temporarily remove the read-only attribute
     os.chmod('loan_attempts.txt', 0o777)

    # Read the existing tokens from the tokens file
     with open('loan_attempts.txt', 'r') as file:
        attempt_lines = file.readlines()

    # Update the tokens for the user
     updated_loan_attempts = f"{username}:{loan_attempts}\n\n"
     for i, line in enumerate(attempt_lines):
        if line.startswith(username + ':'):
            attempt_lines[i] = updated_loan_attempts
            break
     else:
        attempt_lines.append(updated_loan_attempts)

    # Write the updated tokens back to the tokens file
     with open('loan_attempts.txt', 'w') as file:
        file.writelines(attempt_lines)

    # Restore the read-only attribute
    os.chmod('loan_attempts.txt', 0o444)
    def add_account(self, account):
        with open('login.txt', 'a') as file:
            file.write(account)
            
    def register(self):
        # Get the entered username and password
        username = self.username_text.text()
        password = self.password_text.text()

        # Check if username or password fields are empty
        if username == '':
            QMessageBox.warning(self, 'Registration', 'Please enter a username!')
            return
        elif password == '':
            QMessageBox.warning(self, 'Registration', 'Please enter a password!')
            return

        # Check if the username is already taken
        if self.username_exists(username):
            QMessageBox.warning(self, 'Registration', 'Username already exists!')
        else:
            # Add the new account to the database (text file)
            self.add_account(f"{username}:{password}\n")
            self.add_tokens(username,1000)  # Add 1000 tokens for the new user
            self.add_loan(username,0)
            self.add_loan_attempts(username,3)
            QMessageBox.information(self, 'Registration', 'Registration successful!\nCongratulations for 1000 tokens!')
    
    def create_account(self, username, password):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        login_file = os.path.join(script_dir, 'login.txt')

        with open(login_file, 'a') as file:
            file.write(f'{username}:{password}\n')

        tokens_file = os.path.join(script_dir, 'tokens.txt')

        with open(tokens_file, 'a') as file:
            file.write(f'{username}:0\n')
       
    def remove_tokens(self, username):
        # Temporarily remove the read-only attribute
        os.chmod('tokens.txt', 0o777)

        # Remove tokens for a user from the tokens file
        with open('tokens.txt', 'r') as file:
            token_lines = file.readlines()
        with open('tokens.txt', 'w') as file:
            for line in token_lines:
                if not line.startswith(username + ':'):
                    file.write(line)
                    
    def remove_loan(self, username):
        # Temporarily remove the read-only attribute
        os.chmod('loans.txt', 0o777)

        # Remove tokens for a user from the tokens file
        with open('loans.txt', 'r') as file:
            loans_lines = file.readlines()
        with open('loans.txt', 'w') as file:
            for line in loans_lines:
                if not line.startswith(username + ':'):
                    file.write(line)
                    
    def remove_attempts(self, username):
        # Temporarily remove the read-only attribute
        os.chmod('loan_attempts.txt', 0o777)

        # Remove tokens for a user from the tokens file
        with open('loan_attempts.txt', 'r') as file:
            attempt_lines = file.readlines()
        with open('loan_attempts.txt', 'w') as file:
            for line in attempt_lines:
                if not line.startswith(username + ':'):
                    file.write(line)
                    
    def username_exists(self, username):
        with open('login.txt', 'r') as file:
            login = file.readlines()
            for account in login:
                if username == account.split(':')[0]:
                    return True
        return False

    def authenticate(self, username, password):
        with open('login.txt', 'r') as file:
            login = file.readlines()
            for account in login:
                if f'{username}:{password}\n' == account:
                    return True
        return False
    
    def confirm_delete_account(self):
        # Get the entered username to delete
        username = self.username_text.text()
        password = self.password_text.text()
        # Check if username field is empty
        if username == '':
            QMessageBox.warning(self, 'Delete Account', 'Please enter a username!')
            return
        if password == '':
            QMessageBox.warning(self, 'Delete Account', 'Please enter a password!')
            return
        # Check if the username exists in the database
        if self.username_exists(username):
            # Show confirmation dialog
            confirm_dialog = QMessageBox.question(self, 'Delete Account', 'Are you sure you want to delete the account?', QMessageBox.Yes | QMessageBox.No)
            if confirm_dialog == QMessageBox.Yes:
                # Delete the account from the database
                self.remove_account(username)
                self.remove_tokens(username)
                self.remove_loan(username) 
                self.remove_attempts(username)
                
                QMessageBox.information(self, 'Delete Account', 'Account deleted successfully!')
                
                self.username = None
                self.username_label.show()
                self.username_text.show()
                self.username_text.setText('')
                self.password_label.show()
                self.password_text.show()
                self.password_text.setText('')
                self.login_button.show()
                self.register_button.show()
                self.game1_button.hide()
                self.game2_button.hide()
                self.game3_button.hide()
                self.game4_button.hide()
                self.logout_button.hide()
                self.update_login_page_messages()
                self.delete_button.hide()
                self.welcome_label.hide()
                self.tokens_label.hide()
                self.loan_button.hide()
        else:
            QMessageBox.warning(self, 'Delete Account', 'Username does not exist!')
        
    def remove_account(self, username):
        # Temporarily remove the read-only attribute
        os.chmod('login.txt', 0o777)
        
        # Remove an account from the database (text file)
        with open('login.txt', 'r') as file:
            logins = file.readlines()
        with open('login.txt', 'w') as file:
            for login in logins:
                acc_username = login.split(':')[0].strip()
                if username != acc_username:
                    file.write(login)

    def start_number_guessing_game(self):
     tokens = self.get_user_tokens()
     if tokens < 150:
        QMessageBox.warning(self, 'Insufficient Tokens', 'You do not have enough tokens to play this game!')
     else:
        self.subtract_tokens(150)
        self.play_number_guessing_game(tokens)


    def start_hangman_game(self):
        tokens = self.get_user_tokens()
        if tokens < 200:
            QMessageBox.warning(self, 'Insufficient Tokens', 'You do not have enough tokens to play this game!')
        else:
            self.subtract_tokens(200)
            self.play_hangman_game()
            
    def start_tic_tac_toe_game(self):
        tokens = self.get_user_tokens()
        if tokens < 250:
            QMessageBox.warning(self, 'Insufficient Tokens', 'You do not have enough tokens to play this game!')
        else:
            self.subtract_tokens(250)
            self.tic_tac_toe_game()
    
    def start_Rock_Paper_Scissors(self):
        tokens = self.get_user_tokens()
        if tokens < 300:
            QMessageBox.warning(self, 'Insufficient Tokens', 'You do not have enough tokens to play this game!')
        else:
            self.subtract_tokens(300)
            self.rock_paper_scissors_game()
            
    def play_number_guessing_game(self, tokens):
     QMessageBox.information(self, 'Number Guessing Game', 'Let\'s play the Number Guessing Game!')
     remaining_attempts = 6
     deducted_tokens = 0
     secret_number = random.randint(1, 100)

     while remaining_attempts > 0:
        guess, ok = QInputDialog.getInt(self, 'Number Guessing Game',
                                         f'Guess a number between 1 and 100\nAttempts left: {remaining_attempts}',
                                         min=1, max=100)

        if ok:
            if guess == secret_number:
                QMessageBox.information(self, 'Number Guessing Game', f'Congratulations! You guessed the number.\nHere are 150 tokens as a reward.')
                self.add_tokens(200)  # Add 150 tokens to the user's account
                break
            elif guess < secret_number:
                QMessageBox.information(self, 'Number Guessing Game', 'Too low! Guess again.')
            else:
                QMessageBox.information(self, 'Number Guessing Game', 'Too high! Guess again.')

            deducted_tokens += 100
            remaining_attempts -= 1
            if remaining_attempts == 0:
                self.subtract_tokens(100)
                QMessageBox.information(self, 'Number Guessing Game', 'You failed to guess the number within 6 attempts.\n100 tokens have been deducted.')
        else:
            QMessageBox.information(self, 'Number Guessing Game', 'Game canceled.')
            if deducted_tokens > 0:
                self.subtract_tokens(deducted_tokens)
            break

    def play_hangman_game(self):
     QMessageBox.information(self, 'Hangman Game', 'Let\'s play the Hangman Game!')
     deducted_tokens = 0
     words = ['apple', 'banana', 'orange', 'watermelon', 'strawberry', 'grapefruit', 'kiwi', 'pineapple']
     secret_word = random.choice(words)
     guessed_letters = []
     attempts = 6

     hangman_figure = [
        '   _________         ',
        '   |/      |         ',
        '   |      (_)        ',
        '   |      \|/        ',
        '   |       |         ',
        '   |      / \        ',
        '___|___              '
     ]

     while attempts > 0:
        masked_word = ''.join([letter if letter in guessed_letters else '*' for letter in secret_word])
        prompt = f'Guess the word: {masked_word}\nAttempts left: {attempts}\nEnter a letter:\n\n'
        hangman_prompt = '\n'.join(hangman_figure[:6 - attempts])

        guess, ok = QInputDialog.getText(self, 'Hangman Game', prompt + hangman_prompt)

        if not ok:
            QMessageBox.information(self, 'Number Guessing Game', 'Game canceled.')
            if deducted_tokens > 0:
                self.subtract_tokens(deducted_tokens)
            break

        guess = guess.lower()

        if len(guess) != 1:
            QMessageBox.warning(self, 'Hangman Game', 'Please enter a single letter!')
            continue

        if guess in guessed_letters:
            QMessageBox.warning(self, 'Hangman Game', 'You already guessed that letter!')
            continue

        guessed_letters.append(guess)

        if guess in secret_word:
            if all(letter in guessed_letters for letter in secret_word):
                QMessageBox.information(self, 'Hangman Game', f'Congratulations! You guessed the word: {secret_word}\n\nYou have been rewarded with 250 tokens.')
                self.add_tokens(250)   # Add 250 tokens to the user's account
                break
        else:
            attempts -= 1
            if attempts == 0:
                hangman_prompt = '\n'.join(hangman_figure)  # Show full hangman figure on game over
                QMessageBox.information(self, 'Hangman Game', f'Game over! The word was: {secret_word}\n\n{hangman_prompt}\n\n100 tokens have been deducted for playing.')
                self.subtract_tokens(100)  # Subtract 100 tokens from the user's account
            else:
                QMessageBox.information(self, 'Hangman Game', f'Incorrect guess! Attempts left: {attempts}\n\n{hangman_prompt}')
  
    def tic_tac_toe_game(self):
     QMessageBox.information(self, 'Tic Tac Toe Game', 'Let\'s play the Tic Tac Toe Game!')
     deducted_tokens = 0
    # Create an empty board
     board = [[' ' for _ in range(3)] for _ in range(3)]

    # Initialize player and game status variables
     player = 'X'
     game_over = False
     attempts = 9
     
     while not game_over:
         self.display_board(board)
         
         row, ok1 =QInputDialog.getInt(self, 'Tic Tac Toe Game', 'Enter the row (0-2):')
         col, ok2 = QInputDialog.getInt(self, 'Tic Tac Toe Game', 'Enter the column (0-2):')
         
         if not ok1 and not ok2:
             QMessageBox.information(self, 'Tic Tac Toe Game', 'Game canceled.')
             if deducted_tokens > 0:
                 self.subtract_tokens(deducted_tokens)
             break
         if not (0 <= row < 3) or not (0 <= col < 3) or board[row][col] != ' ':
           QMessageBox.warning(self, 'Tic Tac Toe Game', 'Invalid move. Try again.')
           continue
         board[row][col] = player

    # Check if the game is won
         if self.check_win(board, player):
          QMessageBox.information(self, 'Tic Tac Toe Game', f'Player {player} wins!')
          self.add_tokens(300)  # Add tokens to the player's account
          game_over = True  # Set game_over to True to exit the loop
          break

    # Check if it's a draw
         if attempts == 0:
          QMessageBox.information(self, 'Tic Tac Toe Game', 'It\'s a draw!')
          self.subtract_tokens(150)  # Subtract tokens from the player's account
          game_over = True  # Set game_over to True to exit the loop
          break

    # Switch to the next player
         player = 'O' if player == 'X' else 'X'
         attempts -= 1

# Display the final state of the board
     self.display_board(board)
    def display_board(self, board):
    # Display the current state of the board
     board_str = ""
     for row in board:
        board_str += ' | '.join(row) + '\n'
        board_str += '---------\n'
     QMessageBox.information(self, 'Tic Tac Toe Game', board_str)

    def get_player_move(self):
     row, ok1 = QInputDialog.getInt(self, 'Tic Tac Toe', 'Enter the row number (0-2):')
     col, ok2 = QInputDialog.getInt(self, 'Tic Tac Toe', 'Enter the column number (0-2):')
     if ok1 and ok2:
        return row, col
     else:
        return None, None

    def check_win(self, board, player):
    # Check rows
     for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    # Check columns
     for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Check diagonals
     if board[0][0] == board[1][1] == board[2][2] == player:
        return True
     if board[0][2] == board[1][1] == board[2][0] == player:
        return True

     return False

    def rock_paper_scissors_game(self):
     choices = ['rock', 'paper', 'scissors']
     attempts = 5  # Number of allowed attempts
     losses = 0  # Counter for losses

     QMessageBox.information(self, 'Rock-Paper-Scissors Game', "Let's play Rock-Paper-Scissors!")

     dialog = QDialog(self)
     dialog.setWindowTitle('Rock-Paper-Scissors Game')
     dialog.setFixedSize(300, 100)

     one_player_button = QPushButton('1 Player', dialog)
     one_player_button.setGeometry(20, 20, 120, 60)
     one_player_button.clicked.connect(lambda: self.start_game(dialog, 1))

     two_players_button = QPushButton('2 Players', dialog)
     two_players_button.setGeometry(160, 20, 120, 60)
     two_players_button.clicked.connect(lambda: self.start_game(dialog, 2))

     dialog.exec_()

    def start_game(self, dialog, game_type):
     dialog.close()

     choices = ['rock', 'paper', 'scissors']
     attempts = 5  # Number of allowed attempts
     losses = 0  # Counter for losses

     while losses < attempts:
        remaining_attempts = attempts - losses
        prompt = f"Choose one: Rock, Paper, or Scissors\nAttempts remaining: {remaining_attempts}"
        if game_type == 2:
            user_choice1, ok1 = QInputDialog.getText(self, 'Rock-Paper-Scissors Game', f"Player 1: {prompt}")
            user_choice2, ok2 = QInputDialog.getText(self, 'Rock-Paper-Scissors Game', f"Player 2: {prompt}")

            if not ok1 or not ok2 or user_choice1.lower() not in choices or user_choice2.lower() not in choices:
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', 'Game canceled.')
                return

            if user_choice1.lower() == user_choice2.lower():
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "It's a tie!")
            elif (user_choice1.lower() == 'rock' and user_choice2.lower() == 'scissors') or \
                    (user_choice1.lower() == 'paper' and user_choice2.lower() == 'rock') or \
                    (user_choice1.lower() == 'scissors' and user_choice2.lower() == 'paper'):
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "Player 1 wins!")
            else:
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "Player 2 wins!")

        elif game_type == 1:
            user_choice, ok = QInputDialog.getText(self, 'Rock-Paper-Scissors Game', prompt)
            user_choice = user_choice.lower()

            if not ok or user_choice not in choices:
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', 'Game canceled.')
                return

            computer_choice = random.choice(choices)
            QMessageBox.information(self, 'Rock-Paper-Scissors Game', f"The computer chose: {computer_choice}")

            if user_choice == computer_choice:
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "It's a tie!")
            elif (user_choice == 'rock' and computer_choice == 'scissors') or \
                    (user_choice == 'paper' and computer_choice == 'rock') or \
                    (user_choice == 'scissors' and computer_choice == 'paper'):
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "Congratulations! You win!")
                self.add_tokens(350)  # Add tokens to the player's account
                return
            else:
                QMessageBox.information(self, 'Rock-Paper-Scissors Game', "Sorry, you lose!")
                losses += 1

     QMessageBox.information(self, 'Rock-Paper-Scissors Game', f"You've reached the maximum number of attempts ({attempts}). Tokens will be subtracted.")
     self.subtract_tokens(200)

    def show_game_selection(self):
     self.username_label.hide()
     self.username_text.hide()
     self.password_label.hide()
     self.password_text.hide()
     self.login_button.hide()
     self.register_button.hide()
     self.game1_button.show()
     self.game2_button.show()
     self.game3_button.show()
     self.game4_button.show()
     self.logout_button.show()
     self.delete_button.show()
     welcome_message = f'Welcome, {self.username}! Take your pick and let the fun begin!'
     self.welcome_label = QLabel(welcome_message, self)
     self.welcome_label.move(150, 20)
     self.welcome_label.show()
     tokens = self.get_user_tokens()
     tokens_message = f'Tokens: {tokens}'
     self.tokens_label = QLabel(tokens_message, self)
     self.tokens_label.move(150, 50)
     self.tokens_label.show()
     self.loan_button.show()

        
    def logout(self):
     self.username = None
     self.username_label.show()
     self.username_text.show()
     self.username_text.setText('')
     self.password_label.show()
     self.password_text.show()
     self.password_text.setText('')
     self.login_button.show()
     self.register_button.show()
     self.game1_button.hide()
     self.game2_button.hide()
     self.game3_button.hide()
     self.game4_button.hide()
     self.logout_button.hide()
     self.update_login_page_messages()
     self.delete_button.hide()
     self.welcome_label.hide()
     self.tokens_label.hide()
     self.loan_button.hide()

    def get_user_tokens(self):
        with open('tokens.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        username, tokens = parts
                        if username == self.username:
                            return int(tokens)
        return 0

    
    def update_tokens_display(self):
        with open('tokens.txt', 'r') as file:
            lines = file.readlines()
    
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    username, tokens = parts
                    if username == self.username:
                        self.tokens_label.setText(f'Tokens: {tokens}')
                        break

        
    def subtract_tokens(self, amount):
     os.chmod('tokens.txt', 0o777)
     
     with open('tokens.txt', 'r') as file:
        lines = file.readlines()

     for i, line in enumerate(lines):
        username, tokens = line.strip().split(':')
        if username == self.username:
            tokens = int(tokens) - amount
            lines[i] = f'{username}:{tokens}\n'
            break

     with open('tokens.txt', 'w') as file:
        file.writelines(lines)

     os.chmod('tokens.txt', 0o444)

    # Update the tokens display on the GUI
     self.update_tokens_display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont('Verdana', 12)
    app.setFont(font)
    game_app = GameApp()
    game_app.show()
    sys.exit(app.exec_())
