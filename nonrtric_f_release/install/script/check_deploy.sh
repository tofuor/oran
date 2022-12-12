echo "***************************check A1 Policy Management Service***************************"
curl localhost:8081/a1-policy/v2/rics

echo ""
echo "***************************check A1 Simulator***************************"
curl localhost:8081/a1-policy/v2/rics

echo ""
echo "***************************put policy type in ric1***************************"
curl -X PUT -v "http://localhost:8085/a1-p/policytypes/1" -H "accept: application/json" \
 -H "Content-Type: application/json" --data-binary @osc_pt1.json
sleep 5
curl -X PUT -v "http://localhost:8085/a1-p/policytypes/2" -H "accept: application/json" \
 -H "Content-Type: application/json" --data-binary @osc_pt2.json
sleep 5
curl -X PUT -v "http://localhost:8085/a1-p/policytypes/3" -H "accept: application/json" \
 -H "Content-Type: application/json" --data-binary @osc_pt3.json

echo ""
echo "***************************put policy type in nearRT***************************"
curl -X PUT -v "http://192.168.239.137:32080/a1mediator/a1-p/policytypes/1" -H "accept: application/json" \
 -H "Content-Type: application/json" --data-binary @osc_pt1.json
sleep 5
curl -X PUT -v "http://192.168.239.137:32080/a1-p/policytypes/2" -H "accept: application/json" \
 -H "Content-Type: application/json" --data-binary @osc_pt2.json

echo ""
echo "***************************check Information Coordinator Service***************************"
curl -X GET localhost:8083/data-producer/v1/info-types

echo ""
echo "***************************check gateway***************************"
curl localhost:9090/a1-policy/v2/rics
echo ""
curl localhost:9090/data-producer/v1/info-types

echo ""
echo "***************************check App Catalogue***************************"
curl localhost:8680/services

echo ""
echo "***************************check Dmaap Adapter Service***************************"
curl -k -X PUT -H Content-Type:application/json https://localhost:8434/data-consumer/v1/info-jobs/job1 --data-binary @job1.json
echo ""
curl -k https://localhost:8434/A1-EI/v1/eijobs/job1/status
echo ""
echo "Put kafka message ......"
curl -k -X PUT -H Content-Type:application/json https://localhost:8434/data-consumer/v1/info-jobs/job2 --data-binary @job2.json
curl -k https://localhost:8434/A1-EI/v1/eijobs/job2/status

# echo ""
# echo "***************************check Dmaap Mediator Producer***************************"
# curl -X PUT -H Content-Type:application/json https://localhost:8083/data-producer/v1/info-jobs/job3 --data-binary @job3.json
# echo ""
# curl -k https://localhost:8434/A1-EI/v1/eijobs/job3/status

echo ""
echo "***************************check control panel***************************"
echo "http://localhost:8080/"
