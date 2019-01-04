from Managers.myStorageManager import AbstractStorageManager


class ManagerInterface:
    def __init__(self, database: AbstractStorageManager):
        pass

    def add(self, fields: dict)->bool:
        pass

    def view(self, fields: dict)->str:
        pass

    def edit(self, fields: dict)->bool:
        pass

    def delete(self, fields: dict)->bool:
        pass

    @staticmethod
    def reqFields()->list:
        pass

    @staticmethod
    def optFields()->list:
        pass
