# Network monitoring tool
this is a network monitoring tool. It works by pinging serveral hosts bij domain name or IP

# Copy repository
To download the repository in a linux machine enter the following command:
```
git clone https://github.com/Romny468/monitoring.git
```
For windows you can open the following url:
https://github.com/Romny468/monitoring/archive/refs/heads/main.zip 

# Before use
If you are using Gmail as the sender email make sure the option "allow less secure apps is turned on" via 
https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MwNDlHS3z076dVrKM8Zn9nxVMQGK9CwVIiNA_CiTiftSPTWfcSsLFh4LShJttaSaPCj4sxmCG9MMyT11Ujsc_1LxJMwg

# First use
On the first use a config file will be created. This is called "config.yml".
This file contains the webserver addresses, IP-addresses and the email configuration. The list "addresses" is the list of hosts that will be tested.
The email information must be filled with an actual account in order to receive an email if a host in the list is not reachable or down.
The file can be edited in a normal text editor. Make sure the yml structure is correct. Here is an example of the newly created config file
```
addresses:
- google.com
- 127.0.0.1
- nu.nl
- spele.nl

sender: sender_email
password: sender_password
smtp: smtp.gmail.com
port: 465
receivers:
- email1
- email2
```

# Supported operating systems
All operating system should work. It has been tested on:
- Windows
- Ubuntu