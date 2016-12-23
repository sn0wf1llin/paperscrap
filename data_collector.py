__author__ = 'MA573RWARR10R'
import requests
import json


class FacebookDataCollector:
    def __init__(self, api_version, access_token):
        self._api_version = api_version
        self._access_token = access_token

    def get_data(self, url):
        req = requests.get('https://graph.facebook.com/{api_version}/?id={url}&access_token={access_token}&date_format=U'.format(
            url=url, api_version=self._api_version, access_token=self._access_token))
        base_content = req.content.decode("UTF-8")
        json_data = json.loads(base_content)
        if 'error' in json_data:
            print("Error")
            raise ValueError("API received error!\n" + base_content)

        req = requests.get('https://graph.facebook.com/{api_version}/{id}/likes?access_token={access_token}&summary=true'.format(
            api_version=self._api_version, access_token=self._access_token, id=json_data['og_object']['id']))
        likes_content = req.content.decode("UTF-8")
        likes_json = json.loads(likes_content)
        if 'error' in likes_json:
            print("Error")
            raise ValueError("API received error!\n" + likes_content)

        return {
            "social": "facebook",
            "updated_time": json_data['og_object']['updated_time'],
            "comments": json_data['share']['comment_count'],
            'reposts': json_data['share']['share_count'],
            'likes': likes_json['summary']['total_count'],
        }