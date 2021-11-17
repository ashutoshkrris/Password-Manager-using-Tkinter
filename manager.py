import hashlib
from tkinter.constants import BOTH, CENTER, END, LEFT, RIGHT, VERTICAL, Y
from generator import PasswordGenerator
from database import init_database
from tkinter import Button, Canvas, Entry, Frame, Label, Scrollbar, Tk
from functools import partial
from vault import VaultMethods


class PasswordManager:

    def __init__(self):
        self.db, self.cursor = init_database()
        self.window = Tk()
        self.window.update()
        self.window.title("Password Manager")
        self.window.geometry("650x350")

    def welcome_new_user(self):
        self.window.geometry("450x200")

        label1 = Label(self.window, text="Create New Master Password")
        label1.config(anchor=CENTER)
        label1.pack(pady=10)

        mp_entry_box = Entry(self.window, width=20, show="*")
        mp_entry_box.pack()
        mp_entry_box.focus()

        label2 = Label(self.window, text="Enter the password again")
        label2.config(anchor=CENTER)
        label2.pack(pady=10)

        rmp_entry_box = Entry(self.window, width=20, show="*")
        rmp_entry_box.pack()

        self.feedback = Label(self.window)
        self.feedback.pack()

        save_btn = Button(self.window, text="Create Password",
                          command=partial(self.save_master_password, mp_entry_box, rmp_entry_box))
        save_btn.pack(pady=5)

    def login_user(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.geometry("450x200")

        label1 = Label(self.window, text="Enter your master password")
        label1.config(anchor=CENTER)
        label1.place(x=150, y=50)

        self.password_entry_box = Entry(self.window, width=20, show="*")
        self.password_entry_box.place(x=160, y=80)
        self.password_entry_box.focus()

        self.feedback = Label(self.window)
        self.feedback.place(x=170, y=105)

        login_btn = Button(self.window, text="Log In", command=partial(
            self.check_master_password, self.password_entry_box))
        login_btn.place(x=200, y=130)

    def save_master_password(self, eb1, eb2):
        password1 = eb1.get()
        password2 = eb2.get()
        if password1 == password2:
            hashed_password = self.encrypt_password(password1)
            insert_command = """INSERT INTO master(password)
            VALUES(?) """
            self.cursor.execute(insert_command, [hashed_password])
            self.db.commit()
            self.login_user()
        else:
            self.feedback.config(text="Passwords do not match", fg="red")

    def check_master_password(self, eb):
        hashed_password = self.encrypt_password(eb.get())
        self.cursor.execute(
            "SELECT * FROM master WHERE id = 1 AND password = ?", [hashed_password])
        if self.cursor.fetchall():
            self.password_vault_screen()
        else:
            self.password_entry_box.delete(0, END)
            self.feedback.config(text="Incorrect password", fg="red")

    def password_vault_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        vault_methods = VaultMethods()

        self.window.geometry("850x350")
        main_frame = Frame(self.window)
        main_frame.pack(fill=BOTH, expand=1)

        main_canvas = Canvas(main_frame)
        main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        main_scrollbar = Scrollbar(
            main_frame, orient=VERTICAL, command=main_canvas.yview)
        main_scrollbar.pack(side=RIGHT, fill=Y)

        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(
            scrollregion=main_canvas.bbox("all")))

        second_frame = Frame(main_canvas)
        main_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        generate_password_btn = Button(second_frame, text="Generate Password",
                                       command=PasswordGenerator)
        generate_password_btn.grid(row=1, column=2, pady=10)

        add_password_btn = Button(
            second_frame, text="Add New Password", command=partial(vault_methods.add_password, self.password_vault_screen))
        add_password_btn.grid(row=1, column=3, pady=10)

        lbl = Label(second_frame, text="Platform")
        lbl.grid(row=2, column=0, padx=40, pady=10)
        lbl = Label(second_frame, text="Email/Username")
        lbl.grid(row=2, column=1, padx=40, pady=10)
        lbl = Label(second_frame, text="Password")
        lbl.grid(row=2, column=2, padx=40, pady=10)

        self.cursor.execute("SELECT * FROM vault")

        if self.cursor.fetchall():
            i = 0
            while True:
                self.cursor.execute("SELECT * FROM vault")
                array = self.cursor.fetchall()

                platform_label = Label(second_frame, text=(array[i][1]))
                platform_label.grid(column=0, row=i + 3)

                account_label = Label(second_frame, text=(array[i][2]))
                account_label.grid(column=1, row=i + 3)

                password_label = Label(second_frame, text=(array[i][3]))
                password_label.grid(column=2, row=i + 3)

                copy_btn = Button(second_frame, text="Copy Password",
                                  command=partial(self.copy_text, array[i][3]))
                copy_btn.grid(column=3, row=i + 3, pady=10, padx=10)
                update_btn = Button(second_frame, text="Update Password",
                                    command=partial(vault_methods.update_password, array[i][0], self.password_vault_screen))
                update_btn.grid(column=4, row=i + 3, pady=10, padx=10)
                remove_btn = Button(second_frame, text="Delete Password",
                                    command=partial(vault_methods.remove_password, array[i][0], self.password_vault_screen))
                remove_btn.grid(column=5, row=i + 3, pady=10, padx=10)

                i += 1

                self.cursor.execute("SELECT * FROM vault")
                if len(self.cursor.fetchall()) <= i:
                    break

    def encrypt_password(self, password):
        password = password.encode("utf-8")
        encoded_text = hashlib.md5(password).hexdigest()
        return encoded_text

    def copy_text(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)


if __name__ == '__main__':
    db, cursor = init_database()
    cursor.execute("SELECT * FROM master")
    manager = PasswordManager()
    if cursor.fetchall():
        manager.login_user()
    else:
        manager.welcome_new_user()
    manager.window.mainloop()
