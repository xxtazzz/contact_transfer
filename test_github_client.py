# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 20:52:28 2021

@author: gdimitrov
"""

import unittest
import json
import os
from unittest.mock import patch
from github_client.github_client import GithubClient


class TestResponse(object):
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = json.dumps({
            'email': 'octocat@github.com',
            'name': 'The Octocat',
            'twitter_username': None,
        })

class TestCases(unittest.TestCase):
    def setUp(self):
        self.github_client = GithubClient()

    def test_get_request(self):
        with patch('github_client.github_client.requests.get') as mock_requests:
            with patch.dict(os.environ, {"GITHUB_TOKEN": 'secret_token'}):
                self.github_client.get_compatible_user_data("xxtazzz")
                mock_requests.assert_called_with(
                    'https://api.github.com/users/xxtazzz',
                    headers={
                        'Authorization': 'token secret_token',
                        'Accept': 'application/vnd.github.v3+json'
                        }
                )

    def test_get_compatible_user_data(self):
        with patch('github_client.github_client.requests.get', return_value = TestResponse(200)):
            expected_user_data = {
                'email': 'octocat@github.com',
                'name': 'The Octocat',
                'twitter_id': None,
            }

            actual_user_data = self.github_client.get_compatible_user_data("octocat")
            self.assertEqual(actual_user_data, expected_user_data)

    def test_can_not_get_compatible_user_data(self):
        with patch('github_client.github_client.requests.get', return_value = TestResponse(404)):
            user_data = self.github_client.get_compatible_user_data("octocat")
            self.assertEqual(user_data, None)


if __name__ == "__main__":
    unittest.main()
