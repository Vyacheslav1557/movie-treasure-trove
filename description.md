# Описание работы и структуры проекта

## Работа

> Почти все основные данные берутся из [*API кинопоиска*](https://kinopoiskapiunofficial.tech/). 
> Далее эти данные отображаются в [*интерфейсе бота*](https://kinopoiskapiunofficial.tech/) или игнорируются, 
> в зависимости от действий пользователя.

## Структура

### Проект разбит на отдельные файлы и сгруппирован по функционалу

> 1. api_client (инициализация клиента [*API кинопоиска*](https://kinopoiskapiunofficial.tech/))
> 2. bot_features (основной функционал бота и взаимодействие с [*API телеграма*](https://github.com/python-telegram-bot/python-telegram-bot))
> 3. database
>    * bot_database.db (по понятным причинам её нет на гитхабе)
>    * models (модели таблиц базы данных и её инициализация)
>    * queries (упрощение взаимодействия с базой данных)
> 4. shortcuts (сбор основных данных из запросов [*API кинопоиска*](https://kinopoiskapiunofficial.tech/))
> 5. main.py - конфигурация и запуск бота
> 6. constants.py - ключи [*API кинопоиска*](https://kinopoiskapiunofficial.tech/) и [*API телеграма*](https://github.com/python-telegram-bot/python-telegram-bot)
