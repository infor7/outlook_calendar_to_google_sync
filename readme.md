# For who is that software

Container allows to automatically synchronization of outlook calendar to google calendar. The software has been created to ommit limitations made by too strict security policy which blocks sync from outlook calendar to google calendar.


# Quickstart

  
1. Generate own credentials for google calendar API at:
https://developers.google.com/calendar/quickstart/python
2. Put the generated credentials.json file to src directory
3. Export proxy, if needed, to environmental variables: OUTLOOK_PROXY, GOOGLE_PROXY
`export OUTLOOK_PROXY=`
`export GOOGLE_PROXY=http://1.2.3.4:8080`
4. Export necessary envs. **Calendar used in GOOGLE_CALENDAR env will be cleared each time.**
`export OUTLOOK_EMAIL=email
export OUTLOOK_PASSWORD=password_to_email
export GOOGLE_CALENDAR=<calendar-id>@group.calendar.google.com`
5. First run both scripts locally to fulfill authentication. Google will open security alert page in your browser.  `https_proxy=$OUTLOOK_PROXY python src/outlook_downloader.py`
`https_proxy=$GOOGLE_PROXY python src/google_calendar_feeder.py`
6. Build Docker
`docker build --build-arg proxy=<optional-proxy> -t outlook_google_calendar .`
8. Run docker
`docker run --name outlook_google -e OUTLOOK_EMAIL=<email> -e OUTLOOK_PASSWORD=<password> -e OUTLOOK_PROXY=<optional-proxy> -e GOOGLE_PROXY=<optional-proxy> -e GOOGLE_CALENDAR=<calendar-id>@group.calendar.google.com -t -d outlook_google_calendar`

# Developer guide
1. Create virtual env 
`virtualenv venv --python=python3.8`
2. Activate virtual env
`source venv/bin/activate`
4. Download requirements
`pip install -r src/requirements.txt`
5. Export envs - OUTLOOK_PROXY, GOOGLE_PROXY, GOOGLE_CALENDAR


License: MIT
