rm -f $(pwd)/xappInfo/*
docker run -it --net=host --rm -v $(pwd)/xappInfo:/xappInfo xapp:$1