## SNU Network project

### simple chat program 
- python3(3.6.2에서 테스트.)
- socket

##### chat_client.py 와 chat_server.py 로 구성
##### Todo
- 로그인
- 방 초대/ 나가기
- 메세지 큐

##### message type을 정함
```json
{
    "type": "login | invitation |message ",
    "content": "..."

}
```

##### Socket 주의 사항
- ``socket.send()`` 를 할 때에는 ``encode('utf-8')``을 해주고
- ``socket.recv()`` 시에는 ``decode('utf-8')``을 해주어야 한다
- ``json.dumps()`` 는 따로 ``decode`` 해주지 않아도 된다.

##### 가정한 점
- 중복로그인은 없다.
- 로그인 시 초대 메세지는 가장 최근 1개만 보여진다.
- Select library는 window에서 작동하지 않을 수 있다.

##### 실행 방법
- ``python3 chat_server.py``
- ``python3 chat_client.py HOST_URL HOST_PORT``
