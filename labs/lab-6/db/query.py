"""query.py: leverages SQLAlchemy to create generic queries for interacting with the postgres DB"""
from db.server import get_session
from sqlalchemy import select

def get_all(table) -> list:
    """Select all records from a DB table using SQLAlchemy ORM.

        args: 
            table (object): db table

        returns:
            records (list[obj]): list of records from db table
    """
    session = get_session()
    try:
        # get all records in the table
        records = session.query(table).all()
        return records
    
    finally:
        session.close()

def insert(record) -> None:
    """Insert one record into a table

        args:
            record (object): record to insert into db

        returns:
            none
    """
    session = get_session()

    try:
        # insert one new record
        session.add(record)
        # "save" the changes
        session.commit()

    except Exception as e:
        session.rollback()
        print("Error inserting records:", e)
    
    finally:
        session.close()

def get_user_by_email(table, email) -> object:
    """Select a user record from a DB table by email using SQLAlchemy ORM.

        args: 
            table (object): db table
            email (str): email of user to retrieve
        returns:
            record (obj): user record from db table
    """
    session = get_session()
    try:
        # get user record by email
        record = session.execute(select(table).where(table.Email == email)).scalar_one_or_none()
        return record
    
    finally:
        session.close()