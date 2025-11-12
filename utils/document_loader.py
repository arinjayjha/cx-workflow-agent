
class DocumentStore:
    def __init__(self):
        # Very small in-memory KB for demo
        self.docs = [
            {'id':1, 'title':'Refund Policy', 'text':'Refunds are issued within 5-7 business days after verification.'},
            {'id':2, 'title':'Billing FAQ', 'text':'If you are charged for a cancelled order, contact billing with order ID.'}
        ]

    def search(self, query):
        hits = [d for d in self.docs if any(tok.lower() in d['text'].lower() for tok in query.split())]
        if hits:
            return hits[0]['text']
        return 'No relevant KB found.'
