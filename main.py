from DTO import DTO
from GoogleCalendar import GoogleClient
from Brightspace import BrightSpace
import subprocess


def main():
    email = None
    password = None
    client = None
    try:
        subprocess.run("pip install selenium", capture_output=True)
        subprocess.run("pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib",
                       capture_output=True)
        subprocess.run("pip install webdriver-manager", capture_output=True)
    except:
        print("\nError: make sure pip and python3 is properly installed")
    try:
        # credentials.json should be in this folder
        client = GoogleClient('credentials.json')
    except:
        print("\nError: credentials.json needs to be in the current folder")
    try:
        data = DTO()
        email = input("\nEnter algonquin email: ")
        password = input("\nEnter your password: ")
    except:
        print("\nError: Problem getting email and password")
    courses = data.read_txt("courses.txt")
    brightspace = BrightSpace(courses)
    array = ['Theory', 'Labs', 'Assignments']
    data.delete_csv(array)
    print("\nGetting calendar info.")
    try:
        brightspace.start(email, password)
    except:
        print("\nError: A problem occurred while trying to getting brightspace calendar info.")
    try:
        for sub in array:
            print(f'\nUpdating {sub} calendar.')
            data.read_csv(sub)
            file = data.get_file()
            client.create_calendars(sub)
            client.erase_calendar(sub)
            client.add_events(file, sub)
    except:
        print("\nError: A problem occurred while trying to add calendar info to google calendars")
    print("\nUpdated!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interrupted ")
    except:
        print("An Error Occurred")

    exit()
