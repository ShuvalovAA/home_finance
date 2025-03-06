# Веб-приложения FinancePlanner

Авторское право подтверждено государственным университетом "Дубна".


## Краткое описание проекта

Веб-приложения FinancePlanner является приложением SaaS. Оно закрывает потребности пользователей в управлении своими сбережениями,
планируя бюджет расходов и бюджет доходов.

## Технологический стек проекта
+ ASGI - асинхронный интерфейс шлюза сервера;
+ Uvicorn - реализация веб-сервера ASGI;
+ Nginx - веб-сервер;
+ Django - фреймворк для языка программирования Python;
+ Python - интерпретируемый язык программирования;
+ PostgreSQL - объектно-реляционная система управления базами данных;
+ CkickHouse - колоночная аналитическая система управления базами данных;
+ Redis - хранилище данных типа «ключ-значение»;
+ Celery - асинхронная распределённая очередь задач;
+ Docker - платформа контейнеризации;
+ Kubernetes - программное обеспечение для оркестровки контейнеризированных приложений;
+ Ubuntu - операционная система, на базе дистрибутива Linux и Unix-подобной ОС Debian;
+ GitHub - веб-платформа для управления проектами и репозиториями программного кода;
+ Git - система контроля версий;
+ JavaScript - язык программирования, который используется для создания интерактивных и динамических веб-сайтов;
+ VisualStudioCode - текстовый редактор кода;
+ Sentry - платформа для мониторинга и отслеживания ошибок в программном обеспечении;
+ Grafana - программная система визуализации данных, ориентированная на данные систем ИТ-мониторинга;
+ Prometheus - система серверов и программ, предназначенная для сбора и анализа данных о работоспособности IT-оборудования;
+ Стэк ELK - комплекс программ, который используется для управления журналами, поиска и аналитики.

## Структура репозитория

```
├── fixtures                           # файлы с тестовыми наборами данных
├── helm                               # директория директи helm
│   └── templates
│       ├── celery-beat                # директория директивы запуска планироващика Celery
│       ├── celery-worker              # директория директивы запуска воркера Celery
│       ├── clickhouse                 # директория директивы запуска основной СУБД clickhouse
│       ├── clickhouse-replica         # директория директивы запуска реплики clickhouse
│       ├── ellk                       # директория директивы запуска стека ELK
│       │   ├── elastic_search         # директория директивы запуска elastic_search
│       │   ├── filebeat               # директория директивы запуска filebeat
│       │   ├── kibana                 # директория директивы запуска kibana
│       │   └── logstash               # директория директивы запуска logstash
│       ├── grafana                    # директория директивы запуска grafana
│       ├── migration                  # директория директивы запуска миграций баз данных
│       ├── nginx                      # директория директивы запуска nginx
│       ├── postgresql-master          # директория директивы запуска основной СУБД postgresql 
│       ├── postgresql-replica-1       # директория директивы запуска реплики postgresql
│       ├── postgresql-replica-2       # директория директивы запуска реплики postgresql
│       ├── redis                      # директория директивы запуска хранилища ключ-значений
│       └── redis-cache                # директория директивы запуска хранилища ключ-значений для кеширования
└── hfin
│    ├── assistant                     # директория кода эксперементальной функции предсказания
│    ├── clients                       # директория кода лиентов для интеграции
│    ├── common_utils                  # директория кода основных дополнительных инстурментов
│    ├── expense                       # директория кода расходов
│    ├── funds_director                # директория кода фондов
│    ├── income                        # директория кода доходов
│    ├── media                         # директория медиафайлов
│    │   └── temp_files                # директория временных файлов
│    ├── notificator                   # директория кода уведомлений
│    ├── payment                       # директория кода управления платежами пользователей
│    ├── reporter                      # директория кода сборщика отчётов
│    ├── root                          # директория кода административных модулей
│    │   ├── management                # директория кода административных команд
│    ├── static                        # директория статических файлов
│    │   ├── admin                     # директория кода Django
│    │   ├── bootstrap                 # директория кода фреймворка bootstrap
│    │   ├── common                    # директория кода основных статических файлов
│    │   ├── drf-yasg                  # директория кода фреймворка drf-yasg  
│    │   ├── expense                   # директория кода статических файлов расходов
│    │   ├── home                      # директория кода домашней страницы
│    │   ├── income                    # директория кода доходов
│    │   ├── pivottable                # директория кода библиотеки
│    │   ├── profile                   # директория кода профиля пользоватлей
│    │   ├── report                    # директория кода сборщика отчётов
│    │   ├── rest_framework            # директория кода фреймворка rest_framework
│    │   ├── transaction               # директория кода статических файлов транзакций
│    │   └── user                      # директория кода статических файлов для пользователей
│    ├── tasks                         # директория кода задач для отложенного и запланированного выполнения
│    ├── tests                         # директория кода автотестов
│    ├── transaction                   # директория кода транзакций
|    └── user                          # директория кода для управления пользователями
├── hints.md                           # файл с подсказками
├── Dockerfile                         # файл для сборки образа Docker
├── Makefile                           # файл с административным командами над проектом
├── poetry.lock                        # файл логгирования poetry
├── pyproject.toml                     # директива зависимостей poetry для Python
├── LICENSE                            # лицензия проекта
├── .gitignore                         # файл игнорирования файлоф для git
├── .gitlab-ci.yml                     # файл сценария CI/CD
└── README.md                          # файл описания проекта
```


## !Установка!

