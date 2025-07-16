from collections import UserDict
from address_book.record import Record
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
        
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.date()
                bday_this_year = bday.replace(year=today.year)

                # Якщо день народження вже був цього року — перенесемо на наступний
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                if today <= bday_this_year <= end_date:
                    upcoming.append(f"{record.name.value}: {bday.strftime('%d.%m.%Y')}")

        return upcoming
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
