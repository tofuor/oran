docker rm -f xapp-test
docker run -v $PWD/.:/app -p 40936:40936 --name xapp-test -itd xapp-test:1.0