##  Локальная разработка
### Справка
* может быть что нехватает места из-за докер образов на машине. Используйте `docker system prune -f` и `minikube ssh docker system prune` для очистки пространства.
* приложение может быть не доступно из браузера, потому что они по-умочанию запрещают посещать сайты с протоколом http без сертификации
### развёртывание
#### Версия minkube
`minikube v1.23.2`
#### Поднять кластер minikube
`minikube start --extra-config=apiserver.service-node-port-range=80-30000 --cpus 4 --memory 8192`

#### Подключить в кластер ingress-nginx/controller
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/baremetal/deploy.yaml`

#### Удалить неймспейс с подами(обязательно дождаться полного удаления. Проверить через`kubectl get pods -A`)
`helm uninstall hfin -n hfin`

#### Дождаться когда под ingress-nginx-controller-* будет в статусе RUNNING
`kubectl -n ingress-nginx get pods`

#### Внутри директории проекта вызвать сборку с помощью утилиты Helm(пересобрать неймспейс)
helm install <namespace> <project dir> -n <namespace> -f <values config file path>
`helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml --create-namespace`

#### Проверить, что все поды в namespace запущены
`kubectl get pods -A |grep "hfin"` or `kubectl -n hfin get pods`

#### Проверить, что ингресс заведён
`kubectl -n hfin get ing`

#### Добавить host из ингресса на /etc/hosts на локальной машине
echo '<ingress address> <ingress host>' | sudo tee -a /etc/hosts
`echo '192.168.49.2 dev.hfin.local' | sudo tee -a /etc/hosts`

#### Проверить порт для LoadBalancer(ожидается 80:80/TCP,443:443/TCP)
`kubectl -n ingress-nginx get svc | grep 'LoadBalancer'`

#### Проверить резолв http://dev.hfin.local/
`curl http://dev.hfin.local/`

## Установка мониторинга для демонстрации
### ELK
* Адрес Kibana - {minikube ip}:{elk.kibana.service.spec.nodePort}
### Sentry
 * руководство инсталяции: https://develop.sentry.dev/self-hosted/
 * у проекта требуется получить DSN и прописать его в settings.SENTRY_DSN (потребуется перезагрузка проекта, если он запущен)

### Prometeuse + Grafana
#### Prometeuse
1. `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
2. `helm repo update`
3. `helm install prometheus prometheus-community/prometheus`
4. `kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext`
5. получить forward-port `kubectl get svc | grep 'prometheus-server-ext'`
6. получить minkube ip и запомнить `minikube ip`
7. проверить ресурс {minikube ip}:{forward-port}
#### Grafana
1. `helm repo add grafana https://grafana.github.io/helm-charts`
2. `helm repo update`
3. `helm install grafana grafana/grafana`
4. получить пароль `kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo`
    пример = uZsgVOJzUqSP6D47aysuBnbIJwhajk6HnccMFtN5
5. `kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext`
6. `kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext service/grafana-ext exposed`
7. получить forward-port `kubectl get svc | grep 'grafana-ext'`
8. проверить ресурс {minikube ip}:{forward-port}
9. авторизоваться: `login=admin; password=uZsgVOJzUqSP6D47aysuBnbIJwhajk6HnccMFtN5`
10.  перейти к Data sources --> Add Prometheus --> Provide IP Address - Save and Test
10.1 В Data sources выбрать Prometheuse
10.2 Задать Prometgeuse server URL = `http://{minikube}:{forward-port}`
10.3 Нажать `Save and Test`
11. Перейти к Dashboard --> New --> Import
11.1 Указать ID 
11.2 В этом же поле нажать `Load`
11.3 В поле prometheus выбрать `Prometheus` с тегом `default`
11.4 Нажать кнопку `Import`

#### Подключение метрик kubernetes
12. `kubectl expose service prometheus-kube-state-metrics --type=NodePort --target-port=8080 --name=prometheus-kube-state-metrics-ext`
13. получить forward-port `kubectl get svc | grep 'prometheus-kube-state-metrics-ext'`
14. проверить ресурс {minikube ip}:{forward-port}
15. `kubectl edit cm prometheus-server`
16. найти секцию `scrape_configs`
17. добавить в секцию
```Yaml
...
- job_name: prometheus
      static_configs:
      - targets:
        - {minikube ip}:{forward-port}
...
```
18. перейти в DashBoard и нажать `New` --> `New Dashboard` --> `Add vizualization`
18.1 выбрать в качестве источника Prometheus
18.2 в разделе Queries  выбрать metric = `container_memory_rss`
18.21 если выбрать опцию `code`, то можно прописать показатели в гигабайтах
пример = `container_memory_rss{namespace="hfin"}/1024/1024/1024`
18.3 в разделе Queries  выбрать label filters = `namespace = hfin`
18.4 нажать `Run queries`
18.5 нажать `Save dashboard`

## Запуск автотестов
1. Перейти в директорию проекта
`cd home_finance/hfin`
2. Активировать виртуальную среду
`poetry shell`
3. Запустить тестирование
`poetry run pytest .`
4. Запустить тестирование с отчётом покрытия тестами
`poetry run pytest . --cov=. --cov-report=term --cov-report term-missing --cov-config=.coveragerc`

## Использование

Приложение разворачивается на инфраструктре нескольких серверов или локально через технологию K8S.

## Лицензия, коммерческая тайна, права третьих лиц

GNU AGPL

## Контакты


ФИО: Шувалов Артемий Александрович

Email: shuvalovartal@gmail.com

