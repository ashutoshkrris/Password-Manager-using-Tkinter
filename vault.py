from tkinter import simpledialog
from database import init_database


class VaultMethods:

    def __init__(self):
        self.db, self.cursor = init_database()

    def popup_entry(self, heading):
        answer = simpledialog.askstring("Enter details", heading)
        return answer

    def add_password(self, vault_screen):
        platform = self.popup_entry("Platform")
        userid = self.popup_entry("Username/Email")
        password = self.popup_entry("Password")

        insert_cmd = """INSERT INTO vault(platform, userid, password) VALUES (?, ?, ?)"""
        self.cursor.execute(insert_cmd, (platform, userid, password))
        self.db.commit()
        vault_screen()

    def update_password(self, id, vault_screen):
        password = self.popup_entry("Enter New Password")
        self.cursor.execute(
            "UPDATE vault SET password = ? WHERE id = ?", (password, id))
        self.db.commit()
        vault_screen()

    def remove_password(self, id, vault_screen):
        self.cursor.execute("DELETE FROM vault WHERE id = ?", (id,))
        self.db.commit()
        vault_screen()
