# goalkeeper
单点登录系统

## 安装依赖
    1、pip install -r requirement.txt
 
## 建立数据库步骤
    1、flask db init 
    2、flask db migrate -m "create tables" 
    3、flask db upgrade

## 数据库交互
    flask shell

## 添加.env文件
    在根目录添加.env文件，内容如下
    FLASK_APP=goalkeeper.py
    FLASK_DEBUG=1
    FLASK_ENV=development


## 运行
    flask run --host=127.0.0.8 --port=8888
