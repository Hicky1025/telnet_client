# telnet_client
### メモ
soc.recv()について
ソケットからデータを受信し、結果をbytesオブジェクトで返し一度に受信するデータは引数に渡したバッファサイズとなります。
ー＞Telnetは1024で十分
https://qiita.com/castaneai/items/9cc33817419896667f34
https://emotionexplorer.blog.fc2.com/blog-entry-126.html

### how to use
```
docker compose up --build --d
docker exec -it telnet_telnet_client /bin/bash
python3 telnet.py 172.24.118.34 23
```
