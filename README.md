





# 接口说明文档

## 1. 接口规格

| #    | 请求方法 | 请求路径                                | 用途               |
| ---- | -------- | --------------------------------------- | ------------------ |
| 1    | get      | 114.115.208.32:8000/timetable           | 获取课表           |
| 2    | post     | 114.115.208.32:8000/timetable           | 增加数据/请求更新  |
| 3    | get      | 114.115.208.32:8000/score               | 获取成绩           |
| 4    | post     | 114.115.208.32:8000/score               | 增加数据           |
| 5    | get      | 114.115.208.32:8000/tests               | 获取考期表         |
| 6    | post     | 114.115.208.32:8000/tests               | 增加数据           |
| 7    | get      | 114.115.208.32:8000/request             | 获取请求           |
| 8    | post     | 114.115.208.32:8000/request             | 完成请求反馈       |
| 9    | post     | 114.115.208.32:8000/request/timetable/  | 请求更新课表       |
| 10   | post     | 114.115.208.32:8000/request/score/      | 请求更新成绩       |
| 11   | post     | 114.115.208.32:8000/request/ddl/        | 请求更新ddl        |
| 12   | post     | 114.115.208.32:8000/request/empty_room/ | 请求更新空教室     |
| 13   | post     | 114.115.208.32:8000/login/              | 登录               |
| 14   | get      | 114.115.208.32:8000/classroom/          | 空教室查询         |
| 15   | get      | 114.115.208.32:8000/ddl/                | ddl查询            |
| 16   | get      | 114.115.208.32:8000/login/              | 获取所有用户名密码 |
| 17   | post     | 114.115.208.32:8000/classroom/          | 添加空教室数据     |
| 18   | post     | 114.115.208.32:8000/ddl/                | 添加ddl数据        |



## 2. 接口使用说明

- 服务器IP地址：114.115.208.32:8000

### 课表查询接口：

- get请求（前端用）：

    **请求方法1：114.115.208.32:8000/timetable/?student_id=(:id)&week=(:week)**

    ---

    **参数说明：**

    - **student_id**: 表示所查询学生的学号，例如17373333
    - **week**: 表示所查询的周数，例如3，或者all，表示查询总课表

    举例：114.115.208.32:8000/timetable/?student_id=17373333&week=3

    查询学号为17373333，第三周的课表

    **http返回值：**

    - **200**：请求成功，并返回信息(json格式)：

    ```json
    [
        {
            "name": "计算机网络",
            "teacher_course": [
                {
                    "name": "罗洪斌"
                }
                {
                    "name": "张辉"
                }
            ],
            "time": "周2 第1，2节",
            "place": "(一)301",
            "week": "1,2,3,4,5,6,7,8,9,",
            "semester": "2020_Spring"
        }
    ]
    ```

    - **400**：请求失败，参数个数不正确或参数内容不正确

        ​	例：114.115.208.32:8000/timetable/?student_id=17373456

        ​	或：114.115.208.32:8000/timetable/?love_you=17373456

    **请求方法2：114.115.208.32:8000/timetable/?date=(Y-m-d)**

    ---

    **参数说明：**

    - **date**: 表示日期#格式为Y-m-d，例如2020-4-21

    举例：114.115.208.32:8000/timetable/?date=2020-4-21

    查询2020年4月21日是本学期第几周

    **http返回值：**

    - **200：**表示成功，返回对应周数信息

    ```json
    [
        {
            "week": "1"
        }
    ]
    ```

    - **400：**参数错误，或数量不正确

- post请求（爬虫用）：

    **请求方法1：114.115.208.32:8000/timetable/ 附带json格式的信息**

    ---

    **json信息格式：**

    - 第一项：'student_id' = (:id)
    - 第二项：info列表, info里包含每一节课的信息，若有多节课则按列表排列（按顺序，5项）：
        - 课程名称
        - 课程地点
        - 课程教师
        - 课程持续周
        - 课程时间

    举例：114.115.208.32:8000/timetable/

    json文件：

    ```json
    {
        "student_id": "17373010", 
        "info": [
            [
                [
                    "计算机网络", 
                    "(一)301", 
                    "罗洪斌", 
                    "1-9", 
                    "周2 第1，2节"
                ]
            ]
    }
    ```
    表示请求将上述信息加入数据库
    
    **http返回值：**
    
    - **201**：表示成功创建
    - **400**：表示json文件没有按照约定的格式传输
    - **404**：表示没有找到请求创建的学生信息
