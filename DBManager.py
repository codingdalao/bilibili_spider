# -*- coding: UTF-8 -*-
import sqlite3
import os


class DBManager(object):
    def __init__(self, path: str):
        '''
            path str : The path of Database
        '''
        self.__path = path
        isExists = os.path.exists(path)
        if not isExists:
            self.__createNew()

    def __createNew(self):
        path = self.__path
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE USER(
                UID TEXT PRIMARY KEY NOT NULL,
                NICKNAME TEXT NOT NULL,
                SEX TEXT NOT NULL,
                BIRTHDAY TEXT NOT NULL,
                LEVEL INT NOT NULL,
                ISVIP INT NOT NULL,
                REGTIME TEXT NOT NULL,
                FOLLOWER INT NOT NULL,
                FOLLOWING INT NOT NULL,
                SUBMITVIDEOCOUNT INT NOT NULL,
                VIDEOVIEWCOUNT INT NOT NULL,
                ARTICLECOUNT INT NOT NULL,
                ARTICLEVIEWCOUNT INT NOT NULL,
                BANGUMICOUNT INT NOT NULL
                );
            '''
        )
        cursor.close()
        conn.close()

    def addUser(self, user):
        path = self.__path
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO USER VALUES ('%s', '%s', '%s', '%s', %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s)
            '''
            % (
                user.uid,
                user.nickName,
                user.sex,
                user.birthday,
                user.level,
                user.isVip,
                user.regTime,
                user.follower,
                user.following,
                user.submitVideoCount,
                user.videoViewCount,
                user.articleCount,
                user.articleViewCount,
                user.bangumiCount
            )
        )
        cursor.close()
        conn.commit()
        conn.close()

    def clear(self):
        pass
