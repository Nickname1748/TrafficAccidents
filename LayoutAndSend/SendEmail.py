import smtplib

PASSWORD = ''

def send(msg):
    credfile = open('credentials.txt', 'r')
    credentials = [line.rstrip('\n') for line in credfile]
    sendfile = open('sendlist.txt', 'r')
    sendlist = [line.rstrip('\n') for line in sendfile]
    msg['From'] = credentials[0]
    msg['To'] = ''
    fromaddr = credentials[0]
    toaddr = ''
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login(credentials[0], credentials[1])
    for dest in sendlist:
        msg['To'] = dest
        toaddr = dest
        msg_full = msg.as_string()
        server.sendmail(fromaddr, toaddr, msg_full)
    server.quit()