import requests
import pprint
import config
import time
import json
import copy
import sys


def login(uid, upass):
    url = 'https://judgeapi.u-aizu.ac.jp/session'

    login_data = {
        'id': uid,
        'password': upass
    }

    response = requests.post(url, json=login_data)

    if response.status_code == 200:
        print("login ok")
    else:
        print("error: failed login")
        sys.exit()


def logout():
    url = 'https://judgeapi.u-aizu.ac.jp/session'
    response = requests.delete(url)

    print('delete')
    print(response.status_code)


def get_thread_list(arena_id, page, size):
    url = 'https://judgeapi.u-aizu.ac.jp/threads/arenas/{0}?page={1}&size={2}'.format(
        arena_id, page, size)
    response = requests.get(url)

    if response.status_code == 200:
        print("ok. You got thread list.")
        print(response.json())
    else:
        print("error: failed to get thread list")
        sys.exit()

    return response.json()


def main():
    login(config.AOJ_ID, config.AOJ_PASS)
    lsz = 0
    while True:
        thread_list = get_thread_list(config.ARENA_ID, 1, 20)
        if lsz < len(thread_list):
            dic = thread_list[-1]
            messages = {
                'text': '新しいスレッドが追加されました！確認してください。\nproblemId: {0}\n userId: {1}\npolicy: {2}\ntype: {3}\ntitle: {4}\nhttps://onlinejudge.u-aizu.ac.jp/beta/room.html#WUPC2020/board'.format(dic['problemId'], dic['userId'], dic['policy'], dic['type'], dic['title'])
            }
            requests.post(config.SLACK_HOOK_URL, json=messages)
        lsz = len(thread_list)
        time.sleep(config.SLEEP_TIME)


if __name__ == '__main__':
    main()
