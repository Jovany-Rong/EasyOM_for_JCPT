#!/usr/local/bin python
#coding: utf-8

import paramiko

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

class SSHConnection(object):
    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def execute(self, command):
        ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh._transport = self.__transport

        stdin, stdout, stderr = ssh.exec_command(command)

        res = to_str(stdout.read())
        error = to_str(stderr.read())

        if error.strip():
            return {'status' : 'fail', 'result' : error}
        else:
            return {'status' : 'success', 'result' : res}

    def upload(self, local_path, target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)

        sftp.put(local_path, target_path, confirm=True)
        sftp.chmod(target_path, 0o755)

    def download(self, target_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)

        sftp.get(target_path, local_path)

    def __del__(self):
        try:
            self.close()
        except:
            pass