from collections import UserDict
from contacts.record import Record
from datetime import datetime, timedelta

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError("Record with this name already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming = []

        for name, record in self.data.items():
            if not record.birthday:
                continue

            bday = record.birthday.value
            next_birthday = bday.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            delta = (next_birthday - today).days
            if 0 <= delta <= days:
                upcoming.append(f"{name} — {next_birthday.strftime('%d.%m')} (через {delta} дн.)")

        return upcoming
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
