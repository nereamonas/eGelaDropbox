import json
import re
import tkMessageBox
import requests
import urllib
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookiea = ""
    _refs = []
    _root = None
    _ikasgaiaren_url = ""

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####")
        metodo = 'POST'
        uri = "https://egela.ehu.eus/login/index.php"
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        goiburuak = {'Host': 'egela.ehu.eus',
                     'Content-Type': 'application/x-www-form-urlencoded'}

        # datuak inprimaki formatuan bidaltzen direnean, lehenik datuak hiztegi batean sartzen dira eta ondoren hiztegi hori inprimaki fromatu kate bihurtzen da
        edukia = {'username':username, 'password':password}

        print(str(username),str(password))

        # Hiztegitik --> String katera pasatu eta luzera lortu
        edukia_encoded = urllib.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        # Eskaera egin eta erantzuna gorde
        erantzuna = requests.request(metodo, uri, headers=goiburuak, data=edukia_encoded, allow_redirects=False)

        # Erantzunaren balioak gorde
        erantzunKodea = erantzuna.status_code
        erantzunDeskribapena = erantzuna.reason

        # eskaeraren informazioa inprimatu
        print ('\033[1m' + "1.ESKAERAREN INFORMAZIOA" + '\033[0m')
        print ("\t Metodoa: " + metodo + " Uria: " + uri)
        print ("\t Goiburuak: ")
        for goiburua in goiburuak:
            print("\t\t" + goiburua + ':' + goiburuak[goiburua])
        print ("\t Edukia: " + urllib.urlencode(edukia))
        # erantzunaren informazioa inprimatu
        print
        print ('\033[1m' + "1.ERANTZUNAREN INFORMAZIOA" + '\033[0m')
        print ('\t' + 'Status: ' + str(erantzunKodea) + ' Deskribapena: ' + erantzunDeskribapena)
        print ("\tGoiburuak: \t")
        for goiburua in erantzuna.headers:
            print("\t\t" + goiburua + ':' + erantzuna.headers[goiburua])
        print("--------------------------------------------------------------------------------------------------")

        # MoodleSessionegela eta location lortu behar ditugu. Hurrengo eskaera egiteko
        cookia = erantzuna.headers['Set-Cookie'].split(';')[0]
        location = erantzuna.headers['Location']





        #######################################################################################################################################

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        metodo = 'GET'
        uri = location
        goiburuak = {'Host':'egela.ehu.eus', 'Cookie':cookia}

        # Eskaera egin eta erantzuna gorde
        erantzuna = requests.request(metodo, uri, headers=goiburuak, allow_redirects=False)

        # Erantzunaren balioak gorde
        erantzunKodea = erantzuna.status_code
        erantzunDeskribapena = erantzuna.reason

        # eskaeraren informazioa inprimatu
        print ('\033[1m' + "2.ESKAERAREN INFORMAZIOA" + '\033[0m')
        print ("\t Metodoa: " + metodo + " Uria: " + uri)
        print ("\t Goiburuak: ")
        for goiburua in goiburuak:
            print("\t\t" + goiburua + ':' + goiburuak[goiburua])
        print
        # erantzunaren informazioa inprimatu
        print ('\033[1m' + "2.ERANTZUNAREN INFORMAZIOA" + '\033[0m')
        print ('\t' + 'Status: ' + str(erantzunKodea) + ' Deskribapena: ' + erantzunDeskribapena)
        print ("\tGoiburuak: \t")
        for goiburua in erantzuna.headers:
            print("\t\t" + goiburua + ':' + erantzuna.headers[goiburua])

        print("--------------------------------------------------------------------------------------------------")

        if erantzunKodea == 303:
            # location lortu behar dugu. Hurrengo eskaera egiteko
            location = erantzuna.headers['Location']





            #######################################################################################################################################

            progress = 66
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)

            print("\n##### 3. ESKAERA #####")
            #############################################
            # RELLENAR CON CODIGO DE LA PETICION HTTP
            # Y PROCESAMIENTO DE LA RESPUESTA HTTP

            metodo = 'GET'
            uri = location
            goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': cookia}

            # Eskaera egin eta erantzuna gorde
            erantzuna = requests.request(metodo, uri, headers=goiburuak, allow_redirects=False)

            # Erantzunaren balioak gorde
            erantzunKodea = erantzuna.status_code
            erantzunDeskribapena = erantzuna.reason

            # eskaeraren informazioa inprimatu
            print ('\033[1m' + "3.ESKAERAREN INFORMAZIOA" + '\033[0m')
            print ("\t Metodoa: " + metodo + " Uria: " + uri)
            print ("\t Goiburuak: ")
            for goiburua in goiburuak:
                print("\t\t" + goiburua + ':' + goiburuak[goiburua])
            print
            # erantzunaren informazioa inprimatu
            print ('\033[1m' + "3.ERANTZUNAREN INFORMAZIOA" + '\033[0m')
            print ('\t' + 'Status: ' + str(erantzunKodea) + ' Deskribapena: ' + erantzunDeskribapena)
            print ("\tGoiburuak: \t")
            for goiburua in erantzuna.headers:
                print("\t\t" + goiburua + ':' + erantzuna.headers[goiburua])

            print

            #######################################################################################################################################

            progress = 100
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)
            popup.destroy()

            if erantzunKodea==200:
                #############################################
                # ACTUALIZAR VARIABLES
                self._login = 1
                self._cookiea = cookia

                # hurrengo eskaera egiteko, Web sistemak ikasgaiaren pdf guztiak deskargatzeko, Web sistemak ikasgaiaren url-a lortu beharko dugu:
                html = erantzuna.content
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a', {'class': 'ehu-visible'}, href=re.compile(r'(course)'))
                for el in links:
                    s = str(el)  # string-era bihurtuko dugu
                    ikasgaia = s.split('>')[1].split('<')[0]  # ikasgaiaren izena bilatuko dugu
                    if (ikasgaia == 'Web Sistemak'):  # ikasgaia web sistemak bada:
                        self._ikasgaiaren_url = el['href']  # bere url-arekin geratuko gara
                #############################################
                self._root.destroy()
            else:
                tkMessageBox.showinfo("Alert Message", "Login incorrect!")
        else:
            tkMessageBox.showinfo("Alert Message", "Login incorrect!")



    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        metodo = 'GET'
        uri = self._ikasgaiaren_url
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}

        # Eskaera egin eta erantzuna gorde
        erantzuna = requests.request(metodo, uri, headers=goiburuak, allow_redirects=False)

        # Erantzunaren balioak gorde
        erantzunKodea = erantzuna.status_code
        erantzunDeskribapena = erantzuna.reason
        html = erantzuna.content

        # eskaeraren informazioa inprimatu
        print ('\033[1m' + "4.ESKAERAREN INFORMAZIOA" + '\033[0m')
        print ("\t Metodoa: " + metodo + " Uria: " + uri)
        print ("\t Goiburuak: ")
        for goiburua in goiburuak:
            print("\t\t" + goiburua + ':' + goiburuak[goiburua])
        # erantzunaren informazioa inprimatu
        print
        print ('\033[1m' + "4.ERANTZUNAREN INFORMAZIOA" + '\033[0m')
        print ('\t' + 'Status: ' + str(erantzunKodea) + ' Deskribapena: ' + erantzunDeskribapena)
        print ("\tGoiburuak: \t")
        for goiburua in erantzuna.headers:
            print("\t\t" + goiburua + ':' + erantzuna.headers[goiburua])

        #############################################



        print("\n##### HTML-aren azterketa... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs

        # todas las paginas: section=1,section=2
        soup = BeautifulSoup(html, 'html.parser')
        links_section = soup.find_all('a', {'class': 'list-group-item list-group-item-action'},href=re.compile(r'(section)'))

        # ikasgai honetan atal desberdinak ditugu (section): 1:Eskola magistralak eta gelako praktikak eta 2: Laborategiko praktikak.
        # beraz lehenengo 1.ataleko pdf-ak gordeko ditugu eta ondoren 2.atalekoak
        a = ''
        for section in links_section:
            if not (section['href'].endswith('0')):
                section_uri = section['href'] # section-aren url-a
                print(section_uri)
                erantzuna = requests.request(metodo, section_uri, headers=goiburuak, allow_redirects=False)
                soup = BeautifulSoup(erantzuna.content, 'html.parser')
                links = soup.find_all('a', {'class': ''}, href=re.compile(r'(resource)'))  # a, bere klasea hutsa '' eta href-ean resource hitza dutenak

                url_list = []  #url guztiak lortuko ditugu
                for el in links:
                    if (el['href'].startswith('https')):
                        name = str(el).split('span')[1].split('>')[1].split('<')[0]
                        urlBat={'name': name, 'url': el['href'] }
                        url_list.append(urlBat)

                progress_step = float(100.0 / len(url_list))

                for urlBat in url_list:
                    # orain url horren eskaera egingo dugu pdf-aren helbidea lortzeko
                    metodo = 'GET'
                    uria = urlBat['url']
                    goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
                    erantzuna = requests.request(metodo, uria, headers=goiburuak, allow_redirects=False)
                    html = erantzuna.content

                    soup = BeautifulSoup(html, 'html.parser')
                    links = soup.find_all('a', href=re.compile(r'(.pdf)'))  # bilatuko ditu 'a' klaseko eta .pdf formatua duten linkak eta array batean gordeko ditu.
                    for el in links:
                        if (el['href'].startswith('http')):  # pdf-en http-a
                            url = el['href']  # url-a lortuko dugu. href-ri erreferentzia egiten dio
                            name=urlBat['name']
                            if name not in a:  #planifikazioa eta sekzio guztietan agertzen dira. Beraz honela soilik behin hartuko du
                                pdf_name = json.loads('"' + name + '"')   #decode json. String bat hartzen du eta json object bihurtzen du
                                pdf_link = json.loads('"' + url + '"')   #decode json. String bat hartzen du eta json object bihurtzen du
                                pdfBat = {'pdf_name': pdf_name, 'pdf_link': pdf_link}
                                a=a+' '+name
                                print(pdfBat)
                                self._refs.append(pdfBat)   #zerrendara gehitu


            #############################################

                            # ACTUALIZAR BARRA DE PROGRESO
                            # POR CADA PDF ANIADIDO EN self._refs
                            progress += progress_step
                            progress_var.set(progress)
                            progress_bar.update()
                            time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP

        bat = self._refs[selection]

        pdf_nameIkusi=bat['pdf_name']    #ikusten dugun izena
        pdf_url = bat['pdf_link']   #url-a

        # pdf_url = https://egela.ehu.eus/pluginfile.php/3349504/mod_resource/content/12/WS_2020-04-06_Praktika3_eXist-db_gida.pdf
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
        erantzuna = requests.get(pdf_url, headers=goiburuak,
                           allow_redirects=False)  # goiburuak pasa behar dizkiogu, bertan cookia dugulako. eta pdf-ak deskargatzeko kautotuta egotea beharrezkoa da.

        pdf_file = erantzuna.content   # edukia

        split= pdf_url.split('/')
        pdf_name=split[len(split)-1]

        print("pdf_name: "+pdf_name  + "pdf_url    "+  pdf_url)  #el eduki mjr no imprimo
        #############################################

        return pdf_name, pdf_file