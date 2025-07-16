from Address_book.fields import Name, Phone, Birthday, Email, Address

class Record:
    """
    Представляє запис контакту в адресній книзі.

    Зберігає ім'я, список телефонів, день народження, email і адресу.
    """
    def __init__(self, name):
        """
        Ініціалізує новий запис із заданим ім'ям.

        Args:
            name (str): Ім'я контакту.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        """
        Додає новий номер телефону до контакту.

        Args:
            phone (str): Телефон у форматі з 10 цифр.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Видаляє вказаний номер телефону з контакту.

        Args:
            phone (str): Телефон, який потрібно видалити.

        Raises:
            ValueError: Якщо номер не знайдено.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone, new_phone):
        """
        Замінює старий номер телефону на новий.

        Args:
            old_phone (str): Номер, який потрібно замінити.
            new_phone (str): Новий номер телефону.

        Raises:
            ValueError: Якщо старий номер не знайдено.
        """
        for p in self.phones:
            if p.value == old_phone:
                self.phones.remove(p)
                self.phones.append(Phone(new_phone))
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone):
        """
        Шукає номер телефону серед записів.

        Args:
            phone (str): Шуканий номер.

        Returns:
            Phone | None: Знайдений об'єкт Phone або None, якщо не знайдено.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, bday_str):
        """
        Додає або оновлює день народження контакту.

        Args:
            bday_str (str): Дата у форматі DD.MM.YYYY.

        Raises:
            ValueError: Якщо формат некоректний.
        """
        self.birthday = Birthday(bday_str)

    def add_email(self, email_str):
        """
        Додає або оновлює email для контакту.

        Args:
            email_str (str): Email у форматі name@example.com.

        Raises:
            ValueError: Якщо формат некоректний.
        """
        self.email = Email(email_str)

    def add_address(self, address_str):
        """
        Додає або оновлює адресу контакту.

        Args:
            address_str (str): Фізична адреса.

        Raises:
            ValueError: Якщо адреса порожня.
        """
        self.address = Address(address_str)

    def edit_email(self, email):
        self.email = email

    def edit_address(self, address):
        self.address = address

    def edit_birthday(self, birthday):
        self.add_birthday(birthday)



    def __str__(self):
        """
        Повертає строкове представлення запису контакту.

        Returns:
            str: Всі поля контакту у вигляді рядка.
        """
        phones_str = ', '.join(p.value for p in self.phones)
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{bday_str}{email_str}{address_str}"
