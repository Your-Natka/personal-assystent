import re
from datetime import datetime


class Note:
    def __init__(self, text, tags=None):
        if not text.strip():
            raise ValueError("Note cannot be empty.")
        self.text = text.strip()
        self.tags = set(tags) if tags else set()
        self.created = datetime.now()

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.discard(tag)

    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else "No tags"
        return f"[{self.created.strftime('%Y-%m-%d %H:%M')}] {self.text} (Tags: {tags_str})"


class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)
        return "Note added."

    def find_notes(self, keyword):
        result = []
        for note in self.notes:
            if keyword.lower() in note.text.lower() or keyword.lower() in (tag.lower() for tag in note.tags):
                result.append(note)
        return result

    def remove_note(self, index):
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            return "Note deleted."
        else:
            raise IndexError("Invalid note index.")
    def sort_by_tags(self):
        return sorted(self.notes, key=lambda note: sorted(note.tags))

    def list_notes(self):
        return [str(note) for note in self.notes]