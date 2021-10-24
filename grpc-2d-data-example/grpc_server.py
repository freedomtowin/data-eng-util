"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

import numpy as np
import tensorflow as tf

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

export_path_sm = "./mobilenet_final/001"
reloaded_sm = tf.saved_model.load(export_path_sm)


class Greeter(helloworld_pb2_grpc.GreeterServicer):
        
    def CallModel(self, request, context):
        rslt = ' '.join([str(d) for d in request.data])
        img = np.array(request.data).reshape(request.rows,request.cols,request.channels)
     
        pred = reloaded_sm(tf.cast(img[np.newaxis, ...],tf.float32)).numpy()
        return helloworld_pb2.ModelResult(message='Input Data, %s!' % str(np.argmax(pred)))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

