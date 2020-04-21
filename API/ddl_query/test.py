#数据库中实验2020-3-19 下午11:55
#标准时间2020-04-01 02:03:00

def add_0(s):
    if int(s)<10:
        s = "0" + s
    return s

def standard_time(t):
    temp = t.split("-")
    year = temp[0]
    month = add_0(temp[1])
    
    temp2 = temp[2].split(" ")
    day = add_0(temp2[0])
    
    time = ""
    type = 0
    if "上午" in temp2[1]:
        time = temp2[1].replace('上午','')
    elif "下午" in temp2[1]:
        type = 1#代表下午
        time = temp2[1].replace("下午",'')
    temp3 = time.split(":")

    if type == 0:
        hour = add_0(temp3[0])
    else:
        hour = str(int(temp3[0])+12)
    minute = add_0(temp3[1])

    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"

print(standard_time("2020-12-9 上午9:5"))
#标准时间2020-04-01 02:03:00