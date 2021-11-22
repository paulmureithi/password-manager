from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json

my_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890~@!#$%&*+/()-_=?,.'


# ------------------------------Save Password-------------------------------#
def password_generator():
    password = ""
    for i in range(10):
        password += random.choice(my_string)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ------------------------------Save Password-------------------------------#
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Missing Values", message=f"Please fill all fields.")
    else:
        is_ok = messagebox.showinfo(title="Save Info",
                                    message=f" Crosscheck your details:\n Website: {website}\n Email: {email} "
                                            f"\n Password: {password}")
        if is_ok:
            try:
                with open("password_db.json", mode="r") as file:
                    # read the existing data
                    new_data = json.load(file)

            except FileNotFoundError:
                with open("password_db.json", mode="w") as file:
                    # write new data to the json file
                    json.dump(data, file, indent=4)
            else:
                # update the data
                new_data.update(data)

                with open("password_db.json", mode="w") as file:
                    # write new data to the json file
                    json.dump(new_data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ------------------------------Search Password-------------------------------#
def find_password():
    search_term = website_entry.get()

    if len(search_term) > 0:
        try:
            with open('password_db.json', mode='r') as search:
                current_data = json.load(search)
        except FileNotFoundError:
            messagebox.showwarning(title="No Data Found", message=f"Database doesn't exist.")

        else:
            for k, v in current_data.items():
                if k == search_term:
                    messagebox.showinfo(title=f"{search_term}",
                                        message=f" Details:\n Website: {search_term}\n Email: {v['email']} "
                                                f"\n Password: {v['password']}")
                elif search_term not in current_data.keys():
                    messagebox.showwarning(title="No Data Found", message=f"{search_term} not in the records.")
                    break

    else:
        messagebox.showwarning(title="Empty Field", message=f"Please enter a name in the website field.")


# ------------------------------UI Setup-------------------------------#
window = Tk()
window.title("Password Manager")

# set minimum window size value
window.minsize(400, 300)

# set maximum window size value
window.maxsize(400, 300)

# create the canvas widget
canvas = Canvas(width=400, height=300)
bg_image = PhotoImage(file="password_bg.png")
canvas.create_image(200, 150, image=bg_image)
canvas.create_text(110, 180, text="Website:", fill='black', anchor=E)
canvas.create_text(110, 205, text="Email/Username:", fill='black', anchor=E)
canvas.create_text(110, 230, text="Password:", fill='black', anchor=E)

# entry boxes
website_entry = Entry(bd=0.5, relief='solid')
website_entry.focus()
website_entry.config(width=20)
website_entry_window = canvas.create_window(185, 180, window=website_entry)

email_entry = Entry(bd=0.5, relief='solid')
email_entry.insert(0, 'johndoe@gmail.com')
email_entry.config(width=35)
email_entry_window = canvas.create_window(230, 205, window=email_entry)

password_entry = Entry(bd=0.5, relief='solid')
password_entry.config(width=20)
password_entry_window = canvas.create_window(185, 230, window=password_entry)

# password generate button
password_generate = Button(text="Generate Password", bd=0.5, relief='solid', command=password_generator)
password_generate.config(width=15)
password_generate_window = canvas.create_window(315, 230, window=password_generate)

# password save button
password_save = Button(text="Save Password", bd=0.5, relief='solid', command=save)
password_save.config(width=12)
password_save_window = canvas.create_window(200, 280, window=password_save, anchor=CENTER)

# search button
password_search = Button(text="Search Password", bd=0.5, relief='solid', command=find_password)
password_search.config(width=15)
password_search_window = canvas.create_window(315, 180, window=password_search)

canvas.pack()

window.mainloop()
