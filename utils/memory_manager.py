
class MemoryManager:
    def __init__(self):
        self.store = []  # simple list store for demo

    def add(self, key, value):
        self.store.append({'key':key,'value':value})

    def query(self, key_substr):
        return [x for x in self.store if key_substr.lower() in x['key'].lower() or key_substr.lower() in str(x['value']).lower()]
