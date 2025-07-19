# ✅ тут зберігаються всі функції для нотаток

from datetime import datetime
import re


# # Клас Note представляє окрему нотатку
class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        return f"Note: {self.text} | Tags: {tags_str}"

# Клас NoteBook — колекція об'єктів Note
class NoteBook:
    def __init__(self):
        self.notes = []

    # Додавання нової нотатки до списку
    def add_note(self, note: Note):
        self.notes.append(note)

    # Видалення нотатки за індексом
    def delete_note(self, index: int):
        if 0 <= index < len(self.notes):
            del self.notes[index]

    # Редагування тексту або тегів у нотатці
    def edit_note(self, index: int, new_text: str = None, new_tags: list = None):
        if 0 <= index < len(self.notes):
            if new_text:
                self.notes[index].text = new_text
            if new_tags is not None:
                self.notes[index].tags = new_tags

    def find_notes(self, keyword: str):
        # Пошук нотаток за ключовим словом у тексті або тегах.
        # Параметри: keyword (str): ключове слово для пошуку (без врахування регістру).
        # Повертає: Список об'єктів Note, у яких ключове слово зустрічається або в тексті нотатки, або в будь-якому з тегів.
        return [note for note in self.notes
                if keyword.lower() in note.text.lower()               # пошук у тексті
                or any(keyword.lower() in tag.lower() for tag in note.tags)]   # пошук у тегах

    def list_notes(self):
        return self.notes
    
    def search_by_tag(self, tag: str):
        # Пошук нотаток, які містять заданий тег.
        # Параметри: tag (str): тег для пошуку (без врахування регістру).
        # Повертає: Список об'єктів Note, які містять цей тег.
        return [note for note in self.notes
                if tag.lower() in [t.lower() for t in note.tags]
        ]
