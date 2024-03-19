import requests
import numpy as np

import aiosqlite
import asyncio
import aiohttp
class Getting_location:
    async def create_db(self, base_path):
        async with aiosqlite.connect(base_path) as db:
            await db.execute(""" CREATE TABLE IF NOT EXISTS water_free(title TEXT, instagram TEXT, description TEXT, address TEXT, refillType TEXT, option TEXT, locationx INTEGER, locationy INTEGER, photo TEXT) """)
    async def add_to_db(self, title, instagram, description, address, refillType, option, locationx, locationy, photo, base_path):
        async with aiosqlite.connect(base_path) as db:
            sat_tuple = (title, instagram, description, address, refillType, option, locationx, locationy, photo)
            await db.execute("""INSERT or REPLACE INTO water_free (title, instagram, description, address, refillType, option, locationx, locationy, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", sat_tuple)
            await db.commit()
    async def get_from_db(self, base_path):
        async with aiosqlite.connect(base_path) as db:
            get_location = await db.execute('SELECT locationx, locationy FROM water_free')
            get_location = await get_location.fetchall()
            return get_location
    async def get_from_coffee(self, base_path):
        async with aiosqlite.connect(base_path) as db:
            get_location = await db.execute('SELECT locationx, locationy FROM coffee_sale')
            get_location = await get_location.fetchall()
            return get_location
    async def get_location(self, latitude, longitude, DBPATH):
        locations = await self.get_from_db(DBPATH)
        coordination = np.array((latitude, longitude))
        distances = np.linalg.norm(locations-coordination, axis=1)
        min_index = np.argsort(distances)
        min_index = min_index[0:25]
        return min_index
    
    async def get_location_coffee(self, latitude, longitude, DBPATH):
        locations = await self.get_from_coffee(DBPATH)
        coordination = np.array((latitude, longitude))
        distances = np.linalg.norm(locations-coordination, axis=1)
        min_index = np.argsort(distances)
        min_index = min_index[0:25]
        return min_index
    async def create_coffee(self, base_path):
        async with aiosqlite.connect(base_path) as db:
            await db.execute(""" CREATE TABLE IF NOT EXISTS coffee_sale(title TEXT, instagram TEXT, description TEXT, address TEXT, refillType TEXT, option TEXT, locationx INTEGER, locationy INTEGER, photo TEXT) """)
            
    async def add_to_db_coffee(self, title, instagram, description, address, refillType, option, locationx, locationy, photo, base_path):
        async with aiosqlite.connect(base_path) as db:
            sat_tuple = (title, instagram, description, address, refillType, option, locationx, locationy, photo)
            await db.execute("""INSERT or REPLACE INTO coffee_sale (title, instagram, description, address, refillType, option, locationx, locationy, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", sat_tuple)
            await db.commit()
    # async def write_to_file(self, filename, blob):
    #     async with aiofiles.open(filename, mode="wb") as f:
    #         await f.write(blob)
    # async def delete_file(self, filename):
    #     await os.remove(filename)
            
            
    

    # async def download_and_convert_to_binary_data(self, url, session):
    #     try:
    #         async with session.get(url=url) as resp:
    #             if "jpg" or "JPG" in url:
    #                 filename = url.split("/")[-1].split(".jpg")[0]+".jpg"
    #             elif "png" in url:
    #                 filename = url.split("/")[-1].split(".png")[0]+".png"
    #             elif "jpeg" in url:
    #                 filename = url.split("/")[-1].split(".jpg")[0]+"jpg"
    #             else:
    #                 print(url)
    #                 filename = ""
    #             if resp.status == 200:
    #                 f = await aiofiles.open(filename, mode='wb')
    #                 await f.write(await resp.read())
    #                 await f.close()
    #             elif resp.status == 503:
    #                 pass
    #             async with aiofiles.open(filename, 'rb') as file:
    #                 blob_binary_data = await file.read()
    #                 await file.close()
    #                 await os.remove(filename)
    #                 return blob_binary_data
    #     except aiohttp.client_exceptions.InvalidURL:
    #         return None
        
# a = Getting_location()
# asyncio.run(a.get_location(latitude=54.735152, longitude=55.958736))
# asyncio.run(get_location(54.989347, 73.368221))
# asyncio.run(a.create_coffee("""C:/Users/tea/Desktop/project/modules/database/users.db"""))

# print(locations)

# DBPATH = """C:/Users/tea/Desktop/project/modules/database/users.db"""
# async def get_data():
#     async with aiohttp.ClientSession(trust_env=True, raise_for_status=True) as session:
#         r = requests.post("https://wps-api.tvojavoda.ru/water-point/search", data = {"longitude":0.0,"latitude":0.0} )

#         r = r.json()
#         r = r["waterPointList"]
#         for i in r:
#             option = i["optionList"]
#             option = "\n".join(option)
#             if "скидка на кофе в свою кружку" in option:
#                 await a.add_to_db_coffee(i["title"], i["instagram"], i["description"], i["address"], i["refillType"], option, float(i["location"]["coordinates"][1]), float(i["location"]["coordinates"][0]), i["photo"], DBPATH)
            # photo = await a.download_and_convert_to_binary_data(photo_url, session)
#             await a.add_to_db(i["title"], i["instagram"], i["description"], i["address"], i["refillType"], option, float(i["location"]["coordinates"][1]), float(i["location"]["coordinates"][0]), i["photo"], DBPATH)
#             # print(i["title"]+"\n\n"+i["instagram"]+"\n\n"+i["description"]+"\n\n"+i["address"]+"\n\n"+i["refillType"]+"\n\n"+option+"\n\n"+str(i["location"]["coordinates"][0])+"\n\n"+str(i["location"]["coordinates"][1]))
            
# asyncio.run(get_data())