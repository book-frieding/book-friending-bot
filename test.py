import motor.motor_asyncio
import asyncio
import pprint

CONNECTION_STRING = "mongodb+srv://pakrentos:kyh63r8l48@bookfriendingapp.nme65.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(
    CONNECTION_STRING, uuidRepresentation="standard"
)

db = client["test"]
collection = db["tg_users"]


async def do_replace():
    coll = db.tg_users
    old_document = await coll.find_one({ '_id': {'$eq': '1'} })
    print('found document: %s' % pprint.pformat(old_document))
    _id = old_document['_id']
    result = await coll.replace_one({'_id': _id}, {'key': 'value'})
    print('replaced %s document' % result.modified_count)
    new_document = await coll.find_one({'_id': _id})
    print('document is now %s' % pprint.pformat(new_document))


async def do_find_one():
    document = await db.tg_users.find_one({'_id': {'$eq': 0}})
    pprint.pprint(document)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_find_one())
    loop.close()