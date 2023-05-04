from concurrent import futures
import time
import random

import grpc
import book_store_pb2
import book_store_pb2_grpc

class BookStoreServicer(book_store_pb2_grpc.BookStoreServicer):
    def __init__(self, port):
        #self.DataStores = {}    # store info about data stores, id:address
        self.data_storage_servers = []

        # Info about clients and processes
        self.clients = []   # client id's
        self.client_ips = {}
        self.client_processes = {}  # info about clients' processes, client_id:processes_ids
        self.processes_addresses = {}

        self.port_starts_from = port

        # Chain-related variables
        self.is_chain_created = False
        self.processes_with_sucs_preds = {}
        self.processes_chain = []

    def CreateLocalStores(self, request, context):
        client_id = f"Client{len(self.clients)+1}"
        print(f"New request from client: {client_id}")

        self.clients.append(client_id)
        self.client_ips[client_id] = request.ip_address
        self.client_processes[client_id] = []
        for i in range(request.processes_number):
            self.client_processes[client_id].append(client_id + f"-process{i+1}")

        message = "Ids are assigned to the client and the processes successfully."
        return book_store_pb2.CreateLocalStoresResponse(success=True, message=message, client_id=client_id,
                                                        processes_ids=self.client_processes[client_id])

    def CreateChain(self, request, context):
        print(f"Client {request.client_id} requested a chain creation...")

        if not self.is_chain_created:
            # Get all processes and shuffle them (assigning a random order -> random chain)
            for processes in list(self.client_processes.values()):
                self.processes_chain.extend(processes)
            random.shuffle(self.processes_chain)

            self.is_chain_created = True
            message = "Chain was created successfully."
            print(message)
        else:
            message = "Chain alreasy exists."
            print(message)

        self.generate_processes_addresses()

        # To each client we need to send info only about it's processes
        # We send it in a format ---process_id:[predecessor_address, successor_id]---
        self.arrange_predecessors_and_successors(self.processes_chain)  # Create [succ-r, pred-r] dict for all processes
        client_processes_preds_sucs = self.extract_client_processes(request.client_id)    # Extract those only for this client
        head_node_address = self.processes_addresses[self.processes_chain[0]]
        return book_store_pb2.CreateChainResponse(success=True, message=message,
                                                  processes_sucs_preds = client_processes_preds_sucs,
                                                  processes_addresses = self.processes_addresses,
                                                  head_node_address=head_node_address)

    def generate_processes_addresses(self):
        for client in self.clients:
            for process in self.client_processes[client]:
                self.processes_addresses[process] = self.client_ips[client] + ':' + str(self.port_starts_from)
                self.port_starts_from += 1

    # Generating a dictionary of predecessors and successors for all the processes
    def arrange_predecessors_and_successors(self, chain):
        self.processes_with_sucs_preds[chain[0]] = 'None' + ',' + chain[1]
        for i in range(1, len(chain) - 1):
            self.processes_with_sucs_preds[chain[i]] = chain[i - 1] + ',' + chain[i + 1]
        self.processes_with_sucs_preds[chain[-1]] = chain[-2] + ',' + 'None'

    # Extracting processes with their predecessors and successors of the requesting client
    def extract_client_processes(self, client_id):
        processes_addresses = {}
        processes = self.client_processes[client_id]
        for pr in processes:
            processes_addresses[pr] = self.processes_with_sucs_preds[pr]
        return processes_addresses



def serve():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    book_store_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(port+1), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started listening on {port} port")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

