"""The Python implementation of the GRPC helloworld.Greeter client."""
from __future__ import print_function

import argparse

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

import numpy as np

import requests
import cv2

IMAGE_RES = 192

image_file = 'https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg'

req = requests.get(image_file)
image = cv2.cvtColor(cv2.imdecode(np.frombuffer(req.content, np.uint8),-1),cv2.COLOR_BGR2RGB)/255
image_content = cv2.resize(image,(IMAGE_RES, IMAGE_RES))


rows=image_content.shape[0]

cols=image_content.shape[1]

channels=image_content.shape[2]

def run(host, port):
    channel = grpc.insecure_channel('%s:%d' % (host, port))
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    
    response = stub.CallModel(helloworld_pb2.DoubleMatrix(rows=rows,cols=cols,channels=channels,data=image_content.flatten()))
    
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='host name',
                        default='localhost',
                        type=str)
    parser.add_argument('--port', help='port number',
                        default=50051,
                        type=int)
    args = parser.parse_args()
    run(args.host, args.port)
