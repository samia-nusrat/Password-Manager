import sqlite3, hashlib
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from functools import partial

#Database
with sqlite3.connect("Password_DB.db") as db:
    cursor = db.cursor() #an object which helps to execute the query and fetch the records from the database.

#Creating table for storing Master password for the passwrodDB
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL
)
""")

#table to store your Website, Username, Password
cursor.execute("""
CREATE TABLE IF NOT EXISTS storage(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL
)
""")

#Creating Pop-UP
def popUp(text):
    answer = simpledialog.askstring("input string", text)
    #print(answer)
    return answer



#initiating Window
window = Tk()

window.title("Password Manager")

#hashing Password
def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    return hash


#Initial Screen Where you set your master password
def firstScreen():
    window.geometry("350x150")
    window.config(bg="#FFD36E")
    #window.overrideredirect(True)

    lable = Label(window, text="Create Your Password", bg="#FFD36E", font="Corbel", fg="#9FB4FF")
    lable.config(anchor=CENTER)
    lable.pack()

    txt = Entry(window, width=25, show="*") #shows stars ('*') in the place of plain text
    txt.pack()
    txt.focus()

    lable1 = Label(window, text="Re-Enter Your Password",bg="#FFD36E", font="Corbel", fg="#9FB4FF")
    lable1.pack()

    txt1 = Entry(window, width=25, show="*")
    txt1.pack()

    lable2 = Label(window, text="", bg="#FFD36E")
    lable2.pack()

    #Saving Password into masterpassword Table
    def savePassword():
        if txt.get() == txt1.get():
            hashedPassword = hashPassword(txt.get().encode('utf-8'))  #hashing the password for better security
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()
            passwordManager()

        else:
            lable2.config(text="Passwords don't match", fg="red")


    btn = Button(window, text="Save", command=savePassword, bg="#FFF56D", font="Corbel", fg="#9FB4FF")
    btn.pack(pady=5)

#This is the screen Shown after you have already created your master password
def loginScreen():
    window.geometry("350x150")
    window.config(bg="#FFD36E")
    lable=Label(window, text="Enter Your Password", bg="#FFD36E", font="Corbel", fg="#9FB4FF")
    lable.config(anchor=CENTER)
    lable.pack()

    txt= Entry(window, width=25, show="*")
    txt.pack()
    txt.focus()

    lable1 = Label(window, bg="#FFD36E", font="Corbel", fg="red")
    lable1.pack()

    #gets the hashed master password
    def getRootPassword():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    #checks the hashed password against the entered hashed password
    def checkPassword():
        check = getRootPassword()

        if check:
            passwordManager()
        else:
            txt.delete(0, 'end')
            lable1.config(text="wrong password")

    btn = Button(window, text="Login", command=checkPassword, bg="#FFF56D" , font="Corbel", fg="#9FB4FF")
    btn.pack(pady=20)

#The stored password manager GUI
def passwordManager():
    #When we switch to the manager window we destroy the previous login information and window. So that It doesn't stack
    for widget in window.winfo_children():
        widget.destroy()


    def addEntry():
        msg1 = "Website"
        msg2 = "Username"
        msg3 = "Password"

        website = popUp(msg1)
        username = popUp(msg2)
        password = popUp(msg3)

        #SQL command for storing the information
        insert_fields = """INSERT INTO storage(website,username,password)
        VALUES(?,?,?)"""

        #executes the sql commands
        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        #Recalling the passwordManager method for refreshing the current GUI
        passwordManager()

    def removeEntry(input):
        cursor.execute("DELETE FROM storage WHERE id = ?", (input, ))
        db.commit()

        # Recalling the passwordManager method for refreshing the current GUI
        passwordManager()


    window.geometry("870x720")

    lable= Label(window, text="Password Manager" , bg="#FFD36E", font=("Gabriola",30), fg="#9FB4FF")
    lable.grid(column=1)

    btn = Button(window, text="Add Entry", command=addEntry, bg="#00FF00")
    btn.grid(column=1, pady=20)

    def updatePassword():
        text="Enter Your new Password"
        newPassword = popUp(text)
        hashedPassword = hashPassword(newPassword.encode('utf-8'))
        cursor.execute("DELETE FROM masterpassword WHERE id = 1" )
        db.commit()
        insert_password = """INSERT INTO masterpassword(password)
                    VALUES(?)"""
        cursor.execute(insert_password, [(hashedPassword)])
        db.commit()
        passwordManager()



    btn2 = Button(window, text="Change Master Password", command=updatePassword , bg="#FFF56D")
    btn2.grid(row=1, column= 2)


    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0,padx=100)
    lbl.config(bg="#FFD36E")
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=100)
    lbl.config(bg="#FFD36E")
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2,padx=100)
    lbl.config(bg="#FFD36E")


    cursor.execute("SELECT * FROM storage") #using this to make sure the correct database is used
    if(cursor.fetchall() != None):
        i = 0
        while True:

            cursor.execute("SELECT * FROM storage")
            if (len(cursor.fetchall()) <= i):
                break

            cursor.execute("SELECT * FROM storage")
            array = cursor.fetchall()
            #dumping the array values to make it look like a table
            lable1 = Label(window, text=(array[i][1]), bg="#FFD36E", font="Tahoma", fg="blue")
            lable1.grid(column=0, row = i+3)
            lable2 = Label(window, text=(array[i][2]), bg="#FFD36E", font="Tahoma", fg="blue")
            lable2.grid(column=1, row=i + 3)
            lable3 = Label(window, text=(array[i][3]), bg="#FFD36E", font="Tahoma", fg="blue")
            lable3.grid(column=2, row=i + 3)

            btn = Button(window, text="Delete", command=partial(removeEntry, array[i][0]), bg="#FF0000") #deletes the ID from DB
            btn.grid(column=3, row=i+3, pady=20)

            i+=1


cursor.execute("SELECT * FROM masterpassword")

#if it's null we go to firstScreen to create the password
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()

#looping as long as the application is not closed
window.mainloop()