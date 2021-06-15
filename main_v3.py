try:
    import os, platform, yaml, smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime
except:
    print("error while loading modules! \n exiting!")
    exit()

def config_check():
    if not os.path.exists('config.yml'):
        new_file = {'addresses': ['google.com', '127.0.0.1', 'nu.nl', 'spele.nl']},
        with open('config.yml', 'w') as file: yaml.dump(new_file, file)

def yaml_loader(filepath):
    with open(filepath) as yml_data:
        data = yaml.safe_load(yml_data)
        return data

def main():
    config_check()
    data = yaml_loader("config.yml")
    not_responsive = []

    # check on which os is running and adapt to os
    if platform.system() == "Windows": param = "-n"
    else: param = "-c"

    # ping check all hosts in config file
    for ip in data["addresses"]:
        response = os.system("ping " + param + " 1 " + ip)
        if response == 0: print("Ping to:", ip, "was successful")
        else:
            print("Ping to:", ip, "was unsuccessful")
            not_responsive.append(ip)
            send_mail(ip, not_responsive)

def send_mail(ip, not_responsive):
    with open("settings.yml") as yml_data:
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
            <div><footer style="background-color: #5eff3356388; padding: 15px; width: auto;">This is an automatically generated email. Please do not reply to it. <br />If you have any questions please send an email to: <em>email</em></footer></div>
            """
            mailtext = MIMEText(html, 'html')

            msg['Subject'] = f"Monitor warning on {ip}"
            msg['From'] = sender
            msg['To'] = 'monitor@fontys.nl'
            msg.attach(mailtext)

            try:
                smtp_server = smtplib.SMTP_SSL(smtp, port)
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, receivers, msg.as_string())
                print("email has been send")
                smtp_server.close()
                return True
            except smtplib.SMTPConnectError:
                print("ERROR: connecting during the connection with the SMTP server")
                return False
            except smtplib.SMTPServerDisconnected:
                print("ERROR: an email has been tried to be send but the SMTP sever disconnected")
                return False
            except smtplib.SMTPRecipientsRefused:
                print("ERROR: cannot send an email, recipient refused. Make sure receiver setting is not empty!")
                return False
            except smtplib.SMTPSenderRefused:
                print("ERROR: The senders address refused")
                return False
            except smtplib.SMTPResponseException as e:
                print("ERROR: an email has been tried to be send but the SMTP server returned an error code")
                error_code = e.smtp_code
                error_message = e.smtp_error
                # print("Error code:", error_code)
                # print("Message:", error_message)
                if (error_code == 422):
                    print("Recipient Mailbox Full")
                elif (error_code == 431):
                    print("Server out of space")
                elif (error_code == 447):
                    print("Timeout. Try reducing number of recipients")
                elif (error_code == 510 or error_code == 511):
                    print("One of the addresses doesn't exist. Check again your recipients accounts and correct any possible misspelling.")
                elif (error_code == 512):
                    print("Check all your recipients addresses: there will likely be an error in a domain name.")
                elif (error_code == 541 or error_code == 554):
                    print("Your message has been detected and labeled as spam. You must ask the recipient to whitelist you")
                elif (error_code == 550):
                    print("Though it can be returned also by the recipient's firewall (or when the incoming server is down), the great majority of errors 550 simply tell that the recipient email address doesn't exist. You should contact the recipient otherwise and get the right address.")
                elif (error_code == 553):
                    print("Check all the addresses. There should be an error or a misspelling somewhere.")
                else:
                    print(error_code + ": " + error_message)
                    return False
            except smtplib.SMTPAuthenticationError:
                print("ERROR: SMTP authentication went wrong. The server didn't accept the username/password")
                return False

        except: print("error #1")

if __name__ == "__main__":
    main()
