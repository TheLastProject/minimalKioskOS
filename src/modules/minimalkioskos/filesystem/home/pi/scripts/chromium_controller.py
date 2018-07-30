import subprocess
import sys
import time

import pychrome

class ChromiumController():
    def __init__(self):
        self.kiosk_url = sys.argv[-2]

        try:
            self.mutetime = int(sys.argv[-1])
        except ValueError:
            self.mutetime = 0

        self.mutetimeleft = -1

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
            if self.mutetimeleft > 0:
                self.mutetimeleft -= 1
            elif self.mutetimeleft == 0:
                subprocess.run(['amixer', 'set', 'PCM', 'unmute'], check=True)

            time.sleep(1)

    def _response_received(self, **kwargs):
        # We only care about the main page loading, not of any subelement
        if (kwargs['type'] != 'Document' or self.tab.DOM.getDocument()['root']['children'][-1]['frameId'] != kwargs['frameId']):
            return

        if str(kwargs['response']['status']).startswith(('4', '5')):
            self._loading_failed(**kwargs)
            return

        if self.mutetime > 0:
            subprocess.run(['amixer', 'set', 'PCM', 'mute'], check=True)

            self.mutetimeleft = self.mutetime

    def _loading_failed(self, **kwargs):
        # We only care about the main page loading, not of any subelement
        if (kwargs['type'] != 'Document' or self.tab.DOM.getDocument()['root']['children'][-1]['frameId'] != kwargs['frameId']):
            return

        time.sleep(5)
        self._load_page()

    def _load_page(self):
        self.tab.Page.navigate(url=self.kiosk_url)

while True:
    try:
        chromium_controller = ChromiumController()
        chromium_controller.run_forever()
    except:
        time.sleep(10)
