### 接口规格（暂定）

| #    | 请求方法 | 请求路径                                               | 用途                       |
| ---- | -------- | ------------------------------------------------------ | -------------------------- |
| 1    | post     | /api/users/phone_num/verify/code                       | 手机验证发送验证码         |
| 2    | post     | /api/users/phone_num/verify                            | 验证验证码是否正确         |
| 3    | post     | /api/users/email/verify                                | 验证邮箱，给邮箱寄信       |
| 4    | get      | /api/users/email/verify/:uid/:hash_code                | 验证邮箱，邮箱点击链接返回 |
| 5    | post     | /api/users/forgetpassword/email                        | 忘记密码，绑定的邮箱       |
| 6    | get      | /api/users/forgetpassword/email/verify/:uid/:hash_code | 忘记密码，邮箱转跳         |
| 7    | post     | /api/users/forgetpassword/phone_num/send               | 忘记密码，手机             |
| 8    | post     | /api/users/forgetpassword/phone_num/verify             | 忘记密码，手机验证         |
| 9    | get      | /api/users/:uid/get_class                              | 获取课表                   |
| 10   | get      | /api/users/:uid/update_class                           | 更新课表                   |
| 11   | get      | /api/users/:uid/todolist                               | 课程中心ddl查询            |
| 12   | get      | /api/empty_room                                        | 空教室查询                 |
| 13   | get      | /api/users/:uid/get_score                              | 成绩查询                   |
|      |          |                                                        |                            |
|      |          |                                                        |                            |