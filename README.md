### 接口规格（暂定）

| #    | 请求方法 | 请求路径               | 用途            |
| ---- | -------- | ---------------------- | --------------- |
| 1    | post     | /api/users/verify      | 用户验证        |
| 2    | get      | /api/users/timetable   | 获取课表        |
| 3    | get      | /api/users/score       | 获取成绩        |
| 4    | get      | /api/users/todolist    | 获取课程中心ddl |
| 5    | get      | /api/users/empty_rooms | 获取空教室      |
| 6    | get      | /api/users/tests       | 获取考试时间表  |
|      |          |                        |                 |
|      |          |                        |                 |

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
        # 没有提供参数或提供参数不正确，均返回404错误
        ```



- 登录

  - 访问方法

    ```
    http http://114.115.208.32:8000/login/ usr_name="123" usr_password="321"
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
    http http://127.0.0.1:8000/query/classroom/ campus="学院路校区" date="2020-04-13" section="1,2,"
    
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
    http http://127.0.0.1:8000/query/dll/ student_id="1"
    ```

  - 访问结果

    ```
    {
        "计网": [
            {
                "dll": "2010-10-11",
                "homework": "团队作业",
                "state": "已提交"
            }
        ],
        "软工": [
            {
                "dll": "2010-10-9",
                "homework": "团队作业",
                "state": "已提交"
            },
            {
                "dll": "2010-10-10",
                "homework": "个人作业",
                "state": "已提交"
            },
            {
                "dll": "2010-10-12",
                "homework": "最后一次作业",
                "state": "未提交"
            },
            {
                "dll": "2010-10-13",
                "homework": "团队作业",
                "state": "未提交"
            }
        ]
    }
    ```

    