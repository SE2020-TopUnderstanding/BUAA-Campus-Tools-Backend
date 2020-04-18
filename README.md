### 接口规格（暂定）

| #    | 请求方法 | 请求路径             | 用途            |
| ---- | -------- | -------------------- | --------------- |
| 1    | post     | hostname/login       | 用户验证        |
| 2    | get      | hostname/timetable   | 获取课表        |
| 3    | get      | hostname/score       | 获取成绩        |
| 4    | get      | hostname/todolist    | 获取课程中心ddl |
| 5    | get      | hostname/empty_rooms | 获取空教室      |
| 6    | get      | hostname/tests       | 获取考试时间表  |
| 7    | post     | hostname/timetable   | 添加数据        |
| 8    | post     | hostname/score       | 添加数据        |

## 数据元素定义

- 课程：只有BID、上课周、上课时间、教师、教室、学期完全相同才算同一门课
    - 一周上两次的课也会算作两门不同的课

    - 主键为我们自己定义的id

    - 由于调课现象的存在，应该只能如此来区分

    - 查询参数及返回值：

        ```
        # 可使用的参数有：
        # student_id: 附带学生学号，查询指定学生课表
        # semester: 附带学年学期，查询指定学期课表
        # week: 附带周数，查询指定周的课表，若参数值为all,则查询该学期全部周的课表
        # 例：127.0.0.1/timetable?student_id=17333333&semester=2020_Spring&week=3
        # 查询学号为17373333 2020春季学期第三周课表
        # 没有提供参数或参数数量正确，返回400错误
        # 参数类型不正确，返回404错误
        ```


- 登录

  - 访问方法

    ```
    http --form GET http://127.0.0.1:8000/login/ usr_name="mushan" usr_passwor="132"
    ```

  - 结果

    ```
    {
        "state": 1
    }
    state为1代表访问成功
    state为0代表访问失败
    ```

- 查询空教室

  - 访问方法

    ```
    http://127.0.0.1:8000/classroom/?campus=新主楼&date=2020-4-18&section=1,2,3,
    
    注意，由于只查询连续的节数所以若查询1-3节请将section设为"1,2,3,"
    ```

  - 访问结果

    ```
    {
        "一号楼": [
            {
                "classroom": "(一)103"
            },
            {
                "classroom": "(一)104"
            },
            {
                "classroom": "(一)105"
            }
        ],
        "二号楼": [
            {
                "classroom": "(一)105"
            }
        ]
    }
    
    ```

- 查询ddl

  - 访问访问

    ```
    http://127.0.0.1:8000/ddl/?student_id=17373349
    ```

  - 访问结果

    ```
    
    {
        "计算机网络": [
            {
                "ddl": "2020-4-17 10:02",
                "homework": "实验报告",
                "state": "提交"
            }
        ],
        "软件工程": [
            {
                "ddl": "2020-4-18 9:02",
                "homework": "结对项目",
                "state": "提交"
            },
            {
                "ddl": "2020-4-19 9:02",
                "homework": "个人项目",
                "state": "未提交"
            },
            {
                "ddl": "2020-4-17 14:10",
                "homework": "团队项目",
                "state": "未提交"
            }
        ]
    }
    ```
  
- 成绩：

    ```
        # 参数1:学生学号 e.g. 17373333
        # 参数2：学期 e.g.2020_Spring
        # 没有提供参数或参数数量正确，返回400错误
    	# 参数类型不正确，返回404错误
        # 例:127.0.0.1/score?student_id=11111111&semester=2020_Spring
        # 获得学号为11111111，2020春季学期的成绩
    ```

- 考期表：

    ```
        # 参数1：student_id e.g.17373333
        # 参数2：semester e.g. 2020_Spring
        # 参数3: week e.g. 19
        # 没有提供参数或参数数量正确，返回400错误
    	# 参数类型不正确，返回404错误
        # 例：127.0.0.1/tests?student_id=17373333&semester=2020_Spring&week=19
        # 查询学号为17373333 2020春季学期第19周课表
    ```
