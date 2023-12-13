
---
### Swagger of Staging
- DOCS_URL:http://changeset.midgard.k8s.internal.sailplay.org/services/changeset/docs#/
---
### Общее
Микросервис имеет два главных класса:
* `Starter`, отвечающий за иницилазицию мультисоставной загрузки в 
микросервисе и в бакете сервиса Yandex Object Storage.
* `Chief`, отвечающий за сам процесс загрузки после инициализации.

Мультисоставная загрузка прерывается и требует перезапуска если:
- сервис Yandex Object Storage перестал принимать пакеты загрузки.
- микросервис получил из ClickHouse пустой первый пакет.

Ориентировочная производительность: 10Mb/s или 1 jsonl объект размером 50000 строк в секунду.
### Установка зависимостей
Чтобы локально установить все зависимости, сначала необходимо настроить доступ до pypi. В pyproject.toml уже указан
путь до pypi, нужно добавить свои credentials с доступом. Для этого выполняем следующую команду:
poetry config http-basic.sailplay-pypi < username > < password >
где вместо < username > и < password > необходимо указать личные креды с доступом к nexus.
Также при установке poetry попытается скачивать пакеты из нашего pypi по https и запросит сертификат у nexus.
Для локальной разработки можно отключить эту проверку с помощью команды:
poetry config certificates.sailplay-pypi.cert false
Для установки зависимостей:
poetry install --no-root

### Переменные окружения
Следующие переменные используются микросервисом:
```bash
#Для PostgreSQL
export CHANGESET_POSTGRESQL_DATABASE=postgres
export CHANGESET_POSTGRESQL_PORT=5432
export CHANGESET_POSTGRESQL_HOST=localhost
export CHANGESET_POSTGRESQL_USER=postgres
export CHANGESET_POSTGRESQL_PASSWORD=postgres

#Для ClickHouse
export CHANGESET_CLICKHOUSE_HOST=localhost
export CHANGESET_CLICKHOUSE_PORT=8123
export CHANGESET_CLICKHOUSE_PASSWORD=
export CHANGESET_CLICKHOUSE_DATABASE=default
export CHANGESET_CLICKHOUSE_USER=default

#Для Yandex Object Storage
export AWS_SECRET_ACCESS_KEY=''
export AWS_ACCESS_KEY_ID=''
export BUCKET_NAME=sp-test-app

#Для Redis и Celery
export CHANGESET_REDIS_PORT=6379
export CHANGESET_REDIS_HOST=localhost

#Для приложения и Celery
export TMP_DIR=/tmp/changeset
export APP_NAME=changeset
```
### Обслуживание

#### * работа с миграциями

- документация по [alembic](https://alembic.sqlalchemy.org/en/latest/)
- генерация соответствующей миграции, для дальнейшей правки
`alembic -n {имя блока с настройками в alembic.ini}  revision -m "{имя миграции}"`
- понизить миграцию 
`alembic -n {имя блока с настройками в alembic.ini}  downgrade {количество шагов | head} `
- повысить миграцию
`alembic -n {имя блока с настройками в alembic.ini}  upgrade {количество шагов | head}`

#### * работа с образом
перед билдом следует обновить лок poetry, *если редактировали pyproject.toml вручну.*
```bash
poetry lock
```
- билд образа 

```bash
docker build --build-arg pypi_user={user_name}  --build-arg pypi_pass={user_password} . -t cr.yandex/crp0civq107m91j8p8a2/services/changeset:{tag}
```

####  работа с k8s
- инсталяция микросервиса в midgard
```bash
helm install changeset ./helm -n changeset -f ./helm/values.staging.yaml
```
- деинсталация микросервиса в кластере
```bash
helm uninstall changeset -n changeset 
```
- получение сервисной информации по запущенным подам
```bash
kubectl get pods -A |grep "changeset"
```