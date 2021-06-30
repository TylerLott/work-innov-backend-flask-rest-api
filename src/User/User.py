"""
User class for authentication
"""


class User:
    """Holder of login information"""

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def get_username(self):
        """Getter"""
        return self._username

    def get_password(self):
        """Getter"""
        return self._password

    def set_username(self, new_username):
        """Setter"""
        self._username = new_username

    def set_password(self, new_password):
        """Setter"""
        self._password = new_password
