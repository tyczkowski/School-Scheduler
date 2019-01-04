from abc import ABC, abstractmethod
from TAServer.models import Staff as User, Course, Section


class AbstractStorageManager(ABC):

    # ################################################################################# #
    # List of functional storage methods to be implemented by a data system             #
    # ################################################################################# #

    @staticmethod
    @abstractmethod
    def set_up(overwrite: bool = False)->bool: pass
    # NOTE: WILL WIPE ALL DATA and  IF YOU SET OVERWRITE TO TRUE
    # Sets up storage. JSON, Database, whatever. Also creates one user: username=supervisor password=1234 role=supervisor
    # Returns true on successful setup false otherwise

    @staticmethod
    @abstractmethod
    def insert_course(self, course: Course)->bool: pass
    # Inserts a Course to the course list, overwriting if it exists.
    # Does not validate data! Simply makes sure it has received a course object then inserts it to the database.
    # Returns True if Course existed and was overwritten.

    @staticmethod
    @abstractmethod
    def insert_user(user: User)->bool: pass
    # Inserts a User to the user list, overwriting if it exists. Does not error check for valid data!
    # Does not validate data! Simply makes sure it has received a user object then inserts it to the database.
    # Returns True if User existed and was overwritten.

    @staticmethod
    @abstractmethod
    def insert_section(section: Section)->bool: pass
    # Inserts a Section to the user list, overwriting if it exists. Does not error check for valid data!
    # Does not validate data! Simply makes sure it has received a section object then inserts it to the database.
    # Returns True if Section existed and was overwritten.

    @staticmethod
    @abstractmethod
    def get_course(dept, cnum)->Course: pass
    # Builds a Course model that has this dept and cnum (plus other data from database) and returns it. None if no entry matches.

    @staticmethod
    @abstractmethod
    def get_courses_by(dept, cnum)->[Course]: pass
    # Returns a list of Course models that match dept if cnum is not specified. If dept and cnum are both blank, returns all courses as a list.

    @staticmethod
    @abstractmethod
    def get_user(username)->User: pass
    # Returns a User model that has this username (plus other data from database) and returns it. None if no entry matches

    @staticmethod
    @abstractmethod
    def get_users_by(role)->[User]: pass
    # Returns a list of all User models in the database. Empty list if no matches.
    # NAMES GET_USERS_BY VS GET_ALL_USERS BECAUSE WE MAY WANT TO GET ALL USERS VIA MORE FIELDS LATER

    @staticmethod
    @abstractmethod
    def get_section(dept, cnum, snum)->Section: pass
    # Builds a Section model that has this dept, cnum, and snum (plus other data from database) and returns it. None if no entry matches

    @staticmethod
    @abstractmethod
    def get_sections_by(dept, cnum, snum)->[Section]: pass
    # Returns a list of all Section models in the database. Empty list if no matches.

    @staticmethod
    @abstractmethod
    def delete(to_delete)->bool: pass
    # Deletes an object from the database.
    # Returns True if object existed and was deleted.
