from DTO import DTO
from GoogleCalendar import GoogleClient
from Brightspace import BrightSpace


def main():
    # credentials.json should be in this folder
    client = GoogleClient('credentials.json')
    data = DTO()
    
    email = input("\nEnter algonquin email: ")
    password = input("\nEnter your password: ")
    
    courses = data.read_txt("courses.txt")
    brightspace = BrightSpace(courses)
    array = ['Theory', 'Labs', 'Assignments']
    data.delete_csv(array)
    print("\nGetting calendar info.")
    brightspace.start(email, password)

    for sub in array:
        print(f'\nUpdating {sub} calendar.')
        data.read_csv(sub)
        file = data.get_file()
        client.create_calendars(sub)
        client.erase_calendar(sub)
        client.add_events(file, sub)
    print("\nUpdated!")




if __name__ == "__main__":
    main()

    exit()
