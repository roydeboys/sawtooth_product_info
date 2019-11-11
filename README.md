## Run all container
`
docker-compose -f sawtooth-default.yaml up
`
## Run in shell container
`
docker exec -it sawtooth-shell bash
`
## Check block
`
sawtooth block list --url http://rest-api:8008
`