#!/bin/bash 
echo "start tweeting" 
# please edit it as per your project configuration
cd $(dirname -- ${BASH_SOURCE[0]})
source venv/bin/activate && python manage.py send_scheduled_posts && deactivate >> ./logs/tweet.log
cd -
#echo "end tweeting"
