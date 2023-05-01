

class BookStoreClient:
    """ Implements store logic """

    def __init__(self):
        # Processes storage of DataStore objects.
        self.processes = []
        # Ordered processes in a chain.
        self.processes_chain = []   # queue?

        # List of all available commands.
        self.commands = {"Local-store-ps": self.create_local_stores,
                         "Create-chain": self.create_chain,
                         "List-chain": self.list_chain,
                         "Write-operation": self.write_operation,
                         "List-books": self.list_books,
                         "Read-operation": self.read_operation,
                         "Data-status": self.data_status,
                         "Remove-head": self.remove_head,
                         "Restore-head": self.restore_head
                         }

    ######################################
    # Local-store-ps command             #
    ######################################
    def create_local_stores(self, k=1):
        # By default, it creates 1 process.
        # In our implementation, we specify k processes manually.
        pass

    ######################################
    # Creates a chain of processes       #
    ######################################
    def create_chain(self):
        # Chain is built out of processes which are placed in a random order.
        # Request to the server?
        pass

    ######################################
    # Removes chain's head               #
    ######################################
    def remove_head(self):
        # Request to the server?
        pass

    ######################################
    # Restored chain's head              #
    ######################################
    def restore_head(self):
        # Request to the server.
        pass

    ######################################
    # List-chain command                 #
    ######################################
    def list_chain(self):
        # Makes a request to the server.
        pass

    ######################################
    # Write-operation command            #
    ######################################
    def write_operation(self, book_name: str, price: float):
        # Creates a data item, stores it in the DataStore objects.
        pass

    ######################################
    # List-books command                 #
    ######################################
    def list_books(self):
        # Shows all available books.
        # As data is stored in the DataStore objects,
        # then we probably should extract them from there
        # (question is: do we store them locally in the client object?).
        pass

    ######################################
    # Read-operation command             #
    ######################################
    def read_operation(self, book_name: str):
        # Shows the price of the book.
        # Same data storage issue as discussed in the list-books method.
        pass

    ######################################
    # Data-status command                #
    ######################################
    def data_status(self):
        # Need to check the theory for dirty/clean definitions.
        pass



# Abstract implementation
def run_client():
    client = BookStoreClient()

    while True:
        # Input a command and it's arguments if there are any.
        command_string = input("Enter a command to execute: ")
        if ' ' in command_string:
            command, args = command_string.split(' ')
            args = [args]
        else:
            command = command_string
            args = ['']

        # Extract a command.
        method = client.commands.get(command)

        if method:  # If such command exists.
            # Execute method.
            success, message = method(*args)
        else:   # If such method doesn't exist.
            success = False
            message = f"Command {command} does not exist!"



if __name__ == '__main__':
    run_client()