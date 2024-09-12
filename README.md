# Password-Manager

A simple and secure password manager application developed using Python with Tkinter and SQLite. This application helps users manage their passwords securely by storing them in an encrypted format. The user sets a master password to access the password manager, which is used to hash and secure all other passwords.

## Features

- **Master Password Protection**: Set and update a master password to secure access to the password manager.
- **Password Storage**: Add, view, and delete password entries associated with various websites and usernames.
- **Database Integration**: Uses SQLite to store passwords securely.
- **Graphical User Interface (GUI)**: Built with Tkinter to provide a user-friendly interface.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/samia-nusrat/password-manager.git
2. Navigate to the project directory: cd password-manager

3. Install the required packages:
This project uses Python's built-in libraries, so no additional packages are required. Ensure you have Python installed on your system.

4. Run the application:
python password_manager.py

Usage: 
Initial Setup: On first launch, create a master password. Re-enter the password to confirm and save it.
Login: Enter your master password to access the password manager.
Manage Passwords: Add, update, and delete password entries through the intuitive GUI.
Code Overview
password_manager.py: The main Python script containing all functionalities of the application, including database setup, GUI design, and password management logic.
Security
Passwords are hashed using MD5 before being stored in the database to enhance security.
