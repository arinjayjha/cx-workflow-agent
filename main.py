
from agents.orchestrator import Orchestrator
from utils.document_loader import DocumentStore
from utils.memory_manager import MemoryManager

def demo():
    docs = DocumentStore()
    mem = MemoryManager()
    orch = Orchestrator(docs, mem)
    print('--- Demo ticket: Billing charge for cancelled order ---')
    ticket = 'My order was cancelled but I was charged ₹899. Please help.'
    result = orch.handle_ticket(ticket)
    print('\nFinal response from workflow:\n')
    print(result)

if __name__ == '__main__':
    demo()
