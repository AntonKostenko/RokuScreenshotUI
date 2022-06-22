from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
import os
import platform


class MyGrid(BoxLayout):
    Window.size = (450, 200)
    main_text = StringProperty('Roku Screenshot Utility')
    screenshot = ObjectProperty(None)
    package = ObjectProperty(None)

    def roku_screenshot(self, ip_address, dev_password):
        now = datetime.now()
        current_time = now.strftime("%m%d_%H_%M_%S")

        if platform.system() == 'Windows':
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        else:
            desktop = os.path.join(os.path.expanduser('~'), 'desktop')

        command_url = 'http://%s/plugin_inspect'
        image_url = 'http://%s/pkgs/dev.jpg'
        save_location = desktop + '/'+ ip_address + '_' + current_time + '.jpg'
        auths = HTTPDigestAuth('rokudev', dev_password)
        files = dict(archive='', passwd='', mysubmit='Screenshot')

        # Logic to take the screenshot
        r = requests.post(command_url % ip_address, auth=auths, files=files, timeout=6)
        if r.status_code == 200:
            # Save the image to desktop
            r = requests.get(image_url % ip_address, auth=auths)
            if r.status_code == 200:
                with open(save_location, 'wb') as f:
                    f.write(r.content)
                    self.main_text = 'Screenshot is on your desktop :)'
            else:
                self.main_text = 'Are you sure the dev app is open?'

    def screen_shot_button(self):
        try:
            self.roku_screenshot(self.ip_address.text, self.dev_password.text)
        except requests.exceptions.InvalidURL:
            self.main_text = 'Roku Screenshot Utility'
        except requests.exceptions.Timeout:
            self.main_text = 'Request timed out. Check dev mode and IP'
        except requests.exceptions.ConnectionError:
            self.main_text = 'Connection error. Try again or check dev mode and IP?'


class ScreenshotApp(App):
    def build(self):
        return MyGrid()

if __name__ == '__main__':
    ScreenshotApp().run()
