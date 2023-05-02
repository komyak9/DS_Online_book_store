from concurrent import futures
import time

import grpc
import book_store_pb2
import book_store_pb2_grpc

class BookStoreServicer(book_store_pb2_grpc.BookStoreServicer):
    def __init__(self, port):
        #self.DataStores = {}    # store info about data stores, id:address
        self.data_storage_servers = []
        self.clients = []   # client id's
        self.client_processes = {}  # info about clients' processes, client_id:processes_ids
        self.port_starts_from = port

    def CreateLocalStores(self, request, context):
        client_id = f"Client{len(self.clients)+1}"
        print(f"New request from client: {client_id}")

        self.clients.append(client_id)
        ports = []
        self.client_processes[client_id] = []
        for i in range(request.processes_number):
            self.client_processes[client_id].append(client_id + f"-process{i+1}")
            ports.append(str(self.port_starts_from))
            self.port_starts_from += 1

        message = "Ids are assigned to the client and the processes successfully."
        return book_store_pb2.CreateLocalStoresResponse(success=True, message=message, client_id=client_id,
                                                        processes_ids=self.client_processes[client_id],
                                                        processes_ports=ports)

    # Client sends a request to write.
    # Server checks if this particular client has a head node.
    def WriteOperation(self, request, context):
        pass


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

