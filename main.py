import requests
import pprint
import config
import time
import json
import sys
import string


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
    else:
        print("error: failed to get thread list")
        sys.exit()

    return response.json()


def get_messages_on_thread(arena_id, problem_id):
    url = 'https://judgeapi.u-aizu.ac.jp/threads/arenas/{0}/problems/{1}'.format(
        arena_id, problem_id)
    response = requests.get(url)

    return response.json()


def make_text_about_thread(dic):
    visible = ''
    if dic['visible'] == 1:
        visible = 'public'
    else:
        visible = 'private'
    url = 'https://onlinejudge.u-aizu.ac.jp/beta/room.html#' + config.ARENA_ID + '/board'

    txt = ''
    if dic['problemId'] == '':
        txt = 'コンテスト全体に関する質問スレッドが追加されました！'
    else:
        txt = '{}問題に関する質問スレッドが追加されました！'.format(dic['problemId'])

    txt += '確認してください。\n\n'
    txt += 'userid: {}'.format(dic['userId']) + '\n'
    txt += 'policy: {}'.format(dic['policy']) + '\n'
    txt += 'type: {}'.format(dic['type']) + '\n'
    txt += 'title: {}'.format(dic['title']) + '\n\n'
    txt += url

    return {'text': txt}


def make_text_about_comment(dic, pid, title):
    url = 'https://onlinejudge.u-aizu.ac.jp/beta/room.html#' + config.ARENA_ID + '/board'

    txt = ''
    if pid == '':
        txt = 'コンテスト全体に関する質問スレッド'
    else:
        txt = '{}問題に関する質問スレッド'
    txt += '「{}」'.format(title)
    txt += 'に新しいコメントがつきました！確認してください。\n\n'

    txt += url

    return {'text': txt}


def checker(now_threads):
    def check(c):
        new_problem_dict = get_messages_on_thread(config.ARENA_ID, c)
        new_threads = new_problem_dict['threads']
        for new_thread in new_threads:
            is_exist = False
            for now_thread in now_threads[c]:
                if new_thread['id'] == now_thread['id']:
                    # 新しいコメントが増えてるかどうかチェック
                    now_comments = now_thread['rootComment']
                    new_comments = new_thread['rootComment']
                    for new_cm in new_comments:
                        flag = False
                        for now_cm in now_comments:
                            if new_cm['id'] == now_cm['id']:
                                flag = True
                                break
                        if flag == False:
                            m = make_text_about_comment(
                                new_cm, c, new_thread['title'])
                            requests.post(url=config.SLACK_HOOK_URL, json=m)
                    is_exist = True
                    break
            if is_exist == False:
                m = make_text_about_thread(new_thread)
                requests.post(url=config.SLACK_HOOK_URL, json=m)
        now_threads[c] = new_threads
    # スレッドが増えたかどうかをチェック
    for c in string.ascii_uppercase:
        check(c)
    check('')


def main():
    login(config.AOJ_ID, config.AOJ_PASS)

    now_threads = {}

    for c in string.ascii_uppercase:
        now_threads[c] = list()

    now_threads[''] = list()

    while True:
        print('update')
        checker(now_threads)
        time.sleep(config.SLEEP_TIME)


if __name__ == '__main__':
    main()
