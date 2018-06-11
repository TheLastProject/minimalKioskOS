import sys
import time

import pychrome

while True:
    try:
        global tab

        browser = pychrome.Browser(url="http://127.0.0.1:9222")
        tab = browser.list_tab()[0]

        def loading_failed(**kwargs):
            # We only care about HTML failing to load
            # Others are likely not network issues
            if (kwargs['type'] != 'Document'):
                return

            time.sleep(5)
            global tab
            tab.Page.navigate(url=sys.argv[-1])

        tab.Network.loadingFailed = loading_failed

        tab.start()
        tab.Network.enable()
        tab.Page.navigate(url=sys.argv[-1])

        while True:
            time.sleep(1)
    except:
        time.sleep(10)
