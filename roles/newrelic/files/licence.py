#!/usr/bin/python

import requests
from lxml import html
import re
import sys
from requests.exceptions import RequestException


def get_key():
    user = sys.argv[1]
    user_pw = sys.argv[2]
    login_url = "https://login.newrelic.com/login"
    account_url = "https://rpm.newrelic.com/accounts"

    session_requests = requests.session()

    data = {
        "login[email]": user,
        "login[password]": user_pw
    }

    # Perform login
    try:
        login = session_requests.post(login_url, data=data,
                                      headers=dict(referer=login_url))
    except RequestException as e:
        print ('ERROR: Could not log into newrelic\'s control panel.'
               '\n{0}'.format(e))

    # scrape account number url
    try:
        account_result = (session_requests.get(
                          account_url, headers=dict(referer=account_url)))
    except RequestException as e:
        print ('ERROR: Could not get the account number url page.'
               '\n{0}'.format(e))

    account_tree = html.fromstring(account_result.content)
    account_number_url = account_tree.xpath("//li[@class='insights']/a/@href")

    if not account_number_url:
        print ('ERROR: Could not retrieve account number. This could be '
               'due to incorrect credentials. You could try to manually '
               'login to newrelic\'s control panel, get the licence key'
               ' and then re-run this script')
        sys.exit()

    # with account number, we can go to the licence key page
    account_number = re.search(r'\d+$', account_number_url[0]).group()

    # scrape licence key
    try:
        licence_result = session_requests.get('{}/{}'.format(account_url,
                                                         account_number),
                                          headers=dict(referer=account_url))
    except RequestException as e:
        print ('ERROR: Could retrieve licence key.'
               '\n{0}'.format(e))
        
    licence_tree = html.fromstring(licence_result.content)
    licence = licence_tree.xpath("//code[@id='license_key']/text()")

    return licence[0]


def main():
    licence_key = get_key()
    print licence_key


if __name__ == '__main__':
    main()
