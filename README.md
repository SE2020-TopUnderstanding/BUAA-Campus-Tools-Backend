# 航胥——北航教务助手

本项目为北京航空航天大学2020年“软件工程”课程项目——“航胥”，一款更想要了解你的北航教务助手，后端项目采用的框架为Django框架。

<img src="https://img2020.cnblogs.com/blog/1972959/202004/1972959-20200429101110927-296558721.png" style="zoom:50%" />



## **上手指南**

以下指南将帮助你在本地机器上安装和运行该项目，进行开发和测试。关于如何将该项目部署到在线环境，请参考部署小节。

**基础环境**

Python 3.7+

**安装步骤（windows环境）**

1. 克隆项目：

   选择一个文件夹作为git根目录，在命令行中执行

   `git clone https://github.com/SE2020-TopUnderstanding/BUAA-Campus-Tools-Backend.git`

   将本项目克隆到本地。

2. 安装依赖：

   首先进入项目路径

   `cd BUAA-Campus-Tools-Backend`

   再在命令行中执行

   `pip install -r requirements.txt`

   本地运行不需要PyMySQL，本地运行默认使用的是自带的Sqlite3轻量级数据库。

3. 执行数据库迁移（非必须）：

   在相同路径下，命令行中执行

   `python manage.py makemigrations`

   `python manage.py migrate`

4. 运行框架：

   在相同路径下，命令行中执行：

   `python manage.py runserver`

   若出现以下提示信息，则本地运行成功，可以在浏览器中访问相应的接口

   ```
   System check identified no issues (0 silenced).
   May 11, 2020 - 11:42:14
   Django version 3.0.5, using settings 'API.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

## 测试

**单元测试：**

若想运行单元测试，请在项目的根目录下执行：

`python manage.py test`

**代码风格测试**：

本项目采用的代码风格标准为pylint，具体内容可以参考.pylintrc文件

若想运行代码风格测试，请在项目的根目录下执行：

`pylint BUAA-Campus-Tools-Backend `

## 部署

部署部分请等待补充完成。

## 使用到的框架

Django - Web应用框架

## Wiki Link

[wiki主页](https://github.com/SE2020-TopUnderstanding/BUAA-Campus-Tools-Backend/wiki)