### 成绩查询接口
- get请求（前端用）：
  
    **请求方法1：114.115.208.32:8000/score/?student_id=(:id)&semester=(:semester)**
    
    ---
    
    **参数说明：**
    
    - **student_id**: 表示所查询学生的学号，例如17373333
    - **semester**: 表示所查询的周数，例如2017秋季
    举例：114.115.208.32:8000/semester/?student_id=17373333&semester=2017秋季
    查询学号为17373333，2017秋季学期成绩
    **http返回值：**
    - **200**：请求成功，并返回信息(json格式)：
    ```json
    [
        {
            "course_name": "工科数学分析(1)",
            "credit": 6.0,
            "score": 44
        }
    ]
    ```
    - **400**：请求失败，参数个数不正确或参数内容不正确
    
    **请求GPA: 114.115.208.32:8000/score/gpa/?student_id=(:id)**
    
    ---
    
    **参数说明：**
    
    - **student_id**: 表示所查询学生的学号，例如17373333
    
    **http返回值：**
    
    - **200：成功**
    
    ```json
    {
        "gpa": 4.0000000
    }
    ```
    
    - **404：没有请求的学生**
    - **400：请求错误**
    
    **请求加权平均分: 114.115.208.32:8000/score/avg_score/?student_id=(:id)**
    
    ----
    
    **参数说明：**
    
    - **student_id**: 表示所查询学生的学号，例如17373333
    
    **http返回值：**
    
    - **200：成功**
    
    ```json
    {
        "score": 100.000000000000
    }
    ```
    
    - **404：没有请求的学生**
    - **400：请求错误**
    
- post请求（爬虫用）：
  
    **请求方法1（爬虫用）：114.115.208.32:8000/score/ 附带json格式的信息**
    
    json信息格式：
    - 第一项：'student_id' = (:id)
    - 第二项：'semester' = (:semester)
    - 第三项：info列表, 每个info里包含每个成绩的信息（按顺序，5项）：
        - 课程bid
        - 课程名称
        - 课程学分
        - 课程成绩
    举例：114.115.208.32:8000/score/
    json文件：
    ```json
    {
        "student_id": "17373010", 
        "semember": "2017秋季", 
        "info": [
            [
                "B1A09104A", 
                "工科数学分析(1)", 
                "6.0", 
                "44"
            ]
        ]
    }
    ```
    表示请求将上述信息加入数据库
    **http返回值：**
    ---
    - **201**：表示成功创建
    - **400**：表示json文件没有按照约定的格式传输
    - **404**：表示没有找到请求创建的学生信息
