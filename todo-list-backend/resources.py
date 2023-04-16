from typing import List
import os


def print_with_indent(value, indent=0):
    print('\t' * indent + value)


class Entry:

    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.parent = parent
        self.title = title
        self.entries = entries

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self.title, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        json = {}
        if self.entries is None:
            json = dict(title=self.title, entries=self.entries)
            return json
        json = dict(title=self.title, entries=[i.json() for i in self.entries])
        return json

    @classmethod
    def from_json(cls, value):
        new_entries = Entry(value['title'])
        for i in value['entries']:
            new_entries.add_entry(cls.from_json(i))
        return new_entries

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as file:
            return json.dump(self.json(), file)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            value = json.load(file)
        return cls.from_json(value)

class EntryManager:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for i in self.entries:
            i.save(self.data_path)

    def load(self):
        for i in os.listdir(self.data_path):
            if i.endswith('.json'):
                self.entries.append(Entry.load(os.path.join(self.data_path, i)))

    def add_entry(self, title: str):
        self.entries.append(Entry(title))