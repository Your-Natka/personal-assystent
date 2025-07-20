Наша команда MemoHackers розробила віртуального бота.

Посилання на презентацію: https://gamma.app/docs/MemoHackers-Personal-Assistant-CLI-tvgd1oy80p2on7k?mode=doc

**Personal Assistant** — це консольний помічник на Python, який допоможе керувати:

📇 Контактами (телефон, email, адреса, день народження)

🗒️ Нотатками з тегами

📅 Нагадуваннями про дні народження

2. Наш репозиторій:

https://github.com/Your-Natka/personal-assystent

## ⚙️ Встановлення

### 1. Клонувати репозиторій:

git clone https://github.com/Your-Natka/personal-assystent.git
cd personal-assystent

3. Віртуальне середовище:
python3 -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows

4. Встановлюємо залежності:
pip install -r requirements.txt
Щоб зберегти список залежностей:
pip freeze > requirements.txt

5. Запуск
python3 main.py 
(Якщо у терміналі ввести: source ~/.zshrc
А потім: hello)

6. Інструкція користувача.
Після запуску бот запитає режим:

Enter mode (contacts/notes or exit):

  - введіть contacts — для керування контактами
  - введіть notes — для роботи з нотатками
  - введіть exit — для завершення програми

Після входу в режим бот повідомить:

Entering contacts mode (type 'help' for available commands)
Введіть команду help, щоб побачити всі доступні команди.

🧾 Команди (режим contacts)
Команда	Опис
add	                - Додати новий контакт (інтерактивно)
edit	              - Редагувати контакт (інтерактивно, поле за полем)
delete name	        - Видалити контакт за ім’ям
show name	          - Показати повну інформацію про контакт
all	                - Вивести всі збережені контакти
search keyword	    - Пошук за частиною імені контакту
show-birthday name	- Показати день народження контакту
birthdays	          - Показати всі дні народження на найближчі 7 днів
birthdays-in N	    - Показати дні народження за наступні N днів
help                - Показати список команд
back                - Вийти в головне меню


🧩 Покрокове додавання контакту (команда add)

Команда add запускає інтерактивний режим створення контакту.

