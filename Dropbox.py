import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json


import helper

app_key = 'cm1i0uvz8e0tg20'
app_secret = '6l44a1v1qc4krif'
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # 8090. portuan entzuten dagoen zerbitzaria sortu
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # nabitzailetik 302 eskaera jaso
        client_connection, client_address = server_socket.accept()
        eskaera = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print eskaera

        # eskaeran "auth_code"-a bilatu
        lehenengo_lerroa = eskaera.split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print "\tauth_code: " + auth_code

        # erabiltzaileari erantzun bat bueltatu
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response)
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        #############################################
        # RELLENAR CON CODIGO DE LAS PETICIONES HTTP
        # Y PROCESAMIENTO DE LAS RESPUESTAS HTTP
        # PARA LA OBTENCION DEL ACCESS TOKEN
        print("Autentikazio eta autorizazioa lortu")
        print("   1. pausua - /oauth/authorize")
        # URL Structure   https://www.dropbox.com/oauth2/authorize
        # Method  GET
        # Parameters: response_type, client_id,  redirect_uri
        uri= "https://www.dropbox.com/oauth2/authorize"
        parameters={'response_type': 'code', 'client_id': app_key, 'redirect_uri': redirect_uri}

        params_encoded=urllib.urlencode(parameters)   #parametroak kodifikatuko ditugu
        webbrowser.open(uri + '?' + params_encoded)   #nabigatzailea ireki

        auth_code = self.local_server()
        print ("auth_code: " + auth_code)

        # access token lortu
        print("   2. pausua - /oauth2/token")
        #URL Structure https://api.dropboxapi.com/oauth2/token
        #Method POST
        #Parameters: code, grant_type, client_id, client_secret, redirect_uri
        uri = "https://api.dropboxapi.com/oauth2/token"
        goiburuak = {'Host': 'api.dropboxapi.com', 'Content-Type': 'application/x-www-form-urlencoded'}
        datuak = {'code':auth_code, 'grant_type': 'authorization_code', 'client_id':app_key, 'client_secret': app_secret, 'redirect_uri':redirect_uri,}

        erantzuna = requests.post(uri, headers=goiburuak, data=datuak, allow_redirects=False)
        status = erantzuna.status_code
        print("Status: " + str(status))
        edukia = erantzuna.text
        print("Edukia: " + edukia)
        edukia_json = json.loads(edukia)   #json-era pasatu
        access_token = edukia_json['access_token']   #access_token lortu

        self._access_token= access_token   #gorde access_token
        #############################################

        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        # metodoa: post
            # uri: https://api.dropboxapi.com/2/files/list_folder
            # headers: Authorization, Content-Type
            # data: beharrezkoa den bakarra: path

        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        if self._path=='/':   #/ jartzen badu, hasierako menuan gaudela esan nahi du. Baina, dropbox api-a deitzerakoan, hasierako menuan daudenak, ez dute / aurretik izango. Beraz, kasu honetan aurkitzen bagara, barra kendu beharko diogu
            path=""
        else:
            path=self._path

        datuak = {'path': path}   #datuak. beharrezkoa den bakarra path da
        datuak_encoded = json.dumps(datuak)    #encode json. Json object bat hartzen du eta string bihurtzen du

        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token, 'Content-Type': 'application/json', }
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_encoded, allow_redirects=False)   #eskaera

        status = erantzuna.status_code   #eskaeraren status lortu
        print("\tStatus: " + str(status))
        edukia = erantzuna.text   #erantzunaren edukia lortu
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)   #edukia json-era pasatu

        #############################################

        self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_dict)

    def transfer_file(self, file_path, file_data):   #esto de pasar aqui el cookie queda muy feo, ns
        #file_path = WS_2020-04-06_Praktika3_eXist-db_gida.pdf
        #file_data = fitxategiaren eduki osoa izango da. Bestela egelatik jaitsi behar denez, autentifikazioa behar duelako. beraz hori egela klasean egingo dugu

        print("/upload " + file_path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        # metodoa: post
            # uri: https://content.dropboxapi.com/2/files/upload
            # headers: Authorization, Dropbox-API-Arg, Content-Type
                # Dropbox-API-Arg: path, mode, autorename, mute, strict_conflict
            # data: igotzeko fitxategiaren edukia

        uri='https://content.dropboxapi.com/2/files/upload'

        dropbox_api_arg = {'path': file_path, 'mode': 'add', 'autorename': True, 'mute': False, 'strict_conflict': False,}
        dropbox_api_arg_json = json.dumps(dropbox_api_arg)

        goiburuak = {'Host': 'content.dropboxapi.com', 'Authorization': 'Bearer '+ self._access_token, 'Dropbox-API-Arg': dropbox_api_arg_json, 'Content-Type': 'application/octet-stream'}
        erantzuna = requests.post(uri, headers=goiburuak, data=file_data, allow_redirects=False)

        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

        #############################################

    def delete_file(self, file_path):
        print("/delete_file " + file_path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        datuak = {'path': file_path}
        datuak_encoded = json.dumps(datuak)

        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_encoded, allow_redirects=False)
        status = erantzuna.status_code

        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        #############################################

    def create_folder(self, path):
        print("/create_folder " + path)
        # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        uri = 'https://api.dropboxapi.com/2/files/create_folder_v2'

        datuak = {'path': path, "autorename": True}
        datuak_encoded = json.dumps(datuak)

        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_encoded, allow_redirects=False)

        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)



        #############################################

    def copy(self, file_path):
        print("/copy " + file_path)
        uri = 'https://api.dropboxapi.com/2/files/copy_v2'

        data = {'from_path': file_path, 'to_path': file_path, 'autorename': True, }
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)

        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def rename(self, from_path, to_path):
        print("/rename "+from_path + " to "+ to_path)
        uri='https://api.dropboxapi.com/2/files/move_v2'

        #lortu behar dugu from_path-ren extensioa eta to_path-ri gehitu
        split=from_path.split(".")
        extension = split[len(split)-1]
        print(extension)
        to_path=to_path +"."+extension

        data = {'from_path': from_path, 'to_path': to_path, 'autorename': True,}
        data_json=json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer '+ self._access_token, 'Content-Type': 'application/json',}

        erantzuna= requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)

        status=erantzuna.status_code
        print("\tStatus: "+ str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def share_to_email(self, file_path, email_to_share):

        # mmetadata para coger el id

        #file = '/SW_2020-02-21_M_WebScraping.pdf'
        print("/get_metadata ")
        uri = 'https://api.dropboxapi.com/2/files/get_metadata'

        data = {'path': file_path}
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        print("\tfitxategiaren id-a: " + edukia_json_dict['id'])

        tag = edukia_json_dict['.tag']
        if (tag == 'file'):  # file bat da

            # add_file_member
            id = edukia_json_dict['id']
            print("/add_file_member ")
            uri = 'https://api.dropboxapi.com/2/sharing/add_file_member'

            members = []  # llenar esto dentro con un hitegi.
            user = {'.tag': 'email', 'email': email_to_share}
            members.append(user)

            data = {'file': id, 'members': members, 'quiet': False, 'access_level': 'viewer',
                    'add_message_as_comment': False}
        else:  #folder bat da
            # lehenengo lortu beharko dugu karpetaren shared_folder_id

            if "shared" in edukia:  # jada konpartitzeko id bat du karpeta
                shared_folder_id = edukia_json_dict['shared_folder_id']
            else:  # karpeta ez du konpartitzeko id-rik beraz id bat esleituko diogu
                shared_folder_id = self.get_share_folder_id(file_path)

            print("shared_folder_id:" + shared_folder_id)

            # add_folder_member
            print("/add_folder_member ")
            uri = 'https://api.dropboxapi.com/2/sharing/add_folder_member'

            members = []  # llenar esto dentro con un hitegi.
            u = {'.tag': 'email', 'email': email_to_share}
            user = {'member': u, 'access_level': 'editor', }
            members.append(user)

            data = {'shared_folder_id': shared_folder_id, 'members': members, 'quiet': False, }

        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def move(self, from_path, to_path):
        #file_path = '/Get Started with Dropbox (1).pdf'
        #to_path = '/prueba/Get Started with Dropbox (1).pdf'
        print("/move " + from_path + " to " + to_path)
        uri = 'https://api.dropboxapi.com/2/files/move_v2'

        data = {'from_path': from_path, 'to_path': to_path, 'autorename': True, }
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def search(self, msg_listbox, word):
        print("Search")
        if(word==''):
            self.list_folder(msg_listbox)
        else:
            uri = 'https://api.dropboxapi.com/2/files/search_v2'

            data = {'query': word, 'include_highlights': False, }
            data_json = json.dumps(data)
            goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                         'Content-Type': 'application/json', }

            erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
            status = erantzuna.status_code
            print("\tStatus: " + str(status))
            edukia = erantzuna.text
            print("\tEdukia: " + edukia)
            edukia_json_dict = json.loads(edukia)

            #############################################

            self._files = helper.update_search_listbox2(msg_listbox, self._path, edukia_json_dict)

    def download(self, origin_path, download_path):

        # download

        # lortu behar dugu from_path-ren extensioa eta to_path-ri gehitu
        split = origin_path.split(".")
        extension = split[len(split) - 1]
        print(extension)
        download_path = download_path + "." + extension

        #file_path = '/Get Started with Dropbox (1).pdf'
        #to_path = 'C:\Users\nerea\Desktop\Get Started with Dropbox.pdf'
        print("/download " + origin_path + " to "+download_path)
        uri = 'https://content.dropboxapi.com/2/files/download'
        # uri='https://content.dropboxapi.com/2/files/download_zip'

        dropbox_api_arg = {'path': origin_path, }
        dropbox_api_arg_json = json.dumps(dropbox_api_arg)

        goiburuak = {'Host': 'content.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Dropbox-API-Arg': dropbox_api_arg_json, }
        erantzuna = requests.post(uri, headers=goiburuak, allow_redirects=False)

        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text

        # hasta ahi tengo el eduki. ahora pongo lo mismo q las fotos pa descargar al ordenador
        f = open(download_path, "wb")
        f.write(erantzuna.content)
        f.flush()
        f.close()

    def get_share_folder_id(self, file_path):
        # /share_folder
        path = file_path
        print("/share_folder " + path)
        uri = 'https://api.dropboxapi.com/2/sharing/share_folder'

        data = {'path': path, "force_async": False, "access_inheritance": "inherit"}
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        emaitza=''
        if "already_shared" not in edukia_json_dict:
            emaitza= edukia_json_dict['shared_folder_id']
        return emaitza

    def list_members(self, file_path):

        # /list_file_members
        # metadata para coger el id
        print("/get_metadata ")
        uri = 'https://api.dropboxapi.com/2/files/get_metadata'
        data = {'path': file_path, }
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)

        tag=edukia_json_dict['.tag']
        if(tag=='file'):   #file bat da
            print("\tfitxategiaren id-a: " + edukia_json_dict['id'])
            # ahora si
            file = edukia_json_dict['id']
            print("/link user " + file)
            uri = 'https://api.dropboxapi.com/2/sharing/list_file_members'

            data = {"file": file, "include_inherited": True, "limit": 100}
            data_json = json.dumps(data)
            goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                         'Content-Type': 'application/json', }

            erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
            status = erantzuna.status_code
            print("\tStatus: " + str(status))
            edukia = erantzuna.text
            print("\tEdukia: " + edukia)
            edukia_json_dictSHARE = json.loads(edukia)
        else: #folder bat da
            # lehenengo lortu beharko dugu karpetaren shared_folder_id

            if "shared" in edukia:  #jada konpartitzeko id bat du karpeta
                shared_folder_id =edukia_json_dict['shared_folder_id']
            else: #karpeta ez du konpartitzeko id-rik beraz id bat esleituko diogu
                shared_folder_id= self.get_share_folder_id(file_path)

            print("shared_folder_id:" +shared_folder_id)

            # ahora bai. lista aterako dugu
            print("/list folder user " + file_path)
            uri = 'https://api.dropboxapi.com/2/sharing/list_folder_members'

            data = {"shared_folder_id": shared_folder_id, "actions": [], "limit": 10}
            data_json = json.dumps(data)
            goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                         'Content-Type': 'application/json', }

            erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
            status = erantzuna.status_code
            print("\tStatus: " + str(status))
            edukia = erantzuna.text
            print("\tEdukia: " + edukia)
            edukia_json_dictSHARE = json.loads(edukia)

        # emaitza
        generalText = ''
        arrayMembers=[]

        u = edukia_json_dictSHARE['users']
        if len(u) != 0:
            generalText = generalText + "\n- Users:"
        for uBat in u:
            uu = uBat['user']
            generalText = generalText + "\n\tName: " + uu['display_name'] + ", Email: " + uu['email']
            arrayMembers.append(uu['email'])
        # ---------
        g = edukia_json_dictSHARE['groups']
        if len(g) != 0:
            generalText = generalText + "\n- Groups:"
        for gBat in g:
            generalText = generalText + "\n\tGroup name" + gBat['group']['group_name']
        # ---------
        i = edukia_json_dictSHARE['invitees']
        if len(i) != 0:
            generalText = generalText + "\n- Invitees:"
        for iBat in i:
            generalText = generalText + "\n\tEmail: " + iBat['invitee']['email']
            arrayMembers.append(iBat['invitee']['email'])

        print(generalText)
        return generalText, arrayMembers

    def create_file(self, path, file_data):
        #path = '/pruebitaaaaa3.pdf'
        #file_data = "jajajaja no se que poner"
        path=path
        print("/alpha/upload " + path)
        uri = 'https://content.dropboxapi.com/2/files/alpha/upload'

        dropbox_api_arg = {'path': path, "mode": "add", "autorename": True, "mute": False, "strict_conflict": False}
        dropbox_api_arg_json = json.dumps(dropbox_api_arg)

        goiburuak = {'Host': 'content.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/octet-stream', 'Dropbox-API-Arg': dropbox_api_arg_json}
        erantzuna = requests.post(uri, headers=goiburuak, data=file_data, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def revoke_file_member(self, file_path, email):

        print("/get_metadata ")
        uri = 'https://api.dropboxapi.com/2/files/get_metadata'
        data = {'path': file_path}
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        print("\tfitxategiaren id-a: " + edukia_json_dict['id'])

        tag = edukia_json_dict['.tag']
        if (tag == 'file'):  # file bat da
            #revoke_file_member
            id = edukia_json_dict['id']
            print("/revoke_file_member ")
            uri = 'https://api.dropboxapi.com/2/sharing/remove_file_member_2'
            member = {'.tag': 'email', 'email': email}
            data = {'file': id, 'member': member, }

        else:  # folder bat da
            # lehenengo lortu beharko dugu karpetaren shared_folder_id

            if "shared" in edukia:  # jada konpartitzeko id bat du karpeta
                shared_folder_id = edukia_json_dict['shared_folder_id']
            else:  # karpeta ez du konpartitzeko id-rik beraz id bat esleituko diogu
                shared_folder_id = self.get_share_folder_id(file_path)

            print("shared_folder_id:" + shared_folder_id)
            # revoke_folder_member
            print("/revoke_folder_member ")
            uri = 'https://api.dropboxapi.com/2/sharing/remove_folder_member'
            member = {'.tag': 'email', 'email': email}
            data = {'shared_folder_id': shared_folder_id, 'member': member, 'leave_a_copy': False }

        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def revoke_all(self, file_path):

        print("/get_metadata ")
        uri = 'https://api.dropboxapi.com/2/files/get_metadata'
        data = {'path': file_path}
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        print("\tfitxategiaren id-a: " + edukia_json_dict['id'])

        tag = edukia_json_dict['.tag']
        if (tag == 'file'):  # file bat da
            #unshare_file
            id = edukia_json_dict['id']
            print("/unshare_file ")
            uri = 'https://api.dropboxapi.com/2/sharing/unshare_file'
            data = {'file': id,}

        else:  # folder bat da
            # lehenengo lortu beharko dugu karpetaren shared_folder_id

            if "shared" in edukia:  # jada konpartitzeko id bat du karpeta
                shared_folder_id = edukia_json_dict['shared_folder_id']
            else:  # karpeta ez du konpartitzeko id-rik beraz id bat esleituko diogu
                shared_folder_id = self.get_share_folder_id(file_path)

            print("shared_folder_id:" + shared_folder_id)
            # unshare_folder
            print("/unshare_folder ")
            uri = 'https://api.dropboxapi.com/2/sharing/unshare_folder'
            data = {'shared_folder_id': shared_folder_id, 'leave_a_copy': False }

        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)

    def create_share_link(self, path):
        # Deituko dugu soilik jakinda ez duela shared link
        uri = 'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings'

        settings = {"requested_visibility": "public", "audience": "public", "access": "viewer"}
        data = {'path': path, 'settings': settings, }
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        link = edukia_json_dict['url']

        print("\turl-a " + link)
        return link

    def list_shared_link(self, path):
        # list_shared_links
        print("list_shared_links ")
        uri = 'https://api.dropboxapi.com/2/sharing/list_shared_links'
        data = {'path': path, }
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)
        l = edukia_json_dict['links']
        if l == []:  # ez du konpartitzeko linka sortuta. Beraz sortuko dugu
            return False
        else:
            lehena = l[0]
            link = lehena['url']
            return link

    def revoke_shared_link(self,url):
        print("/revoke_shared_link")
        uri = 'https://api.dropboxapi.com/2/sharing/revoke_shared_link'
        data = {'url': url}
        data_json = json.dumps(data)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json', }

        erantzuna = requests.post(uri, headers=goiburuak, data=data_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)


    def user_info(self):
        print("/get_current_account")
        uri = 'https://api.dropboxapi.com/2/users/get_current_account'
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token, }

        erantzuna = requests.post(uri, headers=goiburuak, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia: " + edukia)
        edukia_json_dict = json.loads(edukia)

        emaitza = ''
        name = edukia_json_dict['name']
        root = edukia_json_dict['root_info']
        ac = edukia_json_dict['account_type']
        emaitza = emaitza + "Account_id: " + edukia_json_dict['account_id'] + "\nName: " + "\n\tGiven_name: " + name[
            'given_name'] + "\n\tSurname: " + name['surname'] + "\n\tFamiliar_name: " + name[
                      'familiar_name'] + "\n\tDisplay_name: " + name['display_name'] + "\n\tAbbreviated_name: " + name[
                      'abbreviated_name'] + "\nEmail: " + edukia_json_dict['email'] + "\nEmail verified: " + str(
            edukia_json_dict['email_verified']) + "\nDisabled: " + str(edukia_json_dict['disabled']) + "\nLocale: " + \
                  edukia_json_dict['locale'] + "\nReferral link: " + edukia_json_dict[
                      'referral_link'] + "\nIs paired: " + str(edukia_json_dict['is_paired']) + "\nAccount type: " + ac[
                      '.tag'] + "\nRoot info: " + "\n\tTag: " + root['.tag'] + "\n\tRoot namespace id: " + root[
                      'root_namespace_id'] + "\n\tHome namespace id: " + root['home_namespace_id']
        # extrak:
        if 'profile_photo_url' in edukia:
            emaitza = emaitza + "\nProfile photo url: " + edukia_json_dict['profile_photo_url']
        if 'country' in edukia:
            emaitza = emaitza + "\nCountry: " + edukia_json_dict['country']
        if 'team' in edukia:
            team = edukia_json_dict['team']
            edukia = edukia + "\nTeam: \n\tId: " + team['id'] + "\n\tName: " + team['name'] + "\n\tSharing policies" + \
                     team['sharing_policies'] + "\n\tOffice addin policy" + team['oddice_addin_policy']
        if 'team_member_id' in edukia:
            emaitza = emaitza + "\nTeam member id: " + edukia_json_dict['team_member_id']

        print emaitza
        return emaitza