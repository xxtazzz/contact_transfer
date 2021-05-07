# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:21:26 2021

@author: gdimitrov
"""

import unittest
from unittest.mock import patch
from contact_transfer import ContactTransfer #as CTrans


class TestCases_ContactTransfer(unittest.TestCase):
    def setUp(self):
        self.contact_transfer = ContactTransfer()
        self.contact_info = {
            'email': 'octocat@github.com',
            'name': 'The Octocat',
            'twitter_id': None,
        }

    def test_github_user_not_found(self):
         with patch('github_client.github_client.GithubClient.get_compatible_user_data', return_value = None):
             result = self.contact_transfer.copy_contact_info('octocat@github.com', 'quicktest')
             self.assertEqual(result, 'Github user not found')

    def test_contact_synced(self):
         with patch('github_client.github_client.GithubClient.get_compatible_user_data', return_value = self.contact_info):
             with patch('freshdesk_client.freshdesk_client.FreshDeskClient.sync_contact', return_value = True):
                 result = self.contact_transfer.copy_contact_info('octocat@github.com', 'quicktest')
                 self.assertEqual(result, 'Contact synced: octocat@github.com')

    def test_freshdesk_error(self):
         with patch('github_client.github_client.GithubClient.get_compatible_user_data', return_value = self.contact_info):
             with patch('freshdesk_client.freshdesk_client.FreshDeskClient.sync_contact', return_value = False):
                 result = self.contact_transfer.copy_contact_info('octocat@github.com', 'quicktest')
                 self.assertEqual(result, 'FreshDesk Error')

if __name__ == "__main__":
    unittest.main()
