import aiosqlite


class Database:
    global user_yes_or_no
    
    async def create_db(self, base_path):
        async with aiosqlite.connect(base_path) as db:
            await db.execute(""" CREATE TABLE IF NOT EXISTS tgusers(userid INTEGER, username TEXT, surname TEXT, firstname TEXT) """)
    async def add_to_db(self, userid, username, surname, firstname, base_path):
        async with aiosqlite.connect(base_path) as db:
            sat_tuple = (userid, username, surname, firstname)
            await db.execute(""" INSERT INTO tgusers (userid, username, surname, firstname) VALUES (?, ?, ?, ?)""", sat_tuple)
            await db.commit()
    async def check_to_db(self, userid, base_path):
        async with aiosqlite.connect(base_path) as db:
            user_yes_or_no = await db.execute('SELECT * FROM tgusers WHERE userid = ?', (userid, ))
            user_yes_or_no = await user_yes_or_no.fetchone()
            return user_yes_or_no
    async def get_places_row(self, base_path, id):
        async with aiosqlite.connect(base_path) as db:
            places = await db.execute("SELECT * FROM water_free")
            places = await places.fetchall()
            places = places[id]
            return places
    async def get_places_row_coffee(self, base_path, id):
        async with aiosqlite.connect(base_path) as db:
            places = await db.execute("SELECT * FROM coffee_sale")
            places = await places.fetchall()
            places = places[id]
            return places 
    async def get_geo(self, base_path, street):
        async with aiosqlite.connect(base_path) as db:
            places = await db.execute("SELECT locationx, locationy FROM water_free WHERE address = ?", (street, ))
            places = await places.fetchone()
            return places
    async def get_geo_coffee(self, base_path, street):
        async with aiosqlite.connect(base_path) as db:
            places = await db.execute("SELECT locationx, locationy FROM coffee_sale WHERE address = ?", (street, ))
            places = await places.fetchone()
            return places