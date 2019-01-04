from TAServer.models import Staff as User
from Managers.userManager import UserManager as UM


class AuthManager:
    def __init__(self, usermgr: UM):
        pass

    def login(self, username: str, password: str)->User:
        pass

    def logout(self, u: User) -> str:
        pass

    def validate(self, command: str) -> bool:
        pass