### 消息队列接口
- get请求：
  
    **请求方法1：114.115.208.32:8000/request/**
    
    ---
    
    获取消息队列中的请求
    **http返回值：**
    
    - **200：**成功，返回请求的具体信息
    ```
    {'req_id': req_id, 'usr_name': student.usr_name, 'password': student.usr_password,
    'req_type': req_type}
    ```
    - **204：**成功，但是没有需要处理的请求
    **请求方法2：114.115.208.32:8000/request/?id=(:id)**
    ---
    询问指定id的请求是否已完成
    参数列表：
    - **id：**req_id
    **http返回值**：
    - **200：**成功，返回信息
        ```
        [
        	{
        		"status" = true/false
        	}
        ]
        ```
    - **400：**参数不正确
    
- post请求：
  
    **请求方法1：114.115.208.32:8000/request/**
    
    ---
    
    爬虫反馈已完成任务的id
    **json格式：**
    
    ```json
    [
    	{
    		"req_id" = 14
    	}
    ]
    ```
    **http返回值：**
    - **200：**成功
    - **404：**找不到这个id的请求
    - **400：**参数错误
    
- 其他路径的请求：
    **请求方法：114.115.208.32:8000/request/(timetable/score/ddl/emptyroom/)/?student_id=(:id)**
    
    ---
    
    请求更新对应页面指定同学的数据
    **http返回值：**
    
    - **200：**成功，返回请求的id
    ```
    [
    	{
    		"id" = 1
    	}
    ]
    ```
    - **400：**参数错误
    - **404：**未找到该学号的同学的信息
### 前端
- 登录
  - 访问方法
    POST
    ```
    http --form POST http://127.0.0.1:8000/login/ usr_name="mushan" usr_password="132"
    ```
  - 返回结果
    ```
    成功：
    {
        "name": "胡彬彬",
        "state": 1,
        "student_id": "17373349"
    }
    失败
    {
        "name": "",
        "state": 0,
        "student_id": ""
    }
    ```
- 空教室查询
  - 访问方法
    GET
    ```
    http://114.115.208.32:8000/classroom/?campus=学院路校区&date=2020-04-20&section=1, 2, 3,
    ```
  - 访问结果
    ```
    访问成功:
    {
        "一号楼": [
            {
                "classroom": "(一)203"
            },
            {
                "classroom": "(一)205"
            }
        ]
    }
    ```
- ddl查询
  - 访问方法
    GET
    ```
    http://127.0.0.1:8000/ddl/?student_id=17373349
    ```
  - 访问结果
    ```
    成功
    [
        {
            "name": "计算机科学方法论",
            "content": [
                {
                    "homework": "第二次作业",
                    "ddl": "2020-04-23 02:03:00",
                    "state": "未提交"
                },
                {
                    "homework": "第一次作业",
                    "ddl": "2020-04-28 04:03:00",
                    "state": "提交"
                }
            ]
        },
        {
            "name": "计算机图形学",
            "content": [
                {
                    "homework": "第一次作业",
                    "ddl": "2020-04-23 04:03:00",
                    "state": "提交"
                }
            ]
        }
    ]
    失败
    [
        {
            "name": "错误",
            "content": [
                {
                    "homework": "抱歉，我们暂时无法获取您的ddl信息。\\n为解决此问题，请在课程中心的用户偏好标签页面保证您所需爬取的课程都属于收藏站点或活跃站点，并且活跃站点不要为空",
                    "ddl": "",
                    "state": "错误"
                }
            ]
        }
    ]
    ```
### 爬虫
- 获取其中某个服务器的用户名和密码
  
  - 访问方法
    
    GET
    
    ```
    http://127.0.0.1:8000/login/?password=123&number=1
    ```
    
  - 返回结果
  
    ```
    成功:
    [
        {
            "usr_name": "hhh",
            "usr_password": "h101"
        },
        {
            "usr_name": "mushan",
            "usr_password": "h102"
        },
        {
            "usr_name": "o",
            "usr_password": "h103"
        }
    ]
    
    失败:
    {}
    ```
  
    
  
- 获取所有用户名和密码
  
  - 访问方法
    GET
    ```
    http://127.0.0.1:8000/login/?password="123"
    ```
  - 返回结果
    ```
    成功:
    [
        {
            "usr_name": "hhh",
            "usr_password": "h101"
        },
        {
            "usr_name": "mushan",
            "usr_password": "h102"
        },
        {
            "usr_name": "o",
            "usr_password": "h103"
        }
    ]
    
    失败:
    {}
    ```
  
- 插入空教室信息
  - 访问方法
    POST
    ```
    http://127.0.0.1:8000/classroom/
    ```
  - 需要json包
    ```
    [
                    {
                        "campus":"学院路校区",
                        "content":[
                            {
                                "teaching_building":"一号楼",
                                "classroom":"(一)203",
                                "date":"2020-04-20",
                                "section":"1,2,3,4,5,7,"
                            },
                            {
                                "teaching_building":"一号楼",
                                "classroom":"(一)204",
                                "date":"2020-04-20",
                                "section":"1,2,3,4,7,"
                            }
                            {
                                "teaching_building":"三号楼",
                                "classroom":"(三)202",
                                "date":"2020-04-20",
                                "section":"3,4,5,7,8,"
                            }
                        ]
                    },
                    {
                        "campus":"沙河校区",
                        "content":[
                            {
                                "teaching_building":"三号楼",
                                "classroom":"(三)202",
                                "date":"2020-04-20",
                                "section":"3,4,5,7,8,"
                            }
                        ]
                    }
                ]
    ```
  
- ddl信息插入
  - 访问方法
    POST
    ```
    http://127.0.0.1:8000/ddl/
    ```
  - 需要json包
    ```
    {
                "student_id":"17373349",
                "ddl":[
                        {
                            "content":[
                                {
                                    "ddl":""2020-3-10 下午11:55",
                                    "homework":"第一次作业",
                                    "state":"提交"
                                },
                                {
                                    "ddl":""2020-3-10 下午11:55",
                                    "homework":"第二次作业",
                                    "state":"未提交"
                                }
                            ],
                            "name":"计算机科学方法论"
                        },
                        {
                            "content":[
                                {
                                    "ddl":""2020-3-10 下午11:55",
                                    "homework":"第一次作业",
                                    "state":"提交"
                                }
                            ],
                            "name":"计算机图形学"
                        }
                    ]
            }
    ```
    



### 版本数据库

- 前端

  - 访问方法

    GET

    ```
     http://127.0.0.1:8000/version/
    ```

  - 返回结果

    ```
    {
        "version_number": "1.1.1",
        "update_date": "2020",
        "announcement": "hh",
        "download_address": "22"
    }
    ```

    最新的版本号，更新日期，更新公告，下载地址

- PM

  - 访问方法

    POST

    ```
     http://127.0.0.1:8000/version/
    ```

  - 需要json包

    ```
    {
        "version_number": "1.1.1",
        "update_date": "2020",
        "announcement": "hh",
        "download_address": "22"
    }
    ```

  - 返回结果

    ```
    {
        "state": "成功"
    }
    {
        "state": "新版本号已有"
    }
    {
        "state": "参数错误"
    }
    {
        "state": "参数数量不正确"
    }
    ```

    分别对应于不同的插入情况



### 2020.4.28新增功能

- 删除数据库和消息队列中的某个用户（在error_handling app中）

  - 访问方法

    POST

    ```
    http://127.0.0.1:8000/delete/
    ```

  - 需要参数

    用户名和密码

    {
    	"usr_name":"mushan",
    	"password":"1"
    }

  - 返回结果

    ```
    {
    	"state":1
    }
    ```

    如果数据库中无该学生，返回0

    如果数据库中密码不相同，返回-1

    如果成功删除返回1
