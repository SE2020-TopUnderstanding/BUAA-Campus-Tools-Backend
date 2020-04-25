ps aux | grep chrome | grep -v grep|awk '{print $2}'| xargs kill -9
ps aux | grep python3 | grep -v grep|awk '{print $2}'| xargs kill -9