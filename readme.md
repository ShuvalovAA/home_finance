# Requarements


# ENV vars

#Для PostgreSQL
export HFIN_POSTGRESQL_DATABASE=postgres
export HFIN_POSTGRESQL_PORT=6432
export HFIN_POSTGRESQL_HOST=localhost
export HFIN_POSTGRESQL_USER=postgres
export HFIN_POSTGRESQL_PASSWORD=postgres

#Для ClickHouse
export HFIN_CLICKHOUSE_HOST=localhost
export HFIN_CLICKHOUSE_PORT=8123
export HFIN_CLICKHOUSE_PASSWORD=
export HFIN_CLICKHOUSE_DATABASE=default
export HFIN_CLICKHOUSE_USER=default


#Для Redis и Celery
export HFIN_REDIS_PORT=6379
export HFIN_REDIS_HOST=localhost


# Deploy

## Docker
### Build
    ```
    docker build . -t 838375350179/hf:latest
    docker push 838375350179/hf:latest
    ```
## K8S
### Local
    ```
    >> minikube start
    >> helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml --create-namespace

    >> helm uninstall hfin
    >> helm upgrade hfin ./helm -n hfin -f ./helm/values.staging.yaml
    ```
