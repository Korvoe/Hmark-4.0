from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.getConfig import getConfig

# Get config data & Set sql_url
config = getConfig()

sql_url     = 'mysql://' + config.dbuser + ':' + config.dbpw + \
'@' + config.dbhost + ':' + config.dbport + '/' + config.dbname + '?charset=' + config.dbcharset
engine = create_engine(sql_url, convert_unicode=False)

metadata    = MetaData(engine)

if not engine.dialect.has_table(engine, 'progress_queue'):
    Table('progress_queue', metadata,
          Column('cve', VARCHAR(25), nullable=False),
          Column('commit', VARCHAR(60), nullable=False),
          Column('crawlType', VARCHAR(255), nullable=False),
          Column('vendor', VARCHAR(255), nullable=False),
          Column('product', VARCHAR(255), nullable=False)
          )

# Create cve_cpe if not exist
if not engine.dialect.has_table(engine, 'cve_cpe'):
    Table('cve_cpe', metadata,
          Column('vendor', VARCHAR(255), nullable=False),
          Column('product', VARCHAR(255), nullable=False),
          Column('version', LONGTEXT),
          Column('cve', VARCHAR(25), nullable=False)
          )

# Create cve_url if not exist
if not engine.dialect.has_table(engine, 'cve_url'):
    Table('cve_url', metadata,
          Column('cve', VARCHAR(25), nullable=False),
          Column('url', VARCHAR(500), nullable=False),
          Column('name', VARCHAR(500), nullable=False),
          Column('refsource', VARCHAR(255), nullable=False),
          Column('tags', VARCHAR(255), nullable=False)
          )

# Create cve_url if not exist
if not engine.dialect.has_table(engine, 'cve_data'):
    Table('cve_data', metadata,
          Column('cve', VARCHAR(25), nullable=False),
          Column('cvssV2', VARCHAR(10), nullable=True),
          Column('cvssV3', VARCHAR(10), nullable=True),
          Column('cwe', VARCHAR(300), nullable=True)
          )

metadata.create_all()

# Maintain Session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(engine)


'''import sqlalchemy
from sqlalchemy import (
    Table,
    Column
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import VARCHAR, LONGTEXT
import json
import os
import configparser

class dbInit:
    def __init__(self):
        # Get config data & Set sql_url
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config.ini')
        db_config = config['DATABASE']

        sql_url = 'mysql://' + db_config['username'] + ':' + db_config['password'] + '@' + db_config['host'] + \
                ':' + db_config['port'] + '/' + db_config['db_name'] + '?charset=' + db_config['charset']

        self.engine = sqlalchemy.create_engine(sql_url, convert_unicode=False)

        self.metadata = sqlalchemy.MetaData(self.engine)

        # Create cve_cpe if not exist
        if not self.engine.dialect.has_table(self.engine, 'cve_cpe'):
            Table('cve_cpe', self.metadata,
                Column('vendor', VARCHAR(255), nullable=False),
                Column('product', VARCHAR(255), nullable=False),
                Column('version', LONGTEXT),
                Column('cve', VARCHAR(25), nullable=False)
                )

        # Create cve_url if not exist
        if not self.engine.dialect.has_table(self.engine, 'cve_url'):
            Table('cve_url', self.metadata,
                Column('cve', VARCHAR(25), nullable=False),
                Column('url', VARCHAR(500), nullable=False),
                Column('name', VARCHAR(500), nullable=False),
                Column('refsource', VARCHAR(255), nullable=False),
                Column('tags', VARCHAR(255), nullable=False)
                )

        # Create cve_url if not exist
        if not self.engine.dialect.has_table(self.engine, 'cve_data'):
            Table('cve_data', self.metadata,
                Column('cve', VARCHAR(25), nullable=False),
                Column('cvssV2', VARCHAR(10), nullable=True),
                Column('cvssV3', VARCHAR(10), nullable=True),
                Column('cwe', VARCHAR(25), nullable=True)
                )
        self.metadata.create_all()

    def getDBSession(self):
        # Maintain Session
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        Base = declarative_base()
        Base.query = db_session.query_property()

        return db_session

def main():
    print(os.path.abspath(os.path.dirname(__file__)))
    print(os.path.abspath(__file__))
    db = dbInit()
    db.getDBSession()


if __name__ == "__main__":
    main()
'''