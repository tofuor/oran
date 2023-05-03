docker kill rapp-policy
docker rmi rapp-policy:1.0.0
docker build -t="rapp-policy:1.0.0" .
docker run --rm -d -v $(pwd)/configs:/configs --network=nonrtric-docker-net -p 6969:6969 --name rapp-policy rapp-policy:1.0.0
# docker ps