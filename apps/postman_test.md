## Тестирование API через Postman

###1. Запрос температуры по локации

Cоздать GET запрос, вставить URL

http://localhost:8000/temperature?location=Living%20Room 

Вернется ответ:

{
    "location": "Living Room",
    "sensorId": 1,
    "temperature": 18.9
}

   

###2. Запрос списка всех зарегистрированных устройств/сенсоров

Создать GET запрос , вставить URL

http://localhost:8000/api/sensors 

Вернется ответ

[
    {
        "created_at": "Sat, 19 Sep 2026 15:30:38 GMT",
        "device_id": "dev-001",
        "id": 1,
        "location": "Living Room",
        "type": "sensor"
    },
    {
        "created_at": "Sat, 19 Sep 2026 15:30:38 GMT",
        "device_id": "dev-002",
        "id": 2,
        "location": "Bedroom",
        "type": "sensor"
    },
    {
        "created_at": "Sat, 19 Sep 2026 15:30:38 GMT",
        "device_id": "dev-003",
        "id": 3,
        "location": "Kitchen",
        "type": "gateway"
    },
    {
        "created_at": "Sat, 19 Sep 2026 15:34:20 GMT",
        "device_id": "sensor -1",
        "id": 4,
        "location": "Kitchen",
        "type": "sensor"
    },
    {
        "created_at": "Sat, 19 Sep 2026 16:27:29 GMT",
        "device_id": "sensor -2",
        "id": 6,
        "location": "Kitchen",
        "type": "sensor"
    },
    {
        "created_at": "Sat, 19 Sep 2026 16:28:15 GMT",
        "device_id": "sensor -3",
        "id": 8,
        "location": "Garage",
        "type": "sensor"
    }
]

###3. Запросить температуру по всем зарегистрированным сенсорам

Создать запрос GET, вставить URL
http://localhost:8000/temperaturebysensors 

Вернется ответ:
{
    "sensors": [
        {
            "device_id": "dev-001",
            "id": 1,
            "location": "Living Room",
            "temperature": 24.7
        },
        {
            "device_id": "dev-002",
            "id": 2,
            "location": "Bedroom",
            "temperature": 23.6
        },
        {
            "device_id": "dev-003",
            "id": 3,
            "location": "Kitchen",
            "temperature": 34.3
        },
        {
            "device_id": "dev-005",
            "id": 4,
            "location": "Hall",
            "temperature": 23.4
        }
    ]
}

