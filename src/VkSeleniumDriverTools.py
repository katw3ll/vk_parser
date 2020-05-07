from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import base64, time, re


class VkSeleniumDriverTools:

    def __init__(self, config):
        self.vk_login = base64.b64decode(config['vk']['auth']['login']).decode("utf-8") 
        self.vk_password = base64.b64decode(config['vk']['auth']['password']).decode("utf-8") 
        self.vk_login_url = config['vk']['urls']['login']
        self.vk_feed_url = config['vk']['urls']['feed']
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.webdriver = webdriver.Firefox()
    
    def login(self):
        self.webdriver.get(self.vk_login_url)
        login_field = self.webdriver.find_element_by_id('email')
        password_field = self.webdriver.find_element_by_id('pass')
        login_field.send_keys(self.vk_login)
        password_field.send_keys(self.vk_password + Keys.RETURN)
        time.sleep(5)
    
    def go_to_feeds(self):
        self.webdriver.get(self.vk_feed_url)

    def get_feeds(self):
        posts = dict()
        wall_data = self.webdriver.find_elements_by_class_name('feed_row')
        for d in wall_data:
            try:
                id = d.find_element_by_class_name('_post').get_attribute('data-post-id')
                title = d.find_element_by_class_name('post_header').find_element_by_class_name('author').text
                text = d.find_element_by_class_name('wall_post_text').text
                images = []
                images_temp = d.find_elements_by_class_name('image_cover')
                for img in images_temp:
                    temp = img.value_of_css_property('background-image')
                    images.append(temp[5:-2])
                if(title != ''):
                    posts[id] = {"title": title, "text": text,"images":images}
            except NoSuchElementException:
                pass
        return posts
    
    def refresh_page(self):
        self.webdriver.refresh()
