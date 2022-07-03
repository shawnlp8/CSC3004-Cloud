# gRPC Imports
import grpc
import item_locator_pb2
import item_locator_pb2_grpc
from concurrent import futures
import logging

class ItemLocator(item_locator_pb2_grpc.ItemLocatorServicer):

    def SearchItem(self, request, context):
        return item_locator_pb2.Reply(res="Item found!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    item_locator_pb2_grpc.add_ItemLocatorServicer_to_server(ItemLocator(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
# Run the gRPC server
    print("gRPC server started and listening on port 50051...\n")
    logging.basicConfig()
    serve()