### move to the Model's Script directory from the root folder
"cd Model\\'\s\ Scripts"

### build the docker image
docker build -t lesson-plan-gen .

### run the docker image
docker run -p 5000:5000 lesson-plan-gen

### volume mounting the container
docker run -p 5000:5000 -v "$(pwd)":/app lesson-plan-gen

docker stop <container_id>

docker restart <container_id>

### making request models prediction from the container
curl -X POST -H "Content-Type: application/json" -d '{"topic":"heat transfer simulation","subject":"science","grade":"middle","student_profile":"","tech_domain":""}' http://localhost:5000/generate-response

curl -X POST -H "Content-Type: application/json" -d '{"topic":"cell division","subject":"biology","grade":"high","student_profile":"hearing impairment","tech_domain":""}' http://localhost:5000/generate-response

### Running test after building the container
docker run -t lesson-plan-gen pytest tests/



