## 航胥——爬虫模块

#### **基础环境** 

Python 3.7

#### **本地开发**

本小节介绍如何在本地建立开发测试环境

1. 克隆项目

选取安装文件夹，在文件夹内执行克隆命令

`git clone -b insert https://github.com/SE2020-TopUnderstanding/BUAA-Campus-Tools-Backend.git`

2. 安装环境依赖

进入项目路径，在命令行中通过requirements.txt安装依赖

`cd BUAA-Campus-Tools-Backend`

`pip install -r requirements.txt`

#### **模块运行方法**

`python interface.py -d 整数` 启动ddl的更新爬虫程序，输入的整数为爬虫的id

`python interface.py -o 整数` 启动课表、空教室、成绩的更新爬虫程序，输入的整数为爬虫的id

`python interface.py -r 整数` 启动ddl、课表、成绩的消息队列处理程序，输入的整数为爬虫的id

#### 代码风格测试

本模块使用pylint检查代码风格，具体标准请参考.pylintrc文件

进行代码风格测试的方法

在命令行中执行`pylint --rcfile .pylintrc -rn BUAA-Campus-Tools-Backend`命令

#### 爬虫在服务器上的部署

本节内容有待补充

#### Wiki Link

[项目wiki](https://github.com/SE2020-TopUnderstanding/BUAA-Campus-Tools-Backend/wiki)



