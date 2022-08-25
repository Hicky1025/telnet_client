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

原理
タグの処理
→ループでできる

問題点
・無限ループだと関数の返り値がないので、綺麗ではない
・パケットの受け取り→パケットの出力
    問題：パケットが受け取れないと処理そ進めることができない
    問題：受信データがどこで終わるのかがわからない
・入力を受け取り→パケットを送信
    問題：^Cでブレイクしても、この関数は終わらせられるが、受信の関数が終了できない
を同時に処理する必要がある

