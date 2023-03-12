import scrapy
from scrapy.http import HtmlResponse
from InstaSpyder.items import InstaspyderItem


class InstaspySpider(scrapy.Spider):
    name = "instaspy"
    allowed_domains = ["graph.instagram.com"]
    start_urls = ["https://graph.instagram.com/me?fields=id,username,media&access_token=IGQVJVSjl5dHpXSkw2TkU2eFI4dmt6M1QyV0lELUtDeWxQUTBIekxkcTFVMXhwRFdMVW9wYTQzSFQxQmxxcjlsRG5lNF9WbHJQWVYzNmlzamNfYU9lT1VXRTUwMDJDRzg0YXFCV1VDMk9WY0lkMFduNwZDZD"]

    def parse(self, response:HtmlResponse):
        data = response.json()
        img_id_list = [thing['id'] for thing in data['media']['data']]
        for img_id in img_id_list:
            yield response.follow(f'https://graph.instagram.com/{img_id}?fields=id,media_type,username,timestamp,media_url&access_token=IGQVJVSjl5dHpXSkw2TkU2eFI4dmt6M1QyV0lELUtDeWxQUTBIekxkcTFVMXhwRFdMVW9wYTQzSFQxQmxxcjlsRG5lNF9WbHJQWVYzNmlzamNfYU9lT1VXRTUwMDJDRzg0YXFCV1VDMk9WY0lkMFduNwZDZD', callback=self.parse_photos)


    def parse_photos(self, response:HtmlResponse):
        answer = response.json()
        media_id = answer['id']
        media_type = answer['media_type']
        user_name = answer['username']
        time_stamp = answer['timestamp']
        media_url = answer['media_url']


        yield InstaspyderItem(
            media_id = media_id,
            media_type = media_type,
            user_name = user_name,
            time_stamp = time_stamp,
            media_url = media_url
        )
