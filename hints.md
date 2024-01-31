# Общие подсказки по проекту

## Docker
### билд образа
docker build . -t 838375350179/hf:latest

### пуш образа
docker push 838375350179/hf:latest

## Kubectl
### создание пространтсва имён
kubectl create namespace hfin

### добавить креды для docker registry
minikube addons configure registry-creds
minikube addons enable registry-creds
minikube kubectl -- get pods -n kube-system | grep registry-creds

### деинсталирование
helm uninstall hfin -n hfin

### инсталирование
helm install hfin ./helm -n hfin -f ./helm/values.staging.yaml

### получение сервисной информации
kubectl get pods -A |grep "hfin"

### получение подробной информации
kubectl -n hfin describe pod hfin-7c7ffbbbb8-lqj69
    
### получение логов контейнера
kubectl -n hfin logs hfin-7c7ffbbbb8-lqj69
    
### переход внутрь процесса контейнера
kubectl -n hfin exec -it hfin-958b7fbc7-grrbh  bash


### получить логи прединициализируемых контейнеров
kubectl logs -f -n hfin hfin-7f95b8ff64-hghnc -c hfin-init-postgress

### информация с IPs
kubectl -n hfin get pod -o wide

### информация по службам
kubectl get svc nginx -o wide

### информация о ноде
kubectl get nodes -o wide


## Minikube
### генерация тунелей в миникубе
minikube tunnel

### APP
### рабочий урл
лежи в hfin.root.settings.CSRF_TRUSTED_ORIGINS

## MetalLB

### разрешить ARP
kubectl get configmap kube-proxy -n kube-system -o yaml | sed -e "s/strictARP: false/strictARP: true/" | kubectl apply -f - -n kube-system
### подключить Metallb
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"