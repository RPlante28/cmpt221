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

def get_record_by_field(table, field, field_value) -> list:
    """Get the full record associated with a field and its value

        args:
            table (object): db table
            field (object): field to get record by
            field_value (variable): value of the field to check
    
        returns:
            entire record as list
    """
    session = get_session()
    try:
        eval_field = eval(f"Users.{field}")
        record = session.query(table).filter(eval_field == field_value).scalar_one_or_none()
        if record:
            print("Record Found")
        else:
            print("Record not found")
    except Exception as e:
        session.rollback()
        print("Error finding record:", e)
    finally:
        return record
    
    return None