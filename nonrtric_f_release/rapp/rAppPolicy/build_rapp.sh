docker build -t="rapp-policy:1.0.0" .
docker run --rm -d --network=nonrtric-docker-net --name rapp-policy rapp-policy:1.0.0
docker ps