Кроки:
Ім’я (обов'язкове)
Телефон (опціонально)
Email (опціонально)
Адреса (опціонально)
День народження (опціонально, формат DD.MM.YYYY)

📌 Після кожного кроку бот запитає:

Do you want to continue? (yes/no):

   - Якщо no — контакт буде збережений з тими даними, що вже введені.

   - Якщо yes — перехід до наступного поля.

🕹️ Ви можете натискати Enter, щоб пропустити поле.

🔔 В кінці буде повідомлення:

Contact 'Anna' added successfully.

📌 Приклад

Enter command: add
Adding new contact (press Enter to skip a field or type 'exit' to cancel)
Enter name: Anna
Enter phone (optional): 0971234567
Do you want to continue? (yes/no): yes
Enter email (optional): anna@example.com
Do you want to continue? (yes/no): yes
Enter address (optional):
Do you want to continue? (yes/no): yes
Enter birthday (DD.MM.YYYY, optional): 15.07.1990
Contact 'Anna' added successfully.


🧩 Покрокове редагування контакту (команда edit)

Команда edit запускає інтерактивний режим редагування для існуючого контакту.

Ви можете змінити номер телефону, email, адресу або день народження. Для кожного поля можна залишити старе значення, просто натиснувши Enter. Щоб вийти з режиму редагування — введіть exit.

📌 Приклад
Enter command: edit
Editing contact (type 'exit' to cancel or press Enter to skip a field)
Enter the name of the contact you want to edit: Lucja
Current phone(s): 0962343456
Enter new phone (or press Enter to keep current): 0674564567
Current email: lucja@gmail.com
Enter new email (or press Enter to keep current): 
Current address: Kyiv
Enter new address (or press Enter to keep current): lwow
Current birthday: 18.07.1990
Enter new birthday (DD.MM.YYYY) (or press Enter to keep current): 20.07/1990
Invalid birthday format: Invalid date format. Use DD.MM.YYYY
Contact 'Lucja' updated successfully.


🧩 Перегляд усіх контактів (команда all)
Команда all виводить усі збережені контакти, включно з доступними полями: ім’я, телефон(и), email, адреса та день народження (якщо вказано).
📌 Приклад:

Enter command: all
Name: Lucja
Phones: 0674564567
Email: lucja@gmail.com
Address: lwow
Birthday: 18.07.1990
------------------------------
Name: Nata
Phones: 0983453453
------------------------------
Name: Vita
Phones: 0737657654
Email: vita@gmail.com
------------------------------

🆘 Отримання списку доступних команд (команда help)
Команда help показує повний список доступних команд та їх короткий опис.

🧩 Покрокове видалення контакту (команда delete)

Щоб видалити контакт, введіть delete [ім'я_контакту].

📌 Приклади:
✅ Успішне видалення:

Enter command: delete Nata
Contact 'Nata' deleted successfully.

❗️Помилка при неправильному форматі команди:
Enter command: delete
Invalid command. Use: delete [username]
Команда під сказу є що тато опи видалити контакт ми маємо знайти його name.

🧩 Команда back повертає нас в головне меню.

Enter command: back
Returning to mode selection...
Enter mode (contacts/notes or exit): exit

🧩 Покрокова робота команди search

Введення команди пошуку
Enter command: search Vi
🖨 Результат:
Contact name: Vita, phones: 0737657654, email: vita@gmail.com

Інший запит
Enter command: search 073
🖨 Результат:

Contact name: Vita, phones: 0737657654, email: vita@gmail.com
Contact name: Natali, phones: 0737657654


🗒️ Робота з нотатками

🗒️ Команди (режим notes)
Команда	Опис
add-note "text" tags.      - Додати нотатку (теги через кому, без пробілів)
show-notes	               - Показати всі нотатки
find-note keyword	         - Знайти нотатки за ключовим словом або тегом
edit-note index "new text" - Редагувати нотатку за індексом
delete-note index	         - Видалити нотатку

🧩 Додавання нотатки (команда add-note)
Щоб додати нову нотатку, використовуйте команду:

add-note "текст нотатки" тег1,тег2,...

Текст нотатки береться в лапки.

Теги вводяться через кому без пробілів.

📌 Приклад:

Enter command: add-note "Зателефонувати лікарю" важливо,здоров'я
Note added successfully.

🧩 Перегляд усіх нотаток (команда show-notes)
Команда show-notes виводить список усіх нотаток із часом створення та тегами.

📌 Приклад:

Enter command: show-notes
[2025-07-19 16:32] Зателефонувати лікарю (Tags: важливо, здоров'я)
[2025-07-19 16:46] Сьогодня перед презентація нашого додатку (Tags: важлива подія)

🧩 Пошук нотаток (команда find-note)
Щоб знайти нотатку за словом або тегом, введіть:

find-note ключове_слово_або_тег

📌 Приклад:
Enter command: find-note важливо
[2025-07-19 16:32] Зателефонувати лікарю (Tags: важливо, здоров'я)

❗️Якщо не вказати ключове слово — отримаєте підказку:
Enter command: find-note
Please provide a keyword to search for notes.

🧩 Редагування нотатки (команда edit-note)
Щоб змінити текст нотатки, введіть:

edit-note індекс "новий текст"

Індекс — номер нотатки у списку (нумерація починається з 1).

Новий текст слід ввести в лапках.

📌 Приклад:

Enter command: edit-note 2 "Зателефонувати стоматологу"
Note updated successfully.

🧩 Видалення нотатки (команда delete-note)
Щоб видалити нотатку, введіть:

delete-note індекс

📌 Приклад:

✅ Успішне видалення:
Enter command: delete-note 1
Deleted note:
[2025-07-18 22:13] 1 (Tags: note., my)

❗️Якщо індекс не вказано:

Enter command: delete-note
Please provide the index of the note to delete.

🧩 Повернення в головне меню (команда back)
Команда back виходить з режиму нотаток у головне меню:

Enter command: back
Returning to mode selection...
Enter mode (contacts/notes or exit):

Enter command: exit чи close закриває наш бот.

7. 💾 Збереження даних

Контакти та нотатки автоматично зберігаються у файли:

contacts_data.pkl
notes_data.pkl

При наступному запуску ці дані будуть завантажені автоматично.

8. Структура проєкту

personal-assystent/
│
├── main.py               # Точка входу
├── commands.py           # Обробка команд
├── storage.py            # Збереження / завантаження даних
├── parser.py             # Парсинг введення
├── data.py               # Глобальні змінні (контакти, нотатки)
├── error_handlers.py     # Обробка помилок
├── Address_book/
│   ├── __init__.py
│   ├── record.py         # Класи Record, Field, Phone, Email, Birthday, Address
│   └── notes.py          # Клас Notebook, Note
└── requirements.txt      # Залежності

9. Приклади

> add
Enter name: Anna
Enter phone: 0971234567
Enter email: anna@example.com
...

> edit
Enter name to edit: Anna
Current phone: 0971234567
Enter new phone (or leave empty): 0987654321
...

> search Anna
Contact name: Anna, phones: 0987654321, email: anna@example.com ...

🧡 Дякуємо за користування нашим помічником!

👋 Якщо у вас є ідеї або побажання — не соромтесь створити issue або pull request!

