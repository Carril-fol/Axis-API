class EmailInvalidFormat(Exception):
    def __init__(self):
        super().__init__("The email format is invalid.")
        

class PasswordDontMatch(Exception):
    def __init__(self):
        super().__init__("Passwords do not match.")


class InvalidCredentials(Exception):
    def __init__(self):
        super().__init__("Invalid credentials.")
        

class UserNotFound(Exception):
    def __init__(self):
        super().__init__("User not found.")