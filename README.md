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
|      |          |                        |                 |
|      |          |                        |                 |
|      |          |                        |                 |
|      |          |                        |                 |
|      |          |                        |                 |
|      |          |                        |                 |

## 数据元素定义

- 课程：只有BID、上课周、上课时间、教师、教室、学期完全相同才算同一门课
    - 一周上两次的课也会算作两门不同的课
    - 主键为我们自己定义的id
    - 由于调课现象的存在，应该只能如此来区分
