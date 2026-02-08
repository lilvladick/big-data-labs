## Запуск базы данных

```bash
docker run -d --name lab1  -e POSTGRES_DB=sakila  -e POSTGRES_PASSWORD=p_ssW0rd  -p 5432:5432 sakiladb/postgres:latest
```

Доступ к базе:
- База данных: sakila 
- Пользователь: sakila 
- Пароль: p_ssW0rd 
- Порт: 5432/5432