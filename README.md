## SNU Network project

### simple chat program 
- python3
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
