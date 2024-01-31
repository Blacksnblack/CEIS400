from GUI import GUI

U, P = "test", "123"  # placeholder user and password

class Manager:
    def __init__(self) -> None:
        self.window = GUI(self)
        self.window.mainloop()

        

    def check_password(self, user: str, pwd: str) -> bool:
        if len(user) == 0 or len(pwd) == 0:
            return False
        print(f"Login Attempt:: User: {user}, Pass: {pwd}") # for debug purposes

        # TODO: check if valid login creds
        if user == U and pwd == P:
            self.window.main_frame()


        return False # placeholder return value