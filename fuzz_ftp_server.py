# Simple boofuzz script to fuzz a FTP server and FTP protocol implementation
# Designed for use with boofuzz v0.0.11
#!/usr/bin/env python

from boofuzz import *

def main():
    # 1. Create a session, which contains a target, which in turn contains a connection
    session = Session(
        target = Target(
            connection = SocketConnection("192.168.0.14", 8021, proto='tcp')))

    # 2. Define FTP protocol messages
    # FTP user login message
    s_initialize("user")
    s_string("USER")
    s_delim(" ")
    s_string("anonymous")
    s_static("\r\n")

    # FTP password message
    s_initialize("pass")
    s_string("PASS")
    s_delim(" ")
    s_string("james")
    s_static("\r\n")

    # FTP store message
    s_initialize("stor")
    s_string("STOR")
    s_delim(" ")
    s_string("AAAA")
    s_static("\r\n")

    # FTP retrieve message
    s_initialize("retr")
    s_string("RETR")
    s_delim(" ")
    s_string("AAAA")
    s_static("\r\n")

    # 3. Sequence the messages
    session.connect(s_get("user"))
    session.connect(s_get("user"), s_get("pass"))
    session.connect(s_get("pass"), s_get("stor"))
    session.connect(s_get("pass"), s_get("retr"))

    # 4. Fuzz the FTP protocol implementation
    session.fuzz()

if __name__ == '__main__':
    main()
