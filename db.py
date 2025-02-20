
import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path = "database.db"):
        self.db_path = db_path
        self.create_db()

    def open(self):
        conn_func = sqlite3.connect(self.db_path)
        curr_func = conn_func.cursor()
        print("The db connection is opened")
        return conn_func, curr_func


    def close(self, conn_func, curr_func):
        conn_func.commit()
        curr_func.close()
        conn_func.close()
        print("The db connection is closed")


    def create_db():

        conn, curr = self.open()
        curr.execute(
                'CREATE TABLE IF NOT EXISTS logging('
                 'id INTEGER PRIMARY KEY,'
                 'user_id INTEGER,'
                 'instrument_id INTEGER,'
                 'instrument_name TEXT,'
                 'rent_date TEXT,'
                 'return_date TEXT DEFAULT NULL'
                 ')'
                 )
        curr.execute(
                'CREATE TABLE IF NOT EXISTS instruments('
                 'id INTEGER PRIMARY KEY,'
                 'user_id INTEGER,'
                 'instrument_name TEXT,'
                 'available INTEGER DEFAULT 0,'
                 ')'
                 )

        self.close(conn,curr)



class DatabaseOperations(Database):
    def __init__(self):
        super().__init__()



    def rented(self, user_id, instrument_id, instrument_name):
            conn, curr = self.open()

            # Check if the instrument is available
            curr.execute("SELECT available FROM instruments WHERE id = ?", (instrument_id,))
            result = curr.fetchone()
            if not result or result[0] == 0:
                self.close(conn, curr)
                raise ValueError("Instrument is not available for rent")

            # Mark instrument as unavailable
            curr.execute("UPDATE instruments SET available = 0 WHERE id = ?", (instrument_id,))

            # Log the rental action
            rent_date = datetime.now().isoformat()
            curr.execute(
                "INSERT INTO logging (user_id, instrument_id, instrument_name, rent_date) VALUES (?, ?, ?, ?)",
                (user_id, instrument_id, instrument_name, rent_date)
            )

            self.close(conn, curr)
            return {"message": f"Instrument {instrument_name} rented successfully"}




    def returned(self, user_id, instrument_id):
            conn, curr = self.open()

            # Fetch the latest rental entry for the instrument and user
            curr.execute(
                "SELECT id FROM logging WHERE user_id = ? AND instrument_id = ? AND return_date IS NULL ORDER BY rent_date DESC LIMIT 1",
                (user_id, instrument_id)
            )
            rental_entry = curr.fetchone()
            if not rental_entry:
                self.close(conn, curr)
                raise ValueError("No active rental found for this user and instrument")

            # Mark instrument as available
            curr.execute("UPDATE instruments SET available = 1 WHERE id = ?", (instrument_id,))

            # Log the return action
            return_date = datetime.now().isoformat()
            curr.execute(
                "UPDATE logging SET return_date = ? WHERE id = ?",
                (return_date, rental_entry[0])
            )

            self.close(conn, curr)
            return {"message": f"Instrument {instrument_id} returned successfully"}



    def create_instrument(self, instrument_name):
        conn, curr = self.open()

        curr.execute(
                "INSERT INTO instruments (instrument_name) VALUES (?)",
                (instrument_name,)
            )

        self.close(conn,curr)
        return {"message": f"Instrument {instrument_name} created successfully"}













    def get_instrument_status(self, instrument_id):
        conn, curr = self.open()


        curr.execute("SELECT available FROM instruments WHERE id = ?", (instrument_id,))
        result = curr.fetchone()
        if not result:
            self.close(conn, curr)
            raise ValueError("Instrument not found")

        self.close(conn, curr)
        return {"instrument_id": instrument_id, "available": bool(result[0])}



    def get_instruments_available(self):
        conn, curr = self.open()
        curr.execute('SELECT id, instrument_name, available FROM instruments WHERE available = ?', (1,))


        instruments = curr.fetchall()
        instruments_list = []
        for instrument in instruments:

            instruments_list = [
                    {"id":instrument[0], "instrument_name": instrument[1], "available": bool(instrument[2])}
                                ]
            
        self.close(conn,curr)
        return instruments_list
            













    def log_instrument(self,instrument_id):
    
        pass

    def log_user(self, user_id):
        pass

    def log_user_instrument(self, user_id, instrument_id):

        pass

