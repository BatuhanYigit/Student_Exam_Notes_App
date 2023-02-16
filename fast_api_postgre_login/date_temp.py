import datetime



today = datetime.datetime.now()

print(today)

expire_time = datetime.datetime.now() + datetime.timedelta(minutes=15)

print("expire : ",expire_time)
print("now : ", today)

print(type(today))

if (today < expire_time):
    print("Tarih geçmemiş")
else:

    print("tarih geçmiş")