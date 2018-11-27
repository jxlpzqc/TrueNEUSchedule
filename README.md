# 任务报告  
任务五：真●课程表

## 项目介绍
首次登陆时，自动从教务处导入课表并保存到数据库  

## 项目部署
1. 配置好MySQL
2. 在MySQL中创建数据库
```SQL
create database trueneu;
```
3. 将settings.py的7-11行修改为对应设置
```python
#实例
SQL_USERNAME = 'root' #数据库账户
SQL_PASSWORD = '123456' #数据库密码
SQL_HOSTADDRESS = 'localhost' #数据库主机名
SQL_HOSTPORT = '3306' #数据库服务端口
SQL_DATABASE = 'trueneu' #数据库名
```
4. 运行setup.py
```
python setup.py
```
5. 启动main.py
```
python main.py
```
6. 打开浏览器，访问[http://localhost:5000/](http://localhost:5000/)测试是否运行正常

## 所需要的库  
- Flask  
- Flask-SQLAlchemy  
- pymysql  
- requests
- beautifulsoup4
```
pip install Flask
pip install Flask-SQLAlchemy
pip install pymysql
pip install requests
pip install beautifulsoup4
```
还可以通过以下的方式一键安装
```
pip install -r requirements.txt
```
## 实现细节
1. 采用Requests库、Flask MVC框架和Flask-SQLALchemy ORM库，实现了基本功能  
2. 前端部分采用了Bootstrap框架做响应式布局  
3. 使用了Ajax请求服务器内容，大大改善了用户体验  
4. 将模型、控制器、工具函数、设置文件、启动函数分离到不同的文件，实现了解耦

## 心得
1. 学会使用IDE了，PyCharm比notepad++好用了太多有木有
2. 搞清楚了Python包和模块的概念，会多文件啦，哈哈哈
3. Flask的session只能保存Json Serializable对象，说白了就是可以变成文本类型，之后又可以转换回来的对象，这个设计相对于其他框架的Session可以存储Object，就很不合理了
4. PyCharm贼好用贼好用，自从有了Pycharm，就再也没有了编译错误，哈哈哈哈哈，一键格式化代码好好用有木有，JB万岁JB万岁，哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈（**此处省略100万字**）（**此处省略100万字**）（**此处省略100万字**）

## 缺陷  
- 窄屏下bootstrap表格会出现错乱的情况，所以移动端不能设置width=device-width，影响了用户体验

## 仍未解决的问题  
还是部署啦，具体描述在[MyPatebin](https://github.com/jxlpzqc/MyPastebin#%E4%BB%8D%E6%9C%AA%E8%A7%A3%E5%86%B3%E7%9A%84%E9%97%AE%E9%A2%98)中有写到

## Demo
 [直接点](http://host.chengziqiu.top:8080)就好了吧，哈哈  
 [http://host.chengziqiu.top:8080](http://host.chengziqiu.top:8080)

