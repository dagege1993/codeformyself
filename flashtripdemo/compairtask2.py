import http.client

conn = http.client.HTTPConnection("127,0,0,1")

payload = "{\n    \"stage\": \"availability\",\n    \"cms_id\": \"5bcd45e89bd4380026444038\",\n    \"user_id\": \"5caef912dda0f3001141f059\",\n    \"room_type\": \"\",\n    \"weego_price\": \"100\",\n    \"checkin\": \"2019-07-30\",\n    \"checkout\": \"2019-07-31\",\n    \"meal_type\": \"False\",\n    \"is_package\": \"False\",\n    \"source\": \"FlashTrip/20190423 CFNetwork/976 Darwin/18.2.0\",\n    \"cancel_policy\": \"\",\n    \"user_ip\": \"119.61.22.42\",\n    \"source_type\": \"wechat\",\n    \"voucher\": \"\",\n    \"deal_check_code\": \"\"\n}"

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "09d1144b-252d-4fcd-bb27-7dd8a8d9988b"
    }

conn.request("POST", "api,v1,record,user", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))