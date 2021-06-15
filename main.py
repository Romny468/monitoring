try:
    import os
    import platform
    import yaml
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime
except:
    print("error while loading modules! \n exiting!")

def config_check():
    if not os.path.exists('config.yml'):
        new_file = {'addresses': ['google.com', '127.0.0.1', 'nu.nl', 'spele.nl']},
        with open('config.yml', 'w') as file:
            yaml.dump(new_file, file)

def yaml_loader(filepath):
    with open(filepath) as yml_data:
        data = yaml.safe_load(yml_data)
    return data

def main():
    config_check()
    data = yaml_loader("config.yml")
    not_responsive = []

    # check on which os is running and adapt to os
    if platform.system() == "Windows":
        param = "-n"
    else:
        param = "-c"

    # ping check all hosts in config file
    for ip in data["addresses"]:
        response = os.system("ping " + param + " 1 " + ip)
        if response == 0:
            print("Ping to:", ip, "was successful")
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
            # print("\n\nsender:", sender, "\npassword:", password, "\nsmtp:", smtp,"\nport", port,"\nreceivers:", receivers)
            msg = MIMEMultipart('alternative')
            html = f"""
            <html>
                <header style="background-color:  #f9a41a; padding: 15px; width: auto;">
                        <h1 style="text-align: center; color: ##000000; ">Server monitoring</h1>
                </header>
                <body>
                    <div style="font-size: 20px; width: auto;">
                        <p>Offline servers:</p>
                        <ul>
                        """
            for x in not_responsive:
                html += f"""
                            <li>{x}</li>
                        """
            html += """
                                            </ul>
                                        </div>
                                    </body>
                                    <footer style="background-color: #5EFF3356388; padding: 15px; width: auto;">
                                    </footer>
                                </html>"""

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
            except smtplib.SMTPResponseException:
                print("ERROR: an email has been tried to be send but the SMTP server returned an error code")
                return False
            except smtplib.SMTPAuthenticationError:
                print("ERROR: SMTP authentication went wrong. The server didn't accept the username/password")
                return False

        except: print("error #1")
        # except FileNotFoundError as ex:
        #     print(ex)

main()
