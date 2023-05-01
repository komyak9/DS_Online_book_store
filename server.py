from concurrent import futures

import grpc
import book_store_pb2
import book_store_pb2_grpc


class DataStoreServicer(book_store_pb2_grpc.DataStoreServicer):
    def __init__(self):
        self.store = {}

    def Get(self, request, context):
        key = request.key
        value = self.store.get(key, '')
        return book_store_pb2.KeyValue(key=key, value=value)

    def Put(self, request, context):
        key = request.key
        value = request.value
        self.store[key] = value
        return book_store_pb2.KeyValue(key=key, value=value)

class ReplicationChainServicer(book_store_pb2_grpc.ReplicationChainServicer):
    def __init__(self, address, head_address, tail_address):
        self.address = address
        self.head_address = head_address
        self.tail_address = tail_address
        self.stubs = []
        self.nodes = []

    def RegisterNode(self, node_info, is_head=False, is_tail=False):
        self.nodes.append((node_info, is_head, is_tail))
        stub = book_store_pb2_grpc.DataStoreStub(grpc.insecure_channel(node_info.address + ':' + str(node_info.port)))
        self.stubs.append(stub)

    def ForwardGet(self, request, context):
        for stub in self.stubs:
            try:
                response = stub.Get(request)
                if response.value != '':
                    return response
            except:
                pass
        return book_store_pb2.KeyValue(key=request.key, value='')

    def ForwardPut(self, request, context):
        self.stubs[0].Put(request)
        for i in range(1, len(self.stubs)):
            try:
                self.stubs[i].Put(request)
            except:
                pass
        return request

def serve_node(node_index, nodes):
    node = nodes[node_index]
    address = node[0].address
    port = node[0].port
    is_head = node[1]
    is_tail = node[2]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kv_store_servicer = DataStoreServicer()
    book_store_pb2_grpc.add_DataStoreServicer_to_server(kv_store_servicer, server)
    replication_chain_servicer = ReplicationChainServicer(address, nodes[0][0].address + ':' + str(nodes[0][0].port), nodes[-1][0].address + ':' + str(nodes[-1][0].port))
    book_store_pb2_grpc.add_ReplicationChainServicer_to_server(replication_chain_servicer, server)
    for i in range(len(nodes)):
        node_info = nodes[i][0]
        is_head = i == 0
        is_tail = i == len(nodes) - 1
        replication_chain_servicer.RegisterNode(node_info, is_head, is_tail)
    server.add_insecure_port(address + ':' + str(port))
    server.start()
    server.wait_for_termination()

