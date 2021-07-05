# gRPC example in python

This is an example to run gRPC server on docker as well as access the server from a client on a local machine.

We will use a custom protocol buffer to send an image to a MobileNet image classifier, prediction server.

## Requirements

- Docker
- Anaconda

## Implement the files

1. Define the protocol-buffer in `helloworld.proto`.
2. Implement a command to generate python files from `helloworld.proto` in `codegen.py`.
3. Implement `grpc_server.py`.
4. Implement `greeter_server.py`.


## How to run the server and the client on our local machine
```
python grpc_server.py

python greeter_client.py
Greeter client received: Hello, cool guy!
```

## How to build and run a docker image

The docker image is used for running `grpc_server.py`.
The host name depends on your environment.
If you use `docker-machine`, we can see the IP address with `docker-machine ip YOUR_DOCKER_MACHINE`.
```
docker build . -t python-grpc-image
docker run --rm -d -p 50051:50051 --name grpc-example python-grpc-example
```

And then, we check if the client can access the server on docker or not:

```
# Execute it on your local machine, not a docker container.
python greeter_cliept.py --host HOST_NAME --port 50051
```
