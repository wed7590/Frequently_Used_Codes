import paho.mqtt.client as mqtt
import time
 
# 콜백 함수 정의하기
#  (mqttc.connect를 잘 되면) 서버 연결이 잘되면 on_connect 실행 (이벤트가 발생하면 호출)
def on_connect(client, userdata, flags, rc):
    # 연결이 성공적으로 된다면 완료 메세지 출력
    if rc == 0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)
 
def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

# (mqttc.publish가 잘 되면) 메시지를 publish하면 on_publish실행 (이벤트가 발생하면 호출)
def on_publish(client, obj, mid):
    # 용도 : publish를 보내고 난 후 처리를 하고 싶을 때
    # 사실 이 콜백함수는 잘 쓰진 않는다.
    print("pub_mid: " + str(mid))

# 클라이언트 생성
client = mqtt.Client()
 
# 콜백 함수 할당하기
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish


# 브로커 연결 설정
# 참고로 브로커를 Cloudmqtt 홈페이지를 사용할 경우
# 미리 username과 password, topic이 등록 되어있어야함.
url = "localhost"
port = 8883
topic = "devs/DEV1"
json = {
    "data" : 1,
    "data2" : 2
}
msg = 'data_data_data'

 
# 클라이언트 설정 후 연결 시도
# client.username_pw_set(username, password)
client.connect(host=url, port=port)
 
# 메시지 토픽에 담아 보내기

# client.publish(topic, bytes(str(json, 'utf-8')), 1)

# timeout 2sec.
def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        send_msg = f"{msg}: {msg_count}"
        result = client.publish(topic, msg, 1)
        status = result[0]
        if status == 0:
            print(f"Send `{send_msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run():
    client.loop_start()
    publish(client)

if __name__== '__main__':
    run()
