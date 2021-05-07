# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:53:36 2021

@author: gdimitrov
"""
import argparse
from github_client.github_client import GithubClient
from freshdesk_client.freshdesk_client import FreshDeskClient

class ContactTransfer:
    def copy_contact_info(self, github_user, freshdesk_subdomain):
        github_client = GithubClient()
        freshdesk_client = FreshDeskClient()

        contact_info = github_client.get_compatible_user_data(github_user)

        if contact_info is None:
            return 'Github user not found'

        result = freshdesk_client.sync_contact(freshdesk_subdomain, contact_info)

        if result == True:
            return 'Contact synced: ' + contact_info['email']
        else:
            return 'FreshDesk Error'


if __name__=='__main__':

    argparser = argparse.ArgumentParser(description='List the content of a folder')
    argparser.add_argument('-g', metavar='gh_user', type=str, help='gitHub username', required=True)
    argparser.add_argument('-f', metavar='fd_subdomain', type=str, help='freshDesk subdomain', required=True)

    args = argparser.parse_args()
    github_user = args.g
    fresh_subdomain = args.f

    data_migrator = ContactTransfer()
    print(data_migrator.copy_contact_info(github_user, fresh_subdomain))




