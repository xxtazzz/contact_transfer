# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 20:52:28 2021

@author: gdimitrov
"""

import unittest
import json
import os
from unittest.mock import patch
from freshdesk_client.freshdesk_client import FreshDeskClient

class TestResponse(object):
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = json.dumps({
            'results': [{'id': '123'}],
            'total': 1
        })

class TestCases(unittest.TestCase):
    def setUp(self):
        self.freshdesk_client = FreshDeskClient()
        self.contact_info = {
            'email': 'octocat@github.com',
            'name': 'The Octocat',
            'twitter_id': None,
        }

    def test_sync_existing_contact(self):
        with patch('freshdesk_client.freshdesk_client.FreshDeskClient.find_contact', return_value = '123'):
            with patch('freshdesk_client.freshdesk_client.FreshDeskClient.update_contact') as mock_update:
                self.freshdesk_client.sync_contact('quicktest', self.contact_info)
                mock_update.assert_called_with('quicktest', '123', self.contact_info)

    def test_sync_new_contact(self):
         with patch('freshdesk_client.freshdesk_client.FreshDeskClient.find_contact', return_value = None):
            with patch('freshdesk_client.freshdesk_client.FreshDeskClient.create_contact') as mock_create:
                self.freshdesk_client.sync_contact('quicktest', self.contact_info)
                mock_create.assert_called_with('quicktest', self.contact_info)


    def test_find_contact(self):
        with patch('freshdesk_client.freshdesk_client.requests.get', return_value = TestResponse(200)):
            existing_contact_id = self.freshdesk_client.find_contact('quicktest', 'octocat@github.com')
            self.assertEqual(existing_contact_id, '123')

    def test_can_not_find_contact(self):
        with patch('freshdesk_client.freshdesk_client.requests.get', return_value = TestResponse(400)):
            existing_contact_id = self.freshdesk_client.find_contact('quicktest', 'octocat@github.com')
            self.assertEqual(existing_contact_id, None)

    def test_find_contact_request(self):
        with patch('freshdesk_client.freshdesk_client.requests.get') as mock_requests:
            self.freshdesk_client.find_contact('quicktest', 'octocat@github.com')
            mock_requests.assert_called_with(
                'https://quicktest.freshdesk.com/api/v2/search/contacts?query="email:\'octocat@github.com\'"',
                 auth = (os.environ["FRESHDESK_TOKEN"], "x"),
                 headers = {"Content-Type" : "application/json"},
            )

    def test_update_contact_request(self):
        with patch('freshdesk_client.freshdesk_client.requests.put') as mock_requests:
            self.freshdesk_client.update_contact('quicktest', '123', self.contact_info)
            mock_requests.assert_called_with(
                 "https://quicktest.freshdesk.com/api/v2/contacts/123",
                 auth = (os.environ["FRESHDESK_TOKEN"], "x"),
                 data = json.dumps(self.contact_info),
                 headers = {"Content-Type" : "application/json"},
            )

    def test_create_contact_request(self):
        with patch('freshdesk_client.freshdesk_client.requests.post') as mock_requests:
            self.freshdesk_client.create_contact('quicktest', self.contact_info)
            mock_requests.assert_called_with(
                 "https://quicktest.freshdesk.com/api/v2/contacts/",
                 auth = (os.environ["FRESHDESK_TOKEN"], "x"),
                 data = json.dumps(self.contact_info),
                 headers = {"Content-Type" : "application/json"},
            )


if __name__ == "__main__":
    unittest.main()


