import os
import sys
import time
import httpx
import signal
import threading
import win32api
import win32gui
import win32com
import win32com.client
from win32con import *
from loguru import logger
from enum import Enum


class NetworkResult(Enum):
    NORMAL = 0
    NEED_LOGIN = 1
    BAD_CONNECTION = -1


class ESurfingDaemon(object):
    def __init__(self):
        default = "C:/Program Files (x86)/Chinatelecom_GDPortal/EsurfingClient.exe"
        self.timeout = int(os.environ.get("ESURFING_TIMEOUT", 30))
        self.retry = int(os.environ.get("ESURFING_RETRY", 3))
        self.interval = int(os.environ.get("ESURFING_INTERVAL", 15))
        self.server = os.environ.get("ESURFING_SERVER", "http://223.5.5.5/")
        self.executable = os.environ.get("ESURFING_EXECUTABLE", default)
        self.hwnd = None
        self.shell = win32com.client.Dispatch('WScript.Shell')
        self.client = httpx.Client(timeout=self.timeout)
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)

    @staticmethod
    def click(x, y):
        width = win32api.GetSystemMetrics(SM_CXSCREEN)
        height = win32api.GetSystemMetrics(SM_CYSCREEN)
        win32api.mouse_event(
            MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE,
            int(x * 65536 / width), int(y * 65536 / height),
            0, 0
        )
        win32api.mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def stop():
        os.system('taskkill /f /im ESurfingClient.exe >nul 2>&1')

    @staticmethod
    def signal_handler(_, __):
        os.system("pssuspend -r ESurfingClient.exe >nul 2>&1")
        os.system("pssuspend64 -r ESurfingClient.exe >nul 2>&1")
        sys.exit(0)

    def check(self, url, disable=False):
        # noinspection PyBroadException
        try:
            response = self.client.get(url)
            if response.status_code == 302 and not disable:
                logger.warning("Session is expired. Now relaunch the client.")
            return NetworkResult.NORMAL if response.status_code == 404 else NetworkResult.NEED_LOGIN
        except:
            if not disable:
                logger.warning("Connection bad. Please check your connection.")
            return NetworkResult.BAD_CONNECTION

    def login(self):
        self.running = True
        while self.running:
            self.shell.SendKeys('%')
            win32gui.SetForegroundWindow(self.hwnd)
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            self.click((left + right) / 2, top + 397)
            time.sleep(1)

    def start(self):
        os.startfile(self.executable)
        logger.info('Wait for window...')
        while not win32gui.FindWindow("wkeWebWindow", '校园客户端'):
            continue
        self.hwnd = win32gui.FindWindow("wkeWebWindow", '校园客户端')
        thread = threading.Thread(target=self.login)
        now = time.time()
        logger.info('Logining...')
        thread.start()
        while self.check(self.server, True) is not NetworkResult.NORMAL and time.time() - now < self.timeout:
            time.sleep(0.5)
        self.running = False
        win32gui.ShowWindow(self.hwnd, SW_MINIMIZE)
        os.system("pssuspend ESurfingClient.exe >nul 2>&1")
        os.system("pssuspend64 ESurfingClient.exe >nul 2>&1")
        logger.info('Login successfully.')

    def watch(self):
        self.start()
        bad = 0
        while True:
            result = self.check(self.server)
            if result is NetworkResult.NEED_LOGIN or bad >= self.retry:
                self.stop()
                self.start()
            elif result is NetworkResult.BAD_CONNECTION:
                bad += 1
            elif result is NetworkResult.NORMAL:
                bad = 0
            time.sleep(self.interval)


ESurfingDaemon().watch()
