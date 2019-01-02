from redis import Redis
conn = Redis(host='localhost', port=6379, db=5, password='**', decode_responses=True)

name=conn.keys()
for name_1 in name:
    conn.delete(name_1)
print('a')