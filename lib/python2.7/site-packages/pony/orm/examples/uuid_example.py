from pony.orm import *
import uuid

db = Database('mysql', host="localhost", user="presentation", passwd="pony", db="presentation")

class Test(db.Entity):
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    attr1 = Required(str)

db.generate_mapping(create_tables=True)


with db_session:
    id  = uuid.uuid4()
    print id
    Test(id=uuid.UUID(id), attr1='test')
    Test(id=id, attr1='test')

