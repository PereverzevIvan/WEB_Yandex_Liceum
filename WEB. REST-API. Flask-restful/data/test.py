from requests import get, post, delete

# 1 [Корректный] Просмотр всех пользователей
print(get('http://localhost:5000/api/v2/users').json())

# 2 [Корректный] Добавление новго пользователя
print(post('http://localhost:5000/api/v2/users', json={
    'id': 11,
    'surname': 'Ivanov',
    'name': 'Ivan',
    'age': 22,
    'position': 'Master',
    'speciality': 'Chasovchik',
    'email': 'pokemon@gmail.com',
    'hashed_password': 'pokemon 1',
    'address': 's. Ne_vashe_delovo'}).json())

# 3 [Корректный] Просмотр конкретного пользователя
print(get('http://localhost:5000/api/v2/users/11').json())

# 4 [Корректный] Удаление конкретного пользователя
print(delete('http://localhost:5000/api/v2/users/11').json())

# 5 [Корректный] Удаление конкретного пользователя
print(delete('http://localhost:5000/api/v2/users/12').json())

# 6 [Некорректный] Буква вместо id пользователя
# print(get('http://localhost:5000/api/v2/users/a').json())

# 7 [Некорректный] отсутствует возраст пользователя
print(post('http://localhost:5000/api/v2/users', json={
    'id': 11,
    'surname': 'Ivanov',
    'name': 'Ivan',
    'position': 'Master',
    'speciality': 'Chasovchik',
    'email': 'pokemon@gmail.com',
    'hashed_password': 'pokemon 1',
    'address': 's. Ne_vashe_delovo'}).json())

# 8 [Некорректный] Неправильный тип данных в поле id
print(post('http://localhost:5000/api/v2/users', json={
    'id': 'a',
    'surname': 'Ivanov',
    'name': 'Ivan',
    'age': 22,
    'position': 'Master',
    'speciality': 'Chasovchik',
    'email': 'pokemon@gmail.com',
    'hashed_password': 'pokemon 1',
    'address': 's. Ne_vashe_delovo'}).json())

# 9 [Некорректный] Производится удаление всех пользователей, а не конкретного
print(delete('http://localhost:5000/api/v2/users').json())

# 10 [Корректный] Просмотр всех пользователей
print(get('http://localhost:5000/api/v2/users').json())
