sudo docker rm -f go19
sudo docker run -v $PWD/.:/app -itd --name go19 go:1.0