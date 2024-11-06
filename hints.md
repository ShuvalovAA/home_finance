#  Локальная разработка
## развёртывание

### Поднять кластер minikube
`minikube start --extra-config=apiserver.service-node-port-range=80-30000`

### Подключить в кластер ingress-nginx/controller
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/baremetal/deploy.yaml`

### Удалить неймспейс с подами(обязательно дождаться полного удаления. Проверить через`kubectl get pods -A`)
`helm uninstall hfin -n hfin`

### Дождаться когда под ingress-nginx-controller-* будет в статусе RUNNING
`kubectl -n ingress-nginx get pods`

### Внутри директории проекта вызвать сборку с помощью утилиты Helm(пересобрать неймспейс)
helm install <namespace> <project dir> -n <namespace> -f <values config file path>
`helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml --create-namespace`

### Проверить, что все поды в namespace запущены
`kubectl get pods -A |grep "hfin"` or `kubectl -n hfin get pods`

### Проверить, что ингресс заведён
`kubectl -n hfin get ing`

### Добавить host из ингресса на /etc/hosts на локальной машине
echo '<ingress address> <ingress host>' | sudo tee -a /etc/hosts
`echo '192.168.49.2 dev.hfin.local' | sudo tee -a /etc/hosts`

### Проверить порт для LoadBalancer(ожидается 80:80/TCP,443:443/TCP)
`kubectl -n ingress-nginx get svc | grep 'LoadBalancer'`

### Проверить резолв http://dev.hfin.local/
`curl http://dev.hfin.local/`


------
# Общие подсказки по проекту

## Docker
### билд образа
docker build {dir} -t {host}/{project}:{tag}
`docker build . -t 838375350179/hf:latest`

### пуш образа
`docker push 838375350179/hf:latest`

## Kubectl
### создание пространтсва имён
`kubectl create namespace hfin`

### добавить креды для docker registry
`minikube addons configure registry-creds`
`minikube addons enable registry-creds`
`minikube kubectl -- get pods -n kube-system | grep registry-creds`

### деинсталирование
`helm uninstall hfin -n hfin`

### инсталирование
`helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml`

### получение сервисной информации
`kubectl get pods -A |grep "hfin"`

### получение подробной информации
`kubectl -n hfin describe pod hfin-7c7ffbbbb8-lqj69`
    
### получение логи контейнера
`kubectl -n hfin logs hfin-7c7ffbbbb8-lqj69`

### переход внутрь процесса контейнера
`kubectl -n hfin exec -it hfin-958b7fbc7-grrbh  bash`


### получить логи прединициализируемых контейнеров
`kubectl logs -f -n hfin hfin-7f95b8ff64-hghnc -c hfin-init-postgress`

### информация с IPs
`kubectl -n hfin get pod -o wide`

### информация по службам
`kubectl get svc nginx -o wide`

### информация о ноде
`kubectl get nodes -o wide`

## Minikube
### генерация тунелей в миникубе
`minikube tunnel`

### APP
### рабочий урл
лежит в hfin.root.settings.CSRF_TRUSTED_ORIGINS

## MetalLB

### разрешить ARP
`kubectl get configmap kube-proxy -n kube-system -o yaml | sed -e "s/strictARP: false/strictARP: true/" | kubectl apply -f - -n kube-system`
### подключить Metallb
`kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml`
`kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"`


# Установка мониторинга для демонстрации
## Sentry
 * руководство инсталяции: https://develop.sentry.dev/self-hosted/
 * у проекта требуется получить DSN и прописать его в settings.SENTRY_DSN (потребуется перезагрузка проекта, если он запущен)

## Prometeuse + Grafana
### Prometeuse
1. `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
2. `helm repo update`
3. `helm install prometheus prometheus-community/prometheus`
4. `kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext`
5. получить forward-port `kubectl get svc | grep 'prometheus-server-ext'`
6. получить minkube ip и запомнить `minikube ip`
7. проверить ресурс {minikube ip}:{forward-port}
### Grafana
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

### Подключение метрик kubernetes
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

