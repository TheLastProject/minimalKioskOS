import subprocess
import sys
import time

import pychrome

class ChromiumController():
    def __init__(self):
        self.kiosk_urls = sys.argv[:-3]

        try:
            self.next_url_time = int(sys.argv[-2])
        except ValueError:
            self.next_url_time = -1

        try:
            self.mute_time = int(sys.argv[-1])
        except ValueError:
            self.mute_time = 0

        self.current_kiosk_url_index = 0
        self.next_url_time_left = self.next_url_time
        self.mute_time_left = -1

        self.browser = pychrome.Browser(url="http://127.0.0.1:9222")
        self.tab = self.browser.list_tab()[0]

        self.tab.Network.responseReceived = self._response_received
        self.tab.Network.loadingFailed = self._loading_failed

        self.tab.start()
        self.tab.DOM.enable()
        self.tab.Network.enable()
        self._load_page()

    def run_forever(self):
        while True:
            if self.next_url_time_left > 0:
                self.next_url_time_left -= 1
            elif self.next_url_time_left == 0:
                if self.current_kiosk_url_index < len(self.kiosk_urls):
                    self.current_kiosk_url_index += 1
                else
                    self.current_kiosk_url_index = 0

                self.next_url_time_left = self.next_url_time
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
