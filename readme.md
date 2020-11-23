# Smart Design Test Task

Для установки тествого виртуального окружения выполните следующие команды:
```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Для запуска контейнера базы данных и сервера на python выполните следующие команды:
```sh
docker run -d -p 27017:27017 mongo
python __main__.py
```
## Тесткейсы
Для создания товаров:
```sh
curl --header "Content-Type: application/json" --request POST --data '{"title": "Alternative Phone", "description": "bad", "display": 6.9}' http://localhost:8080/api/create_item
curl --header "Content-Type: application/json" --request POST --data '{"title": "Phone", "description": "Amazing", "display": 5}' http://localhost:8080/api/create_item
curl --header "Content-Type: application/json" --request POST --data '{"_id": 0, "title": "One more Phone", "description": "Really big", "display": 10}' http://localhost:8080/api/create_item
```
Ответ должен быть:
```json
{"status": "ok"}
```

Для получения списка товаров (без сортировки):
```sh
curl -X POST http://localhost:8080/api/get_items
```
Ответ должен быть (_id будет отличаться):
```json
{"items": [{"_id": {"$oid": "5fbb91282fa7c5279d2eecf8"}, "title": "Alternative Phone", "description": "bad", "display": 6.9}, {"_id": {"$oid": "5fbb91d04be3ee83c1b30fa9"}, "title": "Phone", "description": "Amazing", "display": 5}, {"_id": 0, "title": "One more Phone", "description": "Really big", "display": 10}]}
```

Для получения списка товаров (сортировка по title):
```sh
curl --header "Content-Type: application/json" --request POST --data '{"sort": "title"}' http://localhost:8080/api/get_items
```
Ответ должен быть:
```json
{"items": [{"_id": {"$oid": "5fb3cf643594fa394308e466"}, "title": "Alternative Phone", "description": "bad", "display": "6.9"}, {"_id": "0", "title": "One more Phone", "description": "Really big", "display": "10", "headphones": "false"}, {"_id": {"$oid": "5fb3cdfb7781d5d6860577ba"}, "title": "Phone", "description": "Amazing", "display": "6.5"}]}
```

Для получения товара по _id:
```sh
curl --header "Content-Type: application/json" --request POST --data '{"_id": 0}' http://localhost:8080/api/get_item
```
Ответ должен быть:
```json
{"item": {"_id": 0, "title": "One more Phone", "description": "Really big", "display": 10}}
```

Или по ObjecId:
```sh
curl --header "Content-Type: application/json" --request POST --data '{"_id": "5fbb91282fa7c5279d2eecf8"}' http://localhost:8080/api/get_item
```
Ответ должен быть:
```json
{"item": {"_id": {"$oid": "5fbb91282fa7c5279d2eecf8"}, "title": "Alternative Phone", "description": "bad", "display": 6.9}}
```