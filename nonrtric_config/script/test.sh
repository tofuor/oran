curl -X 'PUT' \
  'http://localhost:8080/data-producer/v1/info-types/type2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "info_job_data_schema": {
    "$schema":"http://json-schema.org/draft-07/schema#",
    "title":"STD_Type1_1.0.0",
    "description":"EI-Type 1",
    "type":"object"
  }
}'

curl -X 'PUT' \
  'http://localhost:8080/data-producer/v1/info-producers/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "info_producer_supervision_callback_url": "https://producer-stub:8093/callbacks/supervision/prod-a",
  "supported_info_types": [
    "type2"
  ],
  "info_job_callback_url": "https://producer-stub:8093/callbacks/job/prod-a"
}'

curl -X 'PUT' \
  'http://localhost:8080/data-consumer/v1/info-jobs/2?typeCheck=false' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "info_type_id": "type2",
  "job_result_uri": "https://ricsim_g3_1:8185/datadelivery",
  "job_owner": "ricsim_g3_1",
  "job_definition": {},
  "status_notification_uri": "http://producer:80/"
}'
