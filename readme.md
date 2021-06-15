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
Before using this program a file must be created in the same folder as the program.
Thsi file should contain some email data. It should look something like:
```
sender: 'Sender email'
password: 'Password Sender email'
smtp: 'smtp.gmail.com'
port: '465'

receivers: ['email1@gmail.com', 'email2@gmail.com']
```
If you are using gmail as send email make sure the option "allow less secure apps is turned on" via https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MwNDlHS3z076dVrKM8Zn9nxVMQGK9CwVIiNA_CiTiftSPTWfcSsLFh4LShJttaSaPCj4sxmCG9MMyT11Ujsc_1LxJMwg

# First use
On the first use a config file will be created. This is called "config.yml".
This file contains the webservers or IP addresses. The file can be edited in a normal text editor.
Make sure the yml structure is correct. Here is an example:
```
addresses:
- google.com
- nu.nl
- 127.0.0.1
- spele.nl
```

# Supported operating systems
All operating system should work. It has been tested on:
- Windows
- Ubuntu