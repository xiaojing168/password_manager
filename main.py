from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    #Every time gerenate a password, can paste without copy
    pyperclip.copy(password)

# ----------------------------Menu Functions------------------------------- #

def format_data(new_window):
    pass_buttons = []
    passwords = []
    emails = []
    websites = []
    web_y = 30
    em_y = 30
    pas_y = 30
    pass_btn_width = 0
    try:
        with open("data.json") as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError or FileNotFoundError:
        if_no = Label(new_window, text="No Saved Data or Passwords found\nAdd Passwords to view them.", bg="light blue")
        if_no.place(x=110, y=90)
    else:
        for website in data:
            websites.append(website)
            emails.append(data[website]["email"])
            passwords.append(data[website]["password"])
        for passw in passwords:
            if len(passw) > pass_btn_width:
                pass_btn_width = len(passw)
        for website in websites:
            websites_label = Label(new_window, text=website, bg="light blue")
            websites_label.place(x=10, y=web_y)
            web_y += 30
        for email in emails:
            emails_label = Label(new_window, text=email, bg="light blue")
            emails_label.place(x=150, y=em_y)
            em_y += 30

        def copy_pass(password_to_copy):
            pyperclip.copy(password_to_copy)

        for password in passwords:
            pas_button = Button(new_window, text=password, height=1, width=pass_btn_width, bg="light blue")
            pas_button.config(command=lambda password_arg=pas_button: copy_pass(password_arg.cget('text')))
            pas_button.place(x=350, y=pas_y)
            pas_y += 30
            pass_buttons.append(pas_button)

    new_window.mainloop()


def view_saved():
    new_window = Tk()
    new_window.geometry("")
    new_window.config(padx=20, pady=2, bg="light blue")
    new_window.title("Saved Passwords")
    web_label = Label(new_window, text="Website", fg="red", font=("aerial", 10, "bold"), bg="light blue")
    web_label.place(x=10, y=10)
    email_user_label = Label(new_window, text="Email/Username", fg="red", font=("aerial", 10, "bold"), bg="light blue")
    email_user_label.place(x=150, y=10)
    pas_label = Label(new_window, text="Password", fg="red", font=("aerial", 10, "bold"), bg="light blue")
    pas_label.place(x=350, y=10)
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    format_data(new_window)
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data
        }
    }

    if website_data == "" or password_data == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
        view_saved()
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(title="Oops", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Oops", message="No detail for this website.")






# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#labels
website = Label(text="website:")
website.grid(column=0, row=1)
email = Label(text="Email/Username:")
email.grid(column=0, row=2)
password = Label(text="Password:")
password.grid(column=0, row=3)

#entries
#Use Sticky "EW" for neat alignments to column edges without pixel adjustment experimentation
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "8redfish168@gmail.com")
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

#buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")
generate_ps_button = Button(text="Generate Password", command=generate_password)
generate_ps_button.grid(column=2, row=3, sticky="EW")
add_button = Button(text="Add", command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")


window.mainloop()