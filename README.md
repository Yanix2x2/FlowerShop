# Сайт FlowerShop

Это сайт сети цветочных магазинов.
Здесь можно заказать консультацию по подбору букета или выбрать из каталога с оформлением доставки или самовывозом.

---
# Переменные окружения

Образ с Django считывает настройки из переменных окружения.  
Создайте файл `.env` в корневом каталоге и запишите туда данные в формате: `ПЕРЕМЕННАЯ=значение`

- **`SECRET_KEY`** — обязательная секретная настройка Django.  
  Это соль для генерации хэшей. Значение может быть любым, важно лишь, чтобы оно никому не было известно.  
  [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key)
- **`DEBUG`** — настройка Django для включения отладочного режима.  
  Принимает значения `TRUE` или `FALSE`.  
  [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG)

- **`ALLOWED_HOSTS`** — настройка Django со списком разрешённых адресов.  
  Если запрос прилетит на другой адрес, то сайт ответит ошибкой **400 Bad Request**.  
  Можно перечислить несколько адресов через запятую, например: `127.0.0.1,192.168.0.1,flower-shop.test`
  [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts)
- **`DATABASE_URL`** — адрес для подключения к базе данных PostgreSQL.  
  Другие СУБД не поддерживаются.  
  [Формат записи](https://github.com/jacobian/dj-database-url#url-schema)

---

## Запуск dev-версии сайта в Docker

Используйте `deploy/docker-compose-dev.yml` из корня репозитория.
1. Установите [Docker Desktop](https://www.docker.com/get-started).
2. Клонируйте репозиторий:
   ```sh
   git https://github.com/Yanix2x2/FlowerShop.git
   ```
3. Перейдите в каталог проекта:
   ```sh
   cd deploy
   ```
4. Соберите и запустите контейнеры:
    ```sh
    docker compose -f docker-compose-dev.yml up --build
    ```
5. После запуска сайт будет доступен по адресу: [http://localhost:8000/](http://localhost:8000/).

* Создать административную учетную запись:

  - запустите команду:

      ```sh
      docker compose -f docker-compose-dev.yml exec web sh -lc 'python manage.py createsuperuser'
      ```

---
## Быстрое развертывание на сервере prod-версии сайта в Docker
1. Скопируйте файл `deploy/deploy.sh` и `.env` в папку на сервере (например `opt`).
2. Запустите Bash скрипт деплоя:
    ```sh
    ./deploy.sh
    ```
    Если у файла нет прав на исполнение выполните команду:

    ```sh
    chmod +x deploy.sh
    ```
* Создать административную учетную запись:

  - Перейдите в каталог проекта:
     ```sh
     cd FloverShop/deploy
     ```
  - запустите команду:

      ```sh
      docker compose -f docker-compose-prod.yml exec web sh -lc 'python manage.py createsuperuser'
      ```
Настройте Nginx указав пути к staticfiles и media (с учетом расположения проекта `opt/FloverShop/flower_store/`):

`opt/FloverShop/flower_store/staticfiles/`

`opt/FloverShop/flower_store/media/`
