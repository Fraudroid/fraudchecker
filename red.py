import os
import redis

app_path = "D:\\PaperW\\Stage2\\droidData\\4600out\\"

pool = redis.ConnectionPool(host='192.168.3.70', port=6379, db=8)
r = redis.Redis(connection_pool=pool)
res_db1 = r.lrange('apkname', 0, -1)

if os.path.exists(app_path):
    fileDist = os.listdir(app_path)
    for file in fileDist:
        r.lpush('apkname', file)
