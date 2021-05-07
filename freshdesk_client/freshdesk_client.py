# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:13:55 2021

@author: gdimitrov
"""
import requests
import json
import os


class FreshDeskClient:
    SUCCESS_STATUSES = [200, 201]

    def sync_contact(self, subdomain, contact_info):
        existing_contact_id = self.find_contact(subdomain, contact_info['email'])
        if existing_contact_id is not None:
            response = self.update_contact(subdomain, existing_contact_id, contact_info)
        else:
            response = self.create_contact(subdomain, contact_info)
        return response.status_code in self.SUCCESS_STATUSES

    def find_contact(self, subdomain, email):
        response = requests.get(
            'https://' + subdomain +'.freshdesk.com/api/v2/search/contacts?query="email:\'' + email+'\'"',
            auth = (os.environ["FRESHDESK_TOKEN"], "x"),
            headers = {"Content-Type" : "application/json"}
        )
        if (response.status_code == 200):
            contact_data = json.loads(response.text)

            if contact_data['total'] == 1:
                return contact_data['results'][0]['id']

        return None

    def create_contact(self, subdomain, contact_info):
        return requests.post(
            "https://" + subdomain + ".freshdesk.com/api/v2/contacts/",
            auth = (os.environ["FRESHDESK_TOKEN"], "x"),
            data = json.dumps(contact_info),
            headers = {"Content-Type" : "application/json"}
        )

    def update_contact(self, subdomain, contact_id, contact_info):
        return requests.put(
            "https://"+ subdomain + ".freshdesk.com/api/v2/contacts/" + str(contact_id),
            auth = (os.environ["FRESHDESK_TOKEN"], "x"),
            data = json.dumps(contact_info),
            headers = {"Content-Type" : "application/json"}
        )
