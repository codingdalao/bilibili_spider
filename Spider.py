# -*- coding: UTF-8 -*-
import json
import time

import requests


class Spider(object):
    PROP_NAME_LIST = [
        'UID',
        '昵称',
        '性别',
        '生日',
        '等级信息',
        'VIP状态',
        '注册时间',
        '关注数',
        '粉丝数',
        '投稿视频数',
        '投稿视频播放量',
        '投稿文章数',
        '投稿文章阅读量',
        '追番列表',
    ]

    PROP_KEY_LIST = [
        'uid',
        'nickName',
        'sex',
        'birthday',
        'level',
        'isVip',
        'regTime',
        'follower',
        'following',
        'submitVideos',
        'videoViewCount',
        'articles',
        'articleViewCount'
        'bangumis',
    ]

    def __init__(self):
        self.__header = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': None,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

    def getUser(self, uid: str):
        '''
            uid str: The ID of User\n
            return dict: {uid, nickName, sex, birthday, level, isVip, regTime, follower, following, submitVideos, videoViewCount, articles, articleViewCount, bangumis}
        '''

        Info = self.__get_GetInfo(uid)
        stat = self.__get_stat(uid)
        submitVideos = self.__get_getSubmitVideos(uid)
        articles = self.__get_article(uid)
        upstat = self.__get_upstat(uid)
        bangumis = self.__get_getList(uid)

        userInfo = {
            'uid': uid,
            'nickName': Info['name'],
            'sex': Info['sex'],
            'birthday': Info['birthday'],
            'level': Info['level_info'],
            'isVip': Info['vip']['vipStatus'],
            'regTime': time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(Info['regtime'])),
            'follower': stat['follower'],
            'following': stat['following'],
            'submitVideos': submitVideos,
            'videoViewCount': upstat['archive']['view'],
            'articles': articles,
            'articleViewCount': upstat['article']['view'],
            'bangumis': bangumis,
        }
        return userInfo

    # 获取 生日、等级信息、性别、VIP状态、注册时间（时间戳）
    def __get_GetInfo(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/member/GetInfo'
        data = {
            'mid': '%s' % uid,
        }
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.post(URL, data=data, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    # 获取 关注数、粉丝数
    def __get_stat(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/relation/stat?vmid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    def __get_upstat(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/space/upstat?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    # 获取文章列表
    def __get_article(self, uid: str):
        header = self.__header
        URL = 'https://api.bilibili.com/x/space/article?mid=%s&pn=1' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    # 获取投稿视频
    def __get_getSubmitVideos(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r

    # 获取追番列表
    def __get_getList(self, uid: str):
        header = self.__header
        URL = 'https://space.bilibili.com/ajax/Bangumi/getList?mid=%s' % uid
        header['Referer'] = 'https://space.bilibili.com/%s' % uid
        try:
            res = requests.get(URL, headers=header).text
            r = json.loads(res)
            r = r['data']
        except:
            r = None
        return r


def main(uid_min=1, uid_max=1):
    start_time = time.strftime('%H:%M:%S', time.localtime())
    u_min = uid_min
    u_max = uid_max + 1
    S = Spider()

    while u_min < u_max:
        print('正在爬取ID为%s的用户...' % u_min)
        userInfo = S.getUser(u_min)
        print(userInfo)
        u_min += 1

    print('爬取完成')
    print('%s%s' % ('开始时间：', start_time))
    print('%s%s' % ('结束时间：', time.strftime('%H:%M:%S', time.localtime())))


if __name__ == '__main__':
    main()
