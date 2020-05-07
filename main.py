from src.JsonTool import JsonTool
from src.VkSeleniumDriverTools import VkSeleniumDriverTools
from src.ResourceScheduler import ResourceScheduler
from src.Reg import initReg
import time

def parse_data(posts):
    titles = dict()
    texts = dict()
    images = dict()
    for key in posts.keys():
        if key in titles.keys():
            continue
        titles[key] = posts[key]['title']
        texts[key] = posts[key]['text']
        images[key] = posts[key]['images']
    return [titles, texts, images]


def main():
    initReg()
    config = JsonTool.parse("config.json")      # Подгружаем конфигурационный файл
    vkTools = VkSeleniumDriverTools(config)     # Передаем его в парсер
    vkTools.login()                             # Авторизируемся
    vkTools.go_to_feeds()                       # Идем на страницу новостей

    rs = ResourceScheduler(config)
    rs.update_table()
    rs.print_table()

    while True:
        posts = vkTools.get_feeds()  
        titles, texts, images = parse_data(posts)
        rs.update_data(titles, texts, images)
        rs.step()
        #time.sleep(1)
        #print("refresh page")
        vkTools.refresh_page()
        #print("refreshed")

if __name__ == '__main__':
    main()
        
