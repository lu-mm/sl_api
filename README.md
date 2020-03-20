### 项目功能简单说明：
```text
资产使用ansible作为接口，需要将连接的服务按ansible方式配置好file/ansible_cmdb_file/hosts
确保ansible可以连接所配置服务器后
先进行更新资产接口，可以获取所以资产的硬件信息，详细看接口信息


目前提供接口
/api #swagger api 接口
/assets/index.html  #资产页面

```


### 环境：
```bash
centos 7.4
Python 3.6.3
```


---
### Linux环境安装python 3.6
```bash
# install package
yum install -y zlib* gcc gcc-c++ openssl openssl-devel sqlite-devel


wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz

tar zxvf Python-3.6.3.tgz
cd Python-3.6.3
./configure \
--with-ssl \
--prefix=/usr/local/python3.6


make && make install

#添加环境变量
vim /etc/profile
----------
export PATH=$PATH:/usr/local/python3.6/bin
----------
source /etc/profile

# 安装pipenv
pip3 install --upgrade pip
pip3 install pipenv

```
### 项目配置
```bash
#配置项目环境变量，并修改对应数据库连接，环境为develop或者product
vim /etc/profile
export FLASK_ENV="develop"
source /etc/profile

# 配置文件路径
sl_api/utils/settings.py

#准备数据库
create database dbname CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


#修改对应环境mysql数据库连接
 DATABASE = {
        'host': '',
        'port': ,
        'user': '',
        'password': '',
        'db': '',
        'charset' :'',
    }
# 对应修改配置文件的其他相关信息


```
### 安装Python虚拟环境
```bash
# 在项目当前目录下面
pipenv install 
```

### Linux 环境部署服务启动
```bash
# 先进入虚拟环境
pipenv shell
#保证当前目录是项目目录下
# 运行sl_api_install.sh
sh sl_api_install.sh
```

### 验证是否成功
```bash
systemctl status sl_api
netstat -lntp | grep 5000
```





