curl -X GET https://localhost:8434/data-producer/v1/info-types/ -k
curl -X GET https://localhost:8434/data-producer/v1/info-producers/ -k
curl -X GET https://localhost:8434/data-producer/v1/info-producers/A1_EI_test_Producer/status -k
curl -X GET https://localhost:8434/data-consumer/v1/info-jobs/ -k
curl -X GET http://localhost:6969/health_check
curl -k -X PUT -H Content-Type:application/json https://localhost:8434/data-consumer/v1/info-jobs/job_test --data-binary @job_test.json

"Add job: {job3owner 2023-03-04T12:28:01.234247Z job3 http:localhost:8888 {{0 0}} STD_Fault_Messages dmaap}"