from database import SessionLocal
from models import Station

db = SessionLocal()

# Тестовые АЗС (координаты реальные, можно менять)
test_stations = [
    {
        "name": "Лукойл, М4 115 км",
        "lat": 54.1961,
        "lng": 37.6193,
        "amenities": {"toilet": True, "cafe": True, "wifi": True, "shower": False},
        "fuels": {"92": "green", "95": "green", "dt": "yellow"}
    },
    {
        "name": "Газпромнефть, М7 89 км",
        "lat": 56.1304,
        "lng": 40.4120,
        "amenities": {"toilet": True, "shower": True, "cafe": False},
        "fuels": {"92": "green", "95": "red", "dt": "green"}
    },
    {
        "name": "Роснефть, Тула",
        "lat": 54.1931,
        "lng": 37.6173,
        "amenities": {"toilet": True, "atm": True},
        "fuels": {"92": "yellow", "95": "green", "dt": "green"}
    },
    {
        "name": "Татнефть, Рязань",
        "lat": 54.6292,
        "lng": 39.7366,
        "amenities": {"toilet": True, "cafe": True},
        "fuels": {"92": "green", "95": "green", "dt": "red"}
    },
    {
        "name": "Башнефть, Владимир",
        "lat": 56.1291,
        "lng": 40.4066,
        "amenities": {"toilet": True, "shower": True, "wifi": True},
        "fuels": {"92": "green", "95": "yellow", "dt": "green"}
    }
]

for data in test_stations:
    station = Station(**data)
    db.add(station)

db.commit()
db.close()

print("✅ Добавлено 5 тестовых АЗС в базу данных")