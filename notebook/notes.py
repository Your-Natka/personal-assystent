import re
import json
from datetime import datetime

class Note:
    def __init__(self, text, tags=None, created=None):
        if not text.strip():
            raise ValueError("Note cannot be empty.")
        self.text = text.strip()
        self.tags = set(tags) if tags else set()
        self.created = datetime.strptime(created, "%Y-%m-%d %H:%M") if created else datetime.now()

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.discard(tag)

    def to_dict(self):
        return {
            'text': self.text,
            'tags': list(self.tags),
            'created': self.created.strftime("%Y-%m-%d %H:%M")
        }
    def to_list(self):
        return [note.to_dict() for note in self.notes]

    @staticmethod
    def from_dict(data):
        return Note(text=data['text'], tags=data['tags'], created=data['created'])

    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else "No tags"
        return f"[{self.created.strftime('%Y-%m-%d %H:%M')}] {self.text} (Tags: {tags_str})"
    @staticmethod
    def from_list(data_list):
        nb = Notebook()
        for data in data_list:
            nb.notes.append(Note.from_dict(data))
        return nb
    
class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)
        return "Note added."

    def find_notes(self, tag_keyword):
        tag_keyword = tag_keyword.lower().strip()
        matched = []
        for note in self.notes:
            # Припустимо note.tags — це список рядків тегів
            tags = [t.lower().strip() for t in note.tags]
            if tag_keyword in tags:
                matched.append(note)
        return matched

    def remove_note(self, index):
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            return "Note deleted."
        else:
            raise IndexError("Invalid note index.")
    def sort_by_tags(self):
        return sorted(self.notes, key=lambda note: sorted(note.tags)[0] if note.tags else '')

    def list_notes(self):
        return [str(note) for note in self.notes]
    