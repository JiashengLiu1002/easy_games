#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Liu Jiasheng


# import tkinter
import tkinter as tk
import random
import time

import logging

import threading
import os

from PIL import Image, ImageTk
# import tkutils as tku
# import win_ai
# import win_single
# import win_multi

# result_str = tk.StringVar()

word_list = []
# temp_word_list = []

default_time_value = 120
time_value = default_time_value


class Guess:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (1000, 400))  # 窗体尺寸
        self.root.title("你来比划我来猜v1.1")
        self.__correct = 0
        self.__result_str = tk.StringVar()
        # self.__result_str.set("正确个数: 0")
        # print(self.__result_str)
        self.__time_str = tk.StringVar()
        logging.debug("test, str=%s" %(self.__result_str))
        self.__word = tk.StringVar()
        self.body()
        # self.time = threading.Timer()
        self.timer_config()
        self.__state = 1
        self.get_word_list('word_list.txt')

    def body(self):
        # ---------------------------------------------------------------------
        # 背景图片
        # ---------------------------------------------------------------------
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.result_fram = tk.Frame(self.main_frame)
        self.__result_str.set("正确个数: 0")
        result_str = "正确个数: 0"
        result_word = tk.Label(self.result_fram, textvariable=self.__result_str, bg='green', font=("Arial",24)).pack(side='left', padx=10)
        self.result_fram.pack(side="top", fill='both')
        # result_word.pack(side='top', fill='both')

        self.__time_str.set(time_value)
        tk.Label(self.result_fram, textvariable = self.__time_str, bg='white', font=("Arial", 24)).pack(side='left', padx=10)

        self.b_start = tk.Button(self.result_fram, text="开始", font=('Arial',24), command = self.start_callback)
        self.b_start.pack(side='right', padx=10)

        self.b_correct = tk.Button(self.result_fram, text="正确", font=('Arial', 24), command = self.correct_callback)
        self.b_correct.pack(side='right', padx=10)

        self.b_pass = tk.Button(self.result_fram, text="跳过", font=('Arial', 24), command = self.wrong_callback)
        self.b_pass.pack(side='right', padx=10)

        self.b_reset = tk.Button(self.result_fram, text="复位", font=('Arial', 24), command = self.reset_callback)
        self.b_reset.pack(side='right', padx=10)

        self.word_frame = tk.Frame(self.main_frame)
        self.word_frame.pack(side='bottom', expand=tk.YES, fill=tk.X)
        self.__word.set('猜词游戏')
        self.word_text = tk.Label(self.word_frame, textvariable=self.__word, bg="white", font=('Arial', 120), width=100, height=20)
        self.word_text.pack(side='bottom', expand=tk.YES, fill=tk.X)

    def get_word_list(self, file):
        if(not os.path.exists(file)):
            print("no file")
        else:
            global word_list
            with open(file, 'r') as f:
                for eachLiine in f.readlines():  # 读取文件的每一行
                    word_list.append(eachLiine)
                f.close()
                word_list = list(set(word_list))

    def update_word(self, list_w):
        len_list = len(list_w)
        if(len_list == 0):
            self.__word.set("没词了, 55555....")
        logging.debug("len=%d" %(len_list))
        rand = random.randint(0, len_list-1)
        self.__word.set(word_list[rand])
        print("num=%d" %rand)
        word_list.remove(word_list[rand])

    def reset_callback(self):
        self.__correct = 0
        self.__result_str.set("正确个数: %d" % (self.__correct))
        self.__word.set("猜词游戏")
        self.timer.cancel()
        # self.timer.join()
        self.__state = 1
        global time_value
        self.timer_config()
        time_value = default_time_value
        self.__time_str.set(time_value)


    def start_callback(self):
        self.__correct = 0
        self.__result_str.set("正确个数: %d" % (self.__correct))
        self.update_word(word_list)
        self.__state = 0
        self.timer.start()

    def correct_callback(self):
        if(self.__state):
            return
        self.__correct = self.__correct + 1
        self.__result_str.set("正确个数: %d" %(self.__correct))
        self.update_word(word_list)

    def wrong_callback(self):
        if(self.__state):
            return
        self.__result_str.set("正确个数: %d" % (self.__correct))
        self.update_word(word_list)

    def timer_config(self):
        # global timer
        self.timer = threading.Timer(1.0, self.time_update, None)
        self.timer.daemon = True
        # timer.start()

    def timeup(self):
        self.__word.set("时间到！")

    def time_update(self):
        if(self.__state):
            return
        global time_value
        time_value = time_value - 1
        self.__time_str.set(time_value)
        if(time_value > 0):
            self.timer = threading.Timer(1.0, self.time_update, None)
            self.timer.run()
        else:
            self.timer.cancel()
            self.timeup()


if __name__ == "__main__":
    guess = Guess()
    guess.root.mainloop()