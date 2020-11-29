# i-book.in_Archive

我不能够授人以鱼，但是我可以授人以渔。这里是 i-book.in 搜索引擎的归档项目，我不会更新和继续维护这个搜素引擎，你可以拿它去做任何你想做的事情。

另：使用此代码产生的任何风险与利益均与我无关。 切记！请不要在你的网站上留下任何关于 i-book.in 的信息。

-----

# 注意！这只是个框架，没有任何数据，不要想着自己搭建一下，就能够搜索到书了。


下面是一个简单的安装教程，我尽可能写的明白了，如有不清楚的，可以到我的tg群组讨论 : https://t.me/SaltyLeo_blog

### 基本需求

python3、docker

### 搭建说明

首先安装一系列必须的插件与更新。
```
apt install python3-pip
pip3 install flask
pip3 install elasticsearch
pip3 install flask_bootstrap
```

#### 安装 docker版es

```
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && docker pull elasticsearch:6.7.0

cd  /
mkdir -p mnt/elasticsearch
cd  mnt/elasticsearch
mkdir config
mkdir master
mkdir slave
chmod 777 master
chmod 777 slave
cd config
touch master.yml
touch slave.yml
nano master.yml
```
将下列参数粘贴到打开的nano编辑器内。

```
cluster.name: elasticsearch-cluster
node.name: master
network.bind_host: 0.0.0.0
network.publish_host: 127.0.0.1
http.port: 9200
transport.tcp.port: 9300
http.cors.enabled: true
http.cors.allow-origin: "*"
node.master: true
node.data: true
discovery.zen.ping.unicast.hosts: ["127.0.0.1:9300","127.0.0.1:9301"]
```

#### 修改线程限制
```
nano /etc/sysctl.conf
#添加这个
vm.max_map_count=262144 
#保存后执行这个命令
sysctl -p
```

#### 初始化 es搜索引擎

`docker run -e ES_JAVA_OPTS="-Xms256m -Xmx256m" -d -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -v /mnt/elasticsearch/config/master.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /mnt/elasticsearch/master:/usr/share/elasticsearch/data --name es-master elasticsearch:6.7.0`

#### 下载源码

```
wget https://github.com/SaltyLeo/i-book.in_Archive/raw/master/i-book.in.tar.gz && tar -zxvf i-book.in.tar.gz && cd web

#墙内无法访问GitHub使用下面这个
wget https://ibookin-1252237247.cos.ap-shanghai.myqcloud.com/i-book.in.tar.gz && tar -zxvf i-book.in.tar.gz && cd web
```
#### 将索引数据导入到ES
`python3 add2es.py`

可能会弹出以下错误，但请忽略即可。

```
/usr/local/lib/python3.6/dist-packages/elasticsearch/connection/base.py:177: ElasticsearchDeprecationWarning: the default number of shards will change from [5] to [1] in 7.0.0; if you wish to continue using the default of [5] shards, you must manage this on the create index request or with an index template
  warnings.warn(message, category=ElasticsearchDeprecationWarning)
```
#### 运行demo

`python3 web.py`

这时候打开你的服务器IP+端口7743即可打开搜索引擎，例:127.0.0.1:7743，如下图：

![image.png](https://i.loli.net/2020/06/27/WgCpfYdKIl45eF6.png)

### 一些提示

网站的logo以及其他的icon都写死在css中，我改不来，所以没怎么调整，改过的几个png很显而易见。

网站索引文件按照test.json格式导入即可，请注意，add2es这个脚本每次都会清空es索引后再执行导入。

各种链接按需修改，请注意web.py改了return的话，前端html文件也需要改，否则flask会报错。

偶尔docker会卡死使用这个命令重启所有docker `docker restart $(docker ps -a | awk '{ print $1}' | tail -n +2)`

其他的自己摸索吧，对于前端我也不是非常的熟练，


