# これは何
- AOJ(Arena)のboardにthreadが追加されたらslackのチャンネルに通知を飛ばすアプリ
- ~~threadが追加されたら通知するだけで、threadにコメントがついても通知されないことに注意~~ コメントも拾えるようにした、多分
- ただしAPIの仕様上、publicなスレッドとコメントしか拾えません。**privateなスレッドとコメントを拾う方法をご存じの方はissue、pull requestお待ちしています...！**

# 使い方

![](https://i.imgur.com/FGzKeFg.png)

- config.pyに設定を追記する。
    - **ARENA_ID**には、コンテストページ上部のID以下を追記
    ![](https://i.imgur.com/yvAtTsu.png)
    - **AOJ_ID, AOJ_PASS**にはそれぞれAOJのID、パスワードを追記
    - **SLACK_HOOK_URL**には[ここ](https://slackbot-test-shiro.slack.com/apps/A0F7XDUAZ--incoming-webhook-?next_id=0)から追加したいslack workspaceのincoming webhook urlを取得し、追記
    - **SLEEP_TIME**はクローリングする間隔です。たとえば値が10なら、10秒ごとに更新されてるかどうかをチェックします。間隔を狭めすぎると過剰にAOJにリクエストを飛ばすため危ないので注意。

- ターミナルにて```python3 main.py``` で起動。
- 使い終わったら```Ctrl+Z```とかで強制終了してください(雑)
