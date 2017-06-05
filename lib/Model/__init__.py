import pymysql.cursors
import logging


class __DBLoggerManager:

    def __init__(self):
        # Set Database Issues Logging
        self.__db_issues_logger = logging.Logger(name="Database Issues")
        self.__db_issues_logger.setLevel(logging.CRITICAL)
        self.__issues_handler = logging.FileHandler("Database Errors.log")
        self.__issues_handler.setLevel(logging.CRITICAL)
        self.__db_issues_logger.addHandler(self.issues_handler)

        # Set Database Queries Logging
        self.__db_queries_logger = logging.Logger(name="Database Queries")
        self.__db_queries_logger.setLevel(logging.INFO)
        self.__queries_handler = logging.FileHandler("Database Queries.log")
        self.__queries_handler.setLevel(logging.INFO)
        self.__db_queries_logger.addHandler(self.queries_handler)

    def getIssuesLogger(self):
        return self.__db_issues_logger

    def getQueriesLogger(self):
        return self.__db_queries_logger


class Database:

    def __init__(self, conn_cred):
        self.connection_cred = conn_cred
        self.loggerManager = DBLoggerManager()
        self.issues_logger = self.loggerManager.getIssuesLogger()
        self.queries_logger = self.loggerManager.getQueriesLogger()

        try:
            self.connection = pymysql.connect(
                host=self.connection_cred['host'],
                user=self.connection_cred['user'],
                password=self.connection_cred['password'],
                db=self.connection_cred['db'],
                charset=self.connection_cred['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            self.issues_logger.log(
                "Connection failed. Info: \n{0}".format(e.message)
            )

    def insert(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
            self.queries_logger.log("Queried OK")
        except Exception as e:
            self.issues_logger.log(
                "Insertion failed. Info: \n{0}".format(e.message)
            )

    def query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            self.queries_logger.log("Queried OK")
            return result
        except Exception as e:
            self.issues_logger.log(
                "Queried failed. Info: \n{0}".format(e.message)
            )

