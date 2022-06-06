import socket
import json
import base64
import logging
import os, os.path

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    if (os.path.exists(filename) == False):
        print("File tidak ditemukan")
        return False
    if (filename != ''):
        try:  
            # proses membaca file yang akan diupload; rb - read binary
            fp = open(f"{filename}",'rb') 
            # proses encoding file untuk diupload
            content = base64.b64encode(fp.read()).decode()

            command_str = f"UPDATE {filename} {content}"
            hasil = send_command(command_str)
            print(hasil)

            if(hasil['status'] == 'OK'):
                print(f'Mengupdate {filename} berhasil !')
                return True
            else:
                print(f'Mengupdate {filename} gagal !')
                return False
        except Exception as e:
            print(e)
            return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"Menghapus {filename} berhasil !")
        return True
    else:
        print(f"Menghapus {filename} gagal!")
        return False
        
if __name__=='__main__':
    server_address=('172.16.16.101',6666)
    remote_list()
    remote_get('rfc2616.pdf')
    # remote_update('daring.jpg')
    # remote_delete('donalbebek2.jpg')

