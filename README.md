# contact_transfer
 

Description:

This program finds the GitHub user by its username and updates user's info in respective freshdesk contact.
	- If there is no such GitHub user the program returns 'Github user not found'.
	- If the GitHub user is found, the program checks if such contact (by email address) exists in freshdesk.
		- If there is no such fresdesk contact, the program creates it.
		- If such contact exists, the program updates its contact info in the compatible fields (email, name, twitter_id).
	If create/update is successful the program returns 'Contact synced: email'.
	If create/update is unsuccessful the program returns 'FreshDesk Error'.

Requirements:

In order to run the program and unittests you need installed Python 3.7 and the module 'requests'.
There is a "requirements.txt" in the program folder.
In order to work properly program needs GitHub and freshdesk authorization tokens as environmental variables GITHUB_TOKEN and FRESHDESK_TOKEN.

Usage:

Tha program can be started from command prompt in the project folder with next parameters:
	'-g' - GitHub username;
	'-f' - freshdesk subdomain;
Both parameters are required.

Example: python contact_transfer.py -g github_username -f freshdesk_subdomain

The unit tests files are placed in the main program folder. They can be started without parameters from the command prompt in the project folder. 

Example: python test_contact_transfer.py

The tests are separated in different files for each module.
