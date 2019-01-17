import os
import subprocess
import sys
import time

import pychrome

class ChromiumController():
    def __init__(self):
        self.env = os.environ.copy()
        self.env["DISPLAY"] = ":0"

        self.kiosk_urls = []
        self.kiosk_urls_display_time = []
        self.kiosk_urls_keypresses = []
        self.spamkeys = []

        with open("/boot/urls.txt", "r") as kiosk_urls_file:
            line = kiosk_urls_file.readline()
            while line:
                data = line.split(' ')
                self.kiosk_urls.append(data[0])
                self.kiosk_urls_display_time.append(int(data[-1]) if len(data) > 1 else -1)
                self.kiosk_urls_keypresses.append(data[1:-1] if len(data) > 2 else [])
                line = kiosk_urls_file.readline()

        with open("/boot/spamkey.txt", "r") as spamkey_file:
            line = spamkey_file.readline()
            if line:
                self.spamkeys = line.split(' ')

        try:
            self.mute_time = int(sys.argv[-1])
        except ValueError:
            self.mute_time = 0

        self.current_kiosk_url_index = 0
        self.next_url_time_left = -1
        self.mute_time_left = -1

        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.tab = self.browser.list_tab()[0]
        self.initial_load = True

        self.tab.Network.responseReceived = self._response_received
        self.tab.Network.loadingFailed = self._loading_failed

        self.tab.start()
        self.tab.DOM.enable()
        self.tab.Network.enable()
        self._load_page()

    def run_forever(self):
        while True:
            if self.kiosk_urls_display_time[self.current_kiosk_url_index] >= 0:
                if self.next_url_time_left >= 0:
                    self.next_url_time_left -= 1
                else:
                    self.next_url_time_left = self.kiosk_urls_display_time[self.current_kiosk_url_index]

                if self.next_url_time_left == 0:
                    self._load_page()

            if self.mute_time_left > 0:
                self.mute_time_left -= 1
            elif self.mute_time_left == 0:
                subprocess.run(['amixer', 'set', 'PCM', 'unmute'], check=True)

            time.sleep(1)

    def _response_received(self, **kwargs):
        # We only care about the main page loading, not of any subelement
        if (kwargs['type'] != 'Document' or self.tab.DOM.getDocument()['root']['children'][-1]['frameId'] != kwargs['frameId']):
            return

        if str(kwargs['response']['status']).startswith(('4', '5')):
            self._loading_failed(**kwargs)
            return

        if self.mute_time > 0:
            subprocess.run(['amixer', 'set', 'PCM', 'mute'], check=True)

            self.mute_time_left = self.mute_time

        if self.initial_load:
            if self.kiosk_urls_keypresses[self.current_kiosk_url_index]:
                time.sleep(5)
                for key in self.kiosk_urls_keypresses[self.current_kiosk_url_index]:
                    command, data = key.split(':', 1)
                    chromium_window_id = subprocess.check_output(['xdotool', 'search', '--onlyvisible', '--class', 'chromium'], env=self.env).splitlines()[0]
                    subprocess.run(['xdotool', 'windowactivate', chromium_window_id], check=True, env=self.env)
                    subprocess.run(['xdotool', command, data], check=True, env=self.env)

            self.initial_load = False
        else:
            for key in self.spamkeys:
                command, data = key.split(':', 1)
                chromium_window_id = subprocess.check_output(['xdotool', 'search', '--onlyvisible', '--class', 'chromium'], env=self.env).splitlines()[0]
                subprocess.run(['xdotool', 'windowactivate', chromium_window_id], check=True, env=self.env)
                subprocess.run(['xdotool', command, data], check=True, env=self.env)

    def _loading_failed(self, **kwargs):
        # We only care about the main page loading, not of any subelement
        if (kwargs['type'] != 'Document' or self.tab.DOM.getDocument()['root']['children'][-1]['frameId'] != kwargs['frameId']):
            return

        time.sleep(5)
        self._load_page()

    def _load_page(self):
        self.tab.Page.navigate(url=self.kiosk_urls[self.current_kiosk_url_index])

while True:
    try:
        chromium_controller = ChromiumController()
        chromium_controller.run_forever()
    except:
        time.sleep(10)
