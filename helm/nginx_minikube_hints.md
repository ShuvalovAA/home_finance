#  Локальная разработка
## развёртывание

### Поднять кластер minikube
`minikube start --extra-config=apiserver.service-node-port-range=80-30000`

### Подключить в кластер ingress-nginx/controller
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/baremetal/deploy.yaml`

### Создать пространство имён
`kubectl create namespace hfin`

### Дождаться когда под ingress-nginx-controller-* будет в статусе RUNNING
`kubectl -n ingress-nginx get pods`

### Внутри директории проекта вызвать сборку с помощью утилиты Helm
helm install <namespace> <project dir> -n <namespace> -f <values config file path>
`helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml`

### Проверить, что все поды в namespace запущены
`kubectl get pods -A |grep "hfin"` or `kubectl -n hfin get pods`

### Проверить, что ингресс заведён
`kubectl -n hfin get ing`

### Добавить host из ингресса на /etc/hosts на локальной машине
echo '<ingress address> <ingress host>' | sudo tee -a /etc/hosts
`echo '192.168.49.2 dev.hfin.local' | sudo tee -a /etc/hosts`

### Завести tunnel
`minikube tunel`

### Проверить порт для LoadBalancer(ожидается 80:80/TCP,443:443/TCP)
`kubectl -n ingress-nginx get svc | grep 'LoadBalancer'`

### Проверить резолв http://dev.hfin.local/
`curl http://dev.hfin.local/`