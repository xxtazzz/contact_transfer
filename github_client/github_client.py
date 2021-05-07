# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 20:52:03 2021

@author: gdimitrov
"""
import requests
import os
import json


class GithubClient:
    def get_compatible_user_data(self, username):
        response = requests.get(self.url(username), headers = self.headers())
        if (response.status_code == 200):
            user_data = json.loads(response.text)
            return {
                'email': user_data['email'],
                'name': user_data['name'],
                'twitter_id': user_data['twitter_username'],
            }
            return json.loads(response.text)
        else:
            return None

    def url(self, username):
         return 'https://api.github.com/users/' + username

    def headers(self):
        print(os.environ["GITHUB_TOKEN"])
        return  {'Authorization' : "token " + os.environ["GITHUB_TOKEN"], "Accept": "application/vnd.github.v3+json"}



