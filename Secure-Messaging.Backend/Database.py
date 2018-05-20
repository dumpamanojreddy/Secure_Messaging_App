import shelve
import sys


class Database:
    DATABASE_FILE = 'database.db'

    database = None

    @staticmethod
    def close():
        Database.database.close()

    @staticmethod
    def initDB():
        global database
        if Database.database == None:
            print "Initializing database..."
            try:
                Database.database = shelve.open(Database.DATABASE_FILE, writeback=True)
            except Exception as e:
                print >> sys.stderr, str(e)

    @staticmethod
    def add(table, object):
        try:
            Database.database[table] = object
        except Exception as e:
            print >> sys.stderr, str(e)

    @staticmethod
    def get(table):
        try:
            if table in Database.database:
                return Database.database[table]
            else:
                return None
        except Exception as e:
            print >> sys.stderr, str(e)

