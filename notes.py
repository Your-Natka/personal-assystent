import pickle

class Note:
    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

    def __str__(self):
        return f"{self.text} (Tags: {', '.join(self.tags)})"

class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags):
        note = Note(text, tags)
        self.notes.append(note)
        return "Note added successfully."

    def list_notes(self):
        return [f"{i}: {str(note)}" for i, note in enumerate(self.notes)]

    def find_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower()]

    def edit_note(self, index, new_text, new_tags=None):
        if 0 <= index < len(self.notes):
            self.notes[index].text = new_text
            if new_tags is not None:
                self.notes[index].tags = new_tags
            return "Note updated."
        return "Invalid index."

    def remove_note(self, index):
        if 0 <= index < len(self.notes):
            self.notes.pop(index)
            return "Note deleted."
        return "Invalid index."

def save_notes(notebook, filename="notes.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(notebook, file)

def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return Notebook()
