# Twitter Python Tips with API

This is just an extension of the
[twitter python tips](https://github.com/stephenoba/twitter_python_tips) project.

Follow same steps in the [twitter python tips](https://github.com/stephenoba/twitter_python_tips)
project then add the following to your .env file;
- ```GOOGLE_FORM_URL``` this is a url to the [@python_tip google form](https://docs.google.com/forms/d/e/1FAIpQLScsHklRH2-uplGYH_vxhtIin-zJS44bXQkAWCH7_N7nUdrGXw/viewform) or a form of similar structure.
- ```GOOGLE_FORM_PYTHON_TIP_FIELD``` this is the input name (i.e ```<input name="get-this-value">```) of the python tip field.
- ```GOOGE_FORM_TWITTER_ID_FIELD``` same as above but for the twitter id field.
- ```GOOGLE_FORM_EMAIL_FIELD``` same as above but for the email field.

Start your server ```python manage.py runserver``` and got to
[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) to see the list of
available endpoints.
