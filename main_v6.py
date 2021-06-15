try: import platform
except:
    print('module: "platform" not found, try installing before running')
    exit()

# check which os is running
def os_check():
    if platform.system() == "Windows": return True
    else: return False

# install yaml if needed
def module_install(package):
    if os_check(): os.system("python -m pip install" + package)
    else: os.system("python3 -m pip install" + package)

# import all other modules
try:
    import os, yaml, smtplib, time
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except:
    print("error while loading modules! Trying to install them")
    try:
        module_install("yaml")
        import yaml
    except:
        print("\n\nInstall failed, exiting!")
        exit()

# function for the first startup
# creates a config file with mail an address list and mail settings.
def first_start():
    if not os.path.exists('config.yml'):
        new_file = {'addresses': ['google.com', '127.0.0.1', 'nu.nl', 'spele.nl'],
                    'sender': 'sender_email', 'password': 'sender_password', 'smtp': 'smtp.gmail.com', 'port': 465,
                    'receivers': ['email1', 'email2']}
        with open('config.yml', 'w') as file: yaml.dump(new_file, file, sort_keys=False)
        print("\nplease edit the config file that has just been created"
              "\nenter mail data so the program can send mail to one or more recipients before running again"
              "\n\nin the address list you can add or delete websites or ip addresses. make sure the structure stays the same.")
        time.sleep(8)
        exit()

# ask the user a question and check for right answer
def question(question):
    while True:
        check1 = input(question + " ([yes]/no): ")
        if check1 == "yes": return True
        elif check1 == "no": return False
        else: print('\nthe question must be answered with "yes" or "no"!')

# open yaml file as data
# might remove this function since it is only used once (which adds about 2 lines of code)
def yaml_loader(filepath):
    with open(filepath) as yml_data:
        data = yaml.safe_load(yml_data)
        return data

# main function
def main():
    first_start()
    not_responsive = []
    try:
        yaml_loader("config.yml")
    except:
        print("\nthe yaml file is not correctly edited.")
        if question("do you want me to create a new config file?"):
            print('\nyou chose "yes"')
            time.sleep(2)
            os.remove("config.yml")
            first_start()
            main()
        else:
            print('\nyou chose "no"',"\n\nplease edit the address lsit in the config file to the following structure before running again:\naddresses:\n- website1\n- website2\n- ip-address")
            time.sleep(4)
            exit()

    # check on which os is running and adapt to os
    if os_check(): param = "-n"
    else: param = "-c"

    # ping all hosts in config file
    # if hosts are offline add to not_responsive list
    data = yaml_loader("config.yml")
    for ip in data["addresses"]:
        response = os.system("ping " + param + " 1 " + ip)
        if response == 0: print("Ping to:", ip, "was successful")
        else:
            print("Ping to:", ip, "was unsuccessful")
            not_responsive.append(ip)
    if not_responsive: send_mail(not_responsive)

# mail function
def send_mail(not_responsive):
    with open("config.yml") as yml_data:
        config = yaml.safe_load(yml_data)
        try:
            sender = config["sender"]
            password = config["password"]
            smtp = config["smtp"]
            port = config["port"]
            receivers = config["receivers"]
            msg = MIMEMultipart('alternative')
            html = f"""
            <div><header style="background-color: #f9a41a; padding: 15px; width: auto;">
            <h1 style="text-align: center; color: ##000000;">Server monitoring</h1>
            </header></div>
            <div style="font-size: 20px; width: auto;">
            <p>Offline servers:</p>
            <ul>"""
            for x in not_responsive:
                html += f"""
                <li>{x}</li>
                """
            html += """</ul>
            </div>
            <div><footer style="background-color: #5eff3356388; padding: 15px; width: auto;">This is an automatically generated email. Please do not reply to it. <br />If you have any questions please send an email to: <em>nowhere</em></footer></div>
            """
            mailtext = MIMEText(html, 'html')

            msg['Subject'] = f"One or more hosts are down"
            msg['From'] = sender
            msg['To'] = 'monitor@fontys.nl'
            msg.attach(mailtext)

            try:
                smtp_server = smtplib.SMTP_SSL(smtp, port)
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, receivers, msg.as_string())
                print("email has been send")
                smtp_server.close()
            except smtplib.SMTPConnectError: print("ERROR: connecting during the connection with the SMTP server")
            except smtplib.SMTPServerDisconnected: print("ERROR: an email has been tried to be send but the SMTP sever disconnected")
            except smtplib.SMTPRecipientsRefused: print("ERROR: cannot send an email, recipient refused. Make sure receiver setting is not empty!")
            except smtplib.SMTPSenderRefused: print("ERROR: The senders address refused")
            except smtplib.SMTPResponseException as e:
                print("ERROR: an email has been tried to be send but the SMTP server returned an error code")
                error_code = e.smtp_code
                error_message = e.smtp_error
                print("Error code:", error_code)
                print("Message:", error_message)
                if (error_code == 422): print("Recipient Mailbox Full")
                elif (error_code == 431): print("Server out of space")
                elif (error_code == 447): print("Timeout. Try reducing number of recipients")
                elif (error_code == 510 or error_code == 511): print("One of the addresses doesn't exist. Check again your recipients accounts and correct any possible misspelling.")
                elif (error_code == 512): print("Check all your recipients addresses: there will likely be an error in a domain name.")
                elif (error_code == 541 or error_code == 554): print("Your message has been detected and labeled as spam. You must ask the recipient to whitelist you")
                elif (error_code == 550): print("Though it can be returned also by the recipient's firewall (or when the incoming server is down), the great majority of errors 550 simply tell that the recipient email address doesn't exist. You should contact the recipient otherwise and get the right address.")
                elif (error_code == 553): print("Check all the addresses. There should be an error or a misspelling somewhere.")
                else: print(error_code + ": " + error_message)
            except smtplib.SMTPAuthenticationError: print("ERROR: SMTP authentication went wrong. The server didn't accept the username/password")
        except: print("error #1")

if __name__ == "__main__":
    main()
