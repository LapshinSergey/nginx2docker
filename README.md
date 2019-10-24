# nginx2docker

Утилита добавления конфигурационного файла nginx проксирующего входящий трафик c nginx на docker контейнер с автоматическим назначением свободного порта из определенного пула. Служит для быстрого добавления конфигурационных файлов nginx при большом количестве ежедневных сборок web-проектов и их быстрого тестирования, а затем очистки.

## Быстрый старт

Для получения свободного порта используйте:
`./nginx2docker.py freeport`

Для запуска демона:
`./nginx2docker.py daemon`

Для запуска контейнера на первом свободном пору (где test.lapshin.pro - hostname который необходимо привязать):
`./nginx2docker.py add-to-pool test.lapshin.pro`

### Возможности:
* Получение первого tcp свободного порта из пула;
* Создание конфигурационного файла nginx;
* Запуск контейнера и его привязка;
* Возможность привязать Let's Encrypt сертификат для домена; (в разработке)
* Запуск в виде REST-сервиса; (в разработке)
* Очистка;
* Работа в контейнере; (в разработке)

## Установка для CentOs 7:

Установка nginx:
yum install nginx -y

Установка интерпретатора python и дополнительных модулей:
yum install python3 python3-devel -y
pip3 install flask psutil termcolor

Для поддержки SSL от Let's Encrypt необходимо установить:
yum install certbot python2-certbot-nginx

## Использование nginx2docker в контейнере.
Утилита nginx2docker может использоваться в контейнерном исполнении, в таком случае она уже будет иметь nginx и все необходимые модули.

Проброс портов на хост машине (firewalld):
firewall-cmd --zone=public --add-masquerade --permanent
firewall-cmd --zone=public --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=172.17.0.1 --permanent
firewall-cmd --reload

Если используете iptables:
Для возможности проброса портов необходимо включить переадресацию трафика на уровне ядра
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sysctl -w net.ipv4.ip_forward=1

Пробросить порт 9006 на 80 порт сервера 10.200.16.216
iptables -t nat -A PREROUTING -i eth2 -p tcp --dport 9006 -j DNAT --to-destination 10.200.16.216:80
iptables -t nat -A POSTROUTING -o eth0 -p tcp --dport 80 -d 10.200.16.216 -j SNAT --to-source 10.200.16.227
service iptables save

... в разработке
