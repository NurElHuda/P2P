
# Docker setup

1. Build the docker image

```
docker build -t p2p:latest .
```

2. Run the built image

```
docker run --rm -it  -p 8000:8000/tcp p2p:latest
```
