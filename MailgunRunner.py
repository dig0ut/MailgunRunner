import sys
import uuid
import requests
import argparse
from datetime import datetime

api_key = ""

usage = '''
  
Examples:

Retrieve all logs:

python3 MailgunRunner.py --logs -d domain.local

Output logs to json:

python3 MailgunRunner.py --logs -d domain.local -o outfile

Retrieve all message keys:

python3 MailgunRunner.py --keys -d domain.local

Retrieve a specific stored message:

python3 MailgunRunner.py --message -d domain.local -k message_key
'''

def get_logs(args):
    response = requests.get(
        "https://api.eu.mailgun.net/v3/"+ args.domain +"/log",
        #auth,
        auth=("api", api_key),
        params={"skip": 0,
                "limit": 300})
    #print(response.text)
    if args.out_json:
        filename = args.out_json
        file = open(filename, "w")
        file.write(response.text)
    else:
        print(response.text)

def get_ips():
    response = requests.get(
        "https://api.eu.mailgun.net/v3/ips",
        #auth,
        params={"dedicated": "true"},
        auth=("api", api_key))
    print(response.text)


def get_routes():
    return requests.get(
        "https://api.mailgun.net/v3/routes",
        auth=("api", api_key),
        params={"skip": 1,
                "limit": 1})


def convert_timestamp(input):
    raw_stamp = input
    if raw_stamp:
        number = str(raw_stamp).split('.')
        if len(number) > 0:
            unixtime = int(number[0])
        utc_timestamp = datetime.fromtimestamp(int(unixtime))  # using UTC timezone
        new_time = utc_timestamp.strftime("%d-%m-%Y %H:%M:%S")
    return new_time


def get_keys(args):
    if args.key is None:
        print("\n[!] Cannot retrieve messages without a domain. Specify a domain with -d DOMAIN\n")
        parser.parse_args(['-h'])
    response = requests.get(
        "https://api.eu.mailgun.net/v3/"+ args.domain + "/events",
        auth=("api", api_key),
        params={"event" : "accepted"})
    if response: 
        json_data = response.json()
    message_keys = []
    for event in json_data['items']:
        message_key = event['storage']['key']
        sender = event['envelope']['sender']
        recipient = event['message']['headers']['to']
        originating_ip = event['originating-ip']
        time_stamp = convert_timestamp(event['timestamp'])
        info = "Message key: "+ str(message_key)+ "\nSender: " + str(sender) + "\nRecipient: " + str(recipient) + "\nOriginating IP: " + str(originating_ip) + "\nUTC Timestamp: " + str(time_stamp) + "\n"
        message_keys.append(info)
    print("[+] All message keys and their associated senders:\n")
    return message_keys


def print_keys(args):
    for each in get_keys(args):
        print(each)


def get_stored_message(args):
    
    if args.action == get_stored_message:
        if args.key is None:
            print("[!] A message key is needed to retrieve stored messages! These can be retrieved by running the '--keys' option.")
            parser.parse_args(['-h'])

    key = args.key
    param1 = str(args.domain)
    param2 = str(uuid.uuid4())
    #param2 = str(key)

    # output filename
    filename = "message_" + param1 + "_" + param2 + ".eml"

    # url for retrieval
    url = "https://storage-europe-west1.api.mailgun.net/v3/domains/%s/messages/%s"
    url = url % (args.domain, key)

    headers = {"Accept": "message/rfc2822"}

    # request to API
    r = requests.get(url, auth=("api", api_key), headers=headers)
    if r.status_code == 200:
        print("[+] Key matches existing message")
        print("[+] Writing message to " + filename)
        with open(filename, "w") as message:
            message.write(r.json()["body-mime"])
      #os.system("thunderbird -file %s" % filename)
    else:
      print("[!] Something went wrong: %s" % r.content)


if __name__ == '__main__':
    
    if api_key == '':
        print("[!] Mailgun API key needed! Add this to the 'api_key' variable.\n")
        sys.exit(-1)

    parser = argparse.ArgumentParser(
    description='Get Mailgun logs, message keys and stored messages for a given domain name.')

    parser.add_argument('--logs', dest='action', action='store_const', const=get_logs)
    parser.add_argument('--message', dest='action', action='store_const', const=get_stored_message)
    parser.add_argument('--keys', dest='action', action='store_const', const=print_keys)
    parser.add_argument("-d", dest="domain", help="Name of domain to query.")
    parser.add_argument("-k", dest="key", help="Message key to stored message to retrieve.")
    parser.add_argument("-o", dest="out_json", help="Ouput raw results to JSON in current directory.")
    args = parser.parse_args()
    if args.action is None:
        parser.parse_args(['-h'])
    args.action(args)






