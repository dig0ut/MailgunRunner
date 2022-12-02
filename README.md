# MailgunRunner
Interacts with Mailgun API to retrieve logs and stored messages.

## Usage:
```
usage: MailgunRunner.py [-h] [--logs] [--message] [--keys] [-d DOMAIN] [-k KEY] [-o OUT_JSON]

Get Mailgun logs, message keys and stored messages for a given domain name.

options:
  -h, --help   show this help message and exit
  --logs
  --message
  --keys
  -d DOMAIN    Name of domain to query.
  -k KEY       Message key to stored message to retrieve.
  -o OUT_JSON  Ouput raw results to JSON in current directory.
```

## Examples:

Retrieve all logs:
```
python3 MailgunRunner.py --logs -d domain.local
```
Output logs to json:
```
python3 MailgunRunner.py --logs -d domain.local -o outfile
```
Retrieve all message keys:
```
python3 MailgunRunner.py --keys -d domain.local
```
Retrieve a specific stored message:
```
python3 MailgunRunner.py --message -d domain.local -k message_key
```

## References:
- https://documentation.mailgun.com/en/latest/api_reference.html
