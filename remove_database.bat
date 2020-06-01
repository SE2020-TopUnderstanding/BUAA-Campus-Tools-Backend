cd course_query
rm -rf migrations
cd ..

cd ddl_query
rm -rf migrations
cd ..

cd empty_room_query
rm -rf migrations
cd ..

cd ping
rm -rf migrations
cd ..

cd post_web_spider
rm -rf migrations
cd ..

cd request_queue
rm -rf migrations
cd ..

cd score_query
rm -rf migrations
cd ..

cd tests_query
rm -rf migrations
cd ..

cd user_feedback
rm -rf migrations
cd ..

cd user_login
rm -rf migrations
cd ..

cd version_information
rm -rf migrations
cd ..

py manage.py makemigrations course_query
py manage.py makemigrations ddl_query
py manage.py makemigrations empty_room_query
py manage.py makemigrations ping
py manage.py makemigrations post_web_spider
py manage.py makemigrations request_queue
py manage.py makemigrations score_query
py manage.py makemigrations tests_query
py manage.py makemigrations user_login
py manage.py makemigrations user_feedback
py manage.py makemigrations version_information
py manage.py migrate
