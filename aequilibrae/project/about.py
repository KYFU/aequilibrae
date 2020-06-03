from os.path import join, dirname, realpath
import sqlite3
import string
from warnings import warn
import uuid
from aequilibrae.project.project_creation import run_queries_from_sql_file
from aequilibrae.paths import release_version


class About:
    """Provides an interface for querying and editing the **about** table of an AequilibraE project
        ::

            p = Project()
            p.open('my/project/folder')
            about = p.about


    """

    def __init__(self, conn: sqlite3.Connection):
        self.__characteristics = []
        self.__conn = conn
        if self.__has_about():
            self.__load()

    def create(self):
        """Creates the 'about' table for project files that did not previously contain it"""

        if not self.__has_about():
            qry_file = join(dirname(realpath(__file__)), 'database_specification', 'tables', 'about.sql')
            run_queries_from_sql_file(self.__conn, qry_file)

        cursor = self.__conn.cursor()
        cursor.execute('select infovalue from about where infoname="aequilibrae_version"')

        if cursor.fetchone()[0] is None:
            cursor.execute(f"UPDATE 'about' set infovalue='{release_version}' where infoname='aequilibrae_version'")
            cursor.execute(f"UPDATE 'about' set infovalue='{uuid.uuid4().hex}' where infoname='project_ID'")
            self.__conn.commit()

            self.__load()
        else:
            warn('About table already exists. Nothing was done', Warning)

    def list_fields(self) -> list:
        """Returns a list of all characteristics the about table holds"""
        return [x for x in self.__characteristics]

    def add_info_field(self, info_field: str) -> None:
        """Adds new information field to the model

            Args:
                *info_field* (:obj:`str`): Name of the desired information field to be added.  Has to be a valid
                Python VARIABLE name (i.e. letter as first character, no spaces and no special characters)

            ::

                p = Project()
                p.open('my/project/folder')
                p.about.add_info_field('my_super_relevant_field')
                p.about.my_super_relevant_field = 'super relevant information'
                p.about.write_back()
        """
        passed = True
        for x in info_field:
            if x not in string.ascii_lowercase + '_':
                passed = False

        if passed:
            sql = "INSERT INTO 'about' (infoname) VALUES(?)"
            curr = self.__conn.cursor()
            curr.execute(sql, [info_field])
            self.__conn.commit()
            self.__characteristics.append(info_field)
        else:
            raise ValueError(f'{info_field} is not valid as a metadata field. Should be a lower case ascii letter or _')

    def write_back(self):
        """Saves the information parameters back to the project database

            ::

                p = Project()
                p.open('my/project/folder')
                p.about.description = 'This is the example project. Do not use for forecast'
                p.about.write_back()
        """
        curr = self.__conn.cursor()
        for k in self.__characteristics:
            v = self.__dict__[k]
            curr.execute(f"UPDATE 'about' set infovalue = '{v}' where infoname='{k}'")
        self.__conn.commit()

    def __has_about(self):
        curr = self.__conn.cursor()
        curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if 'about' in [x[0] for x in curr.fetchall()]:
            return True
        return False

    def __load(self):
        self.__characteristics = []
        curr = self.__conn.cursor()
        curr.execute("select infoname, infovalue from 'about'")

        for x in curr.fetchall():
            self.__characteristics.append(x[0])
            self.__dict__[x[0]] = x[1]
