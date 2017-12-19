import pymysql.cursors
import logging
from pymongo import mongo_client
import datetime


class DBLoggerManager:

    def __init__(self):
        # Set Database Issues Logging
        self.__db_issues_logger = logging.Logger(name="Database Issues")
        self.__db_issues_logger.setLevel(logging.CRITICAL)
        self.__issues_handler = logging.FileHandler("logs/Database Errors.log")
        self.__issues_handler.setLevel(logging.CRITICAL)
        self.__db_issues_logger.addHandler(self.__issues_handler)

        # Set Database Queries Logging
        self.__db_queries_logger = logging.Logger(name="Database Queries")
        self.__db_queries_logger.setLevel(logging.INFO)
        self.__queries_handler = logging.FileHandler("logs/Database Queries.log")
        self.__queries_handler.setLevel(logging.INFO)
        self.__db_queries_logger.addHandler(self.__queries_handler)

    def getIssuesLogger(self):
        return self.__db_issues_logger

    def getQueriesLogger(self):
        return self.__db_queries_logger


class EmailLogManager:
    def __init__(self):
        # Set Email Logging
        self.__email_logger = logging.Logger(name="Email Logs")
        self.__email_logger.setLevel(logging.INFO)
        self.__email_handler = logging.FileHandler("logs/Email Transactions.log")
        self.__email_handler.setLevel(logging.INFO)
        self.__email_logger.addHandler(self.__email_handler)

    def getEmailLogger(self):
        return self.__email_logger


class mongoDatabase:
    """Under Construction until basic fundamentals of MongoDB are covered."""

    def __init__(self, conn_cred):
        """
        Spins up the MongoDB Cluster with the credentials needed
        @:conn_cred, an XML parsed object containing necessary attributes
        """
        self.loggerManager = DBLoggerManager()
        self.issues_logger = self.loggerManager.getIssuesLogger()
        self.queries_logger = self.loggerManager.getQueriesLogger()

        try:
            self.client = mongo_client.MongoClient(conn_cred)
            self.queries_logger.log(
                logging.INFO, "Connected!"
            )
            print("Connected")
        except mongo_client.InvalidURI as e:
            self.issues_logger.log(
                logging.CRITICAL, "Connection failed. Info {0}".format(e.message)
            )



class SQLDatabase:

    def __init__(self, conn_cred):
        self.connection_cred = conn_cred
        self.loggerManager = DBLoggerManager()
        self.issues_logger = self.loggerManager.getIssuesLogger()
        self.queries_logger = self.loggerManager.getQueriesLogger()

        try:
            self.connection = pymysql.connect(
                host=self.connection_cred['cred']['db_cred']['host'],
                user=self.connection_cred['cred']['db_cred']['user'],
                password=self.connection_cred['cred']['db_cred']['password'],
                db=self.connection_cred['cred']['db_cred']['db'],
                charset=self.connection_cred['cred']['db_cred']['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            self.queries_logger.log(
                logging.INFO, "Connected!"
            )

        except Exception as e:
            self.issues_logger.log(
                logging.CRITICAL, "Connection failed. Info: \n{0}".format(e.message)
            )

    def insert(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
            self.queries_logger.log(
                logging.INFO, "Queried OK")
            return True
        except Exception as e:
            self.issues_logger.log(
                logging.CRITICAL, "Insertion failed. Info: \n{0}".format(e.message)
            )
            return False

    def query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            self.queries_logger.log(
                logging.INFO, "Queried OK")
            return result
        except Exception as e:
            self.issues_logger.log(
                logging.CRITICAL, "Queried failed. Info: \n{0}".format(e.message)
            )

    def __del__(self):
        self.connection.close()

