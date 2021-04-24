from requests import get, post, delete

# Посмотрим все работы до внесения изменений в таблицу
print(get('http://localhost:5000/api/jobs').json())

# (Конкретный запрос) Добавляем работу с id, равным 18
print(post('http://localhost:5000/api/jobs', json={
    'id': 16,
    'job': 'Joke job',
    'work_size': 3,
    'collaborators': '1',
    'is_finished': True,
    'team_leader': 1}).json())

# (Неконкретный запрос) отсутствует параметр is_finished
print(post('http://localhost:5000/api/jobs', json={
    'id': 16,
    'job': 'Joke job',
    'work_size': 3,
    'collaborators': '1',
    'team_leader': 1}).json())

# (Неконкретный запрос) Пустой запрос
print(post('http://localhost:5000/api/jobs').json())

# (Неконкретный запрос) Уже добавлена работы с таким id
print(post('http://localhost:5000/api/jobs', json={
    'id': 18,
    'job': 'Joke job',
    'work_size': 3,
    'collaborators': '1',
    'is_finished': True,
    'team_leader': 1}).json())

# Посмотрим на словарь работ после внесения изменений
print(get('http://localhost:5000/api/jobs').json())

print(delete('http://localhost:5000/api/jobs/16').json())

# Посмотрим на словарь работ после внесения изменений
print(get('http://localhost:5000/api/jobs').json())
