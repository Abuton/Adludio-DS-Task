
docker build --tag adludiodev/creative_recommend_engine:1 .

# docker push adludiodev/creative_recommend_engine:1

docker run  -p 8899:80 -it adludiodev/creative_recommend_engine:1
