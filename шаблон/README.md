
---
### Swagger of Staging
- DOCS_URL:http://changeset.midgard.k8s.internal.sailplay.org/services/changeset/docs#/
---
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


### Обслуживание

#### * работа с миграциями

- документация по [alembic](https://alembic.sqlalchemy.org/en/latest/)
- генерация соответствующей миграции, для дальнейшей правки
`alembic -n {имя блока с настройками в alembic.ini}  revision -m "{имя миграции}"`
- понизить миграцию
`alembic -n {имя блока с настройками в alembic.ini}  downgrade {количество шагов}`
- повысить миграцию
`alembic -n {имя блока с настройками в alembic.ini}  upgrade {количество шагов}`

#### * работа с образом
перед билдом следует обномить лок poetry, если редактировали pyproject.toml
```bash
poetry lock
```
- билд образа 

```bash
docker build --build-arg pypi_user={user_name}  --build-arg pypi_pass={user_password} . -t cr.yandex/crp0civq107m91j8p8a2/services/changeset:{tag}
```

####  работа с k8s
- инсталяция микросервиса в кластере
```bash
helm install changeset ./helm -n changeset -f ./helm/values.staging.yaml
```
- деинсталация микросервиса в кластере
```bash
helm uninstall changeset -n changeset 
```
- получение сервисной информации
```bash
kubectl get pods -A |grep "changeset"
```