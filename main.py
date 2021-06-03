import os
from datetime import datetime
from DTO import DTO
from GoogleCalendar import GoogleClient
from Brightspace import BrightSpace


def main():
    os.system("pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    client = GoogleClient('credentials.json')
    brightspace = BrightSpace()
    data = DTO()
    array = ['Theory', 'Labs', 'Assignments']
    creds = input()
    creds = creds.split()
    user = creds[0]
    password = creds[1]
    data.delete_csv(array)
    brightspace.start(user, password)
    for sub in array:
        data.read_csv(sub)
        file = data.get_file()
        client.create_calendars(sub)
        client.erase_calendar(sub)
        client.add_events(file, sub)




if __name__ == "__main__":
    main()
    exit()
