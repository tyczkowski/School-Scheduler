# This is my idea for a potential manager interface. Each of the four main functions takes in a dictionary where each
# key value pair is a field and it's value. Each dict must have a non None value for each key returned by reqFields()
# and optFields() just returns optional fields (mainly for correct spelling and capitalization). This is not meant for
# auth manager or databse manager, just course, section, and user.
from Managers.myStorageManager import AbstractStorageManager as StorageManager
from abc import ABC, abstractmethod


class ManagerInterface(ABC):

    @abstractmethod
    def __init__(self, database: StorageManager): pass

    @abstractmethod
    def add(self, fields: dict) -> (bool, str): pass

    @abstractmethod
    def view(self, fields: dict) -> [dict]: pass

    @abstractmethod
    def edit(self, fields: dict) -> (bool, str): pass

    @abstractmethod
    def delete(self, fields: dict) -> (bool, str): pass

    @staticmethod
    def reqFields(self) -> list: pass

    @staticmethod
    def optFields(self) -> list: pass
