
import time
from concurrent import futures
import grpc

import sys
sys.path.append("sims/proto")
import twinu_core_pb2 as tpb
import twinu_core_pb2_grpc as tpb_grpc


class ClockMaster(tpb_grpc.ClockMasterServicer):

    def __init__(self):
        pass

    def SubscribeClock(self, request_iterator, context):
        for new_msg in request_iterator:
            reply_msgs = []
            print('Receive new message! [name: {}, msg: {}]'.format(new_msg.name, new_msg.msg))
            reply_msgs.append(tpb.ReplyMessage(reply_msg='{} {}'.format(new_msg.msg, new_msg.name)))
            reply_msgs.append(tpb.ReplyMessage(reply_msg='Nice to meet you!!!'))
            for message in reply_msgs:
                yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tpb_grpc.add_ClockMasterServicer_to_server(ClockMaster, server)
    server.add_insecure_port('[::]:1024')
    server.start()
    print('Starting gRPC Master Clock...')
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()