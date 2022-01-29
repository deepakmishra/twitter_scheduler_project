
# Twitter Scheduler
This project is not as per standard because I made this project for a marketing friend to help him schedule tweets. So made it using django admin not views.

---
## Installation

1. Install *python*, *pip*, *virtualenv*.
2. Clone this repository `git clone https://github.com/deepakmishra/twitter_scheduler_project`.
3. Go to project directory `cd twitter_scheduler_project`.
4. Create virtual environment `virtualenv venv` and `source venv/bin/activate`.
5. Install requirements `pip install -r requirements.txt`.
6. Run server `python manage.py runserver`.
7. Go to browser http://localhost:8000/admin/.
8. Login with username: *admin* and password: *admin* and change the password.
9. If the admin UI looks broken and restart the server `python manage.py collectstatic`.
10. Deploy the code in your preferred choice of infra and domain. Mine is deployed as part of http://www.deeptrap.com/.
11. Setup ***crontab*** like in *crontab* file.

---
## For Admin: Create new Twitter User

1. Login to Django Admin. Check *Groups* in *AUTHENTICATION AND AUTHORIZATION*. There will be a *Twitter User* group.
2. Go to *Users* in *AUTHENTICATION AND AUTHORIZATION*. Add new user with username, password, email, ***is staff user*** access and ***Twitter User*** group access. 
3. Go to *Credentials* in *TWITTER_SCHEDULER_APP*. Add credentials record for the user with empty twitter credentials.

---
## For Twitter User: Setup Twitter App and get Credentials

1. Go to [Twitter App](https://developer.twitter.com/en/portal/projects-and-apps).
2. Create App and enter details.
3. Choose *Production*.
4. **COPY**
    - ***API Key***
    - ***API Key Secret***
    - ***Bearer Token***.
5. Go to *App Settings* -> *User authentication settings* -> *Setup*.
6. Enable *OAuth 2.0* and *OAuth 1.0a*.
7. Type of App *Automated App or bot*.
8. Set App permissions ***Read & Write*** (This is required).
9. Put any *Callback URL* and *Website URL* - http://www.deeptrap.com/ and *Save*.
10. **COPY**
    - ***Client ID***
    - ***Client Secret***
11. Go to *Keys and Tokens* -> *Access Token and Secret* -> *Generate*. Make sure before this step, step 8 is done.
12. **COPY** 
    - ***Access Token***
    - ***Access Token Secret***

---
## For Twitter User: Update Twitter API Credentials and Tweet Post

1. Contact admin to add you as *User*, give you *is staff user* access and *Twitter User* group access and add your blank *Credential*.
2. Login and update API details in your *Credential* [here](http://www.deeptrap.com/admin/twitter_scheduler/credential/).
3. Create scheduled posts in *Post* section [here](http://www.deeptrap.com/admin/twitter_scheduler/post/).
4. Check your twitter account for posts at the scheduled time.
5. If you did not receive in 5 minutes post schedule go to the *Post* [here](http://www.deeptrap.com/admin/twitter_scheduler/post/) and check Twitter response. Contact [me](mailto:deepakmishra117@gmail.com) if you don't understand the response.

---
