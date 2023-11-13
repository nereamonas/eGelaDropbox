import Tkinter as tk
import os
import webbrowser
import eGela
import Dropbox
import helper
import time
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

##########################################################################################################

def make_listbox(messages_frame):
    scrollbar = tk.Scrollbar(messages_frame,bg='#f2f9fc')
    msg_listbox = tk.Listbox(messages_frame, height=20, width=70, exportselection=0, selectmode=tk.EXTENDED)
    msg_listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=msg_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    return msg_listbox

def transfer_files():
    popup, progress_var, progress_bar = helper.progress("transfer_file", "Transfering files...")
    progress = 0
    progress_var.set(progress)
    progress_bar.update()
    progress_step = float(100.0 / len(selected_items1))


    for each in selected_items1:
        print(each)
        pdf_name, pdf_file = egela.get_pdf(each)
        
        progress_bar.update()
        newroot.update()

        if dropbox._path == "/":
            path = "/" + pdf_name
        else:
            path = dropbox._path + "/" + pdf_name

        dropbox.transfer_file(path, pdf_file)

        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        newroot.update()

        time.sleep(0.1)

    popup.destroy()
    dropbox.list_folder(msg_listbox2)
    msg_listbox2.yview(tk.END)

def delete_files():
    popup, progress_var, progress_bar = helper.progress("delete_file", "Deleting files...")
    progress = 0
    progress_var.set(progress)
    progress_bar.update()
    progress_step = float(100.0 / len(selected_items2))

    for each in selected_items2:
        if dropbox._path == "/":
            path = "/" + dropbox._files[each]['name']
        else:
            path = dropbox._path + "/" + dropbox._files[each]['name']
        dropbox.delete_file(path)

        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        newroot.update()

        time.sleep(0.1)

    popup.destroy()
    dropbox.list_folder(msg_listbox2)

def name_folder(folder_name):
    if dropbox._path == "/":
        dropbox._path = dropbox._path + folder_name
    else:
        dropbox._path = dropbox._path + '/' + folder_name
    dropbox.create_folder(dropbox._path)
    var.set(dropbox._path)
    dropbox._root.destroy()
    dropbox.list_folder(msg_listbox2)

def create_folder():
    popup = tk.Toplevel(newroot)
    popup.geometry('200x100')
    popup.title('Dropbox')
    popup.iconbitmap('./favicon.ico')
    helper.center(popup)

    login_frame = tk.Frame(popup, padx=10, pady=10,bg='#f2f9fc')
    login_frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(login_frame, text="Create folder",bg='#f2f9fc')
    label.pack(side=tk.TOP)
    entry_field = tk.Entry(login_frame, width=35)
    entry_field.bind("<Return>", name_folder)
    entry_field.pack(side=tk.TOP)
    send_button = tk.Button(login_frame, text="Send", command=lambda: name_folder(entry_field.get()), bg='#b5d9ff')
    send_button.pack(side=tk.TOP)
    dropbox._root = popup

def copy():
    print("copy")
    popup, progress_var, progress_bar = helper.progress("copy_file", "Copying files...")
    progress = 0
    progress_var.set(progress)
    progress_bar.update()
    progress_step = float(100.0 / len(selected_items2))

    for each in selected_items2:
        if dropbox._path == "/":
            path = "/" + dropbox._files[each]['name']
        else:
            path = dropbox._path + "/" + dropbox._files[each]['name']
        dropbox.copy(path)

        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        newroot.update()

        time.sleep(0.1)

    popup.destroy()
    dropbox.list_folder(msg_listbox2)



def rename_file():
    print("Rename file")
    if len(selected_items2)!=0:
        eginBeharrekoak=[]
        def next(pos):
            if pos<len(selected_items2):
                each = selected_items2[pos]
                # Sortu lehio emergentea
                popupRename = tk.Toplevel(newroot)
                popupRename.config(bg='#f2f9fc')
                popupRename.geometry('320x130')
                popupRename.title('Dropbox - Rename ')
                popupRename.iconbitmap('./favicon.ico')
                helper.center(popupRename)

                frame = tk.Frame(popupRename, padx=10, pady=10,bg='#f2f9fc')
                frame.pack(fill=tk.BOTH, expand=True)

                label = tk.Label(frame, text=dropbox._files[each]['name'] + "-ren izen berria sartu:",bg='#f2f9fc')
                label.pack(side=tk.TOP)
                entry_newName = tk.Entry(frame, width=35)
                entry_newName.pack()

                send_button = tk.Button(frame, text="Rename", command=lambda: rename_confirm(), bg='#b5d9ff')
                send_button.pack(side=tk.TOP)
                send_button = tk.Button(frame, text="Back", command=lambda: back_confirm(), bg='#b5d9ff')
                send_button.pack(side=tk.TOP)
                dropbox._root = popupRename

                def back_confirm():
                    popupRename.destroy()
                    next(pos+1)


                def rename_confirm():
                    if dropbox._path == "/":
                        path_zaharra = "/" + dropbox._files[each]['name']
                        path_berria =  "/" + entry_newName.get()
                    else:
                        path_zaharra = dropbox._path + "/" + dropbox._files[each]['name']
                        path_berria = dropbox._path + "/" + entry_newName.get()
                    bat={'zaharra':path_zaharra, 'berria': path_berria}
                    eginBeharrekoak.append(bat)
                    time.sleep(0.1)

                    popupRename.destroy()
                    next(pos+1)

            if pos == len(selected_items2):   #ondoren egin behar dira. Bestela, adibidez 1 posiziokoa hartzen du, eta izena alfabetikoki ondoren badoa, posizioak aldatzen dira eta ondoren 2 posiziokoa hartzean, berriro fitxategi berdina hautatuko du. Beraz informazioa gorde dut eta ondoren metodoa deitu
                print ("Confirm rename")
                popup, progress_var, progress_bar = helper.progress("rename", "Renaming ...")
                progress = 0
                progress_var.set(progress)
                progress_bar.update()
                progress_step = float(100.0 / len(eginBeharrekoak))

                for eachRename in eginBeharrekoak:
                    dropbox.rename(eachRename['zaharra'], eachRename['berria'])
                    progress += progress_step
                    progress_var.set(progress)
                    progress_bar.update()
                    newroot.update()
                popup.destroy()
                dropbox.list_folder(msg_listbox2)
        next(0)

def share_to_email():
    print("Share file")
    izenGuztiak=''
    for each in selected_items2:
        izenGuztiak=izenGuztiak + dropbox._files[each]['name'] + "  \n"
    # Sortu lehio emergentea
    popupShare = tk.Toplevel(newroot)
    popupShare.config(bg='#f2f9fc')
    popupShare.geometry('370x200')
    popupShare.title('Dropbox - Share file')
    popupShare.iconbitmap('./favicon.ico')
    helper.center(popupShare)

    frame = tk.Frame(popupShare, padx=10, pady=10,bg='#f2f9fc')
    frame.pack(fill=tk.BOTH, expand=True)
    labelFitx = tk.Label(frame, text="Fitxategiak: \n"+izenGuztiak, bg='#f2f9fc')
    labelFitx.pack(side=tk.TOP)
    label = tk.Label(frame, text="Konpartitu nahi diozun pertsonaren email-a idatzi:",bg='#f2f9fc')
    label.pack(side=tk.TOP)
    entry_email = tk.Entry(frame, width=35)
    entry_email.pack()
    def back_confirm():
        popupShare.destroy()
    send_button = tk.Button(frame, text="Share", command=lambda: share_to_email_confirm(), bg='#b5d9ff')
    send_button.pack(side=tk.TOP)
    back_button = tk.Button(frame, text="Back", command=lambda: back_confirm(), bg='#b5d9ff')
    back_button.pack(side=tk.TOP)
    dropbox._root = popupShare

    def share_to_email_confirm():
        print ("Confirm share")
        popup, progress_var, progress_bar = helper.progress("share_to_email", "Sharing files...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()
        progress_step = float(100.0 / len(selected_items2))

        for each in selected_items2:
            if dropbox._path == "/":
                path = "/" + dropbox._files[each]['name']
            else:
                path = dropbox._path + "/" + dropbox._files[each]['name']
            dropbox.share_to_email(path, entry_email.get())

            progress += progress_step
            progress_var.set(progress)
            progress_bar.update()
            newroot.update()
            time.sleep(0.1)
        popup.destroy()
        dropbox.list_folder(msg_listbox2)
        popupShare.destroy()


from_p=[]
path_names=[]

def move():
    print("Move")
    #vamos a coger donde esta ahora y guardarlo.
    from_p = []
    path_names = []

    for each in selected_items2:
        if dropbox._path == "/":
            path = "/" + dropbox._files[each]['name']
        else:
            path = dropbox._path + "/" + dropbox._files[each]['name']
        from_p.append(path)
        path_names.append(dropbox._files[each]['name'])
        newroot.update()

        time.sleep(0.1)

    var3 = tk.StringVar()
    var3.set("From: " + dropbox._path +"    To: hautatu taulan")
    label3 = tk.Label(newroot, textvariable=var3,bg='#f2f9fc')
    label3.grid(row=3, column=2, ipadx=5, ipady=5)
    frame3 = tk.Frame(newroot,bg='#f2f9fc')


    def move_confirm():
        print ("Confirm move")
        popup, progress_var, progress_bar = helper.progress("move", "Moving files...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()
        progress_step = float(100.0 / len(from_p))

        i=0
        while i < len(from_p):
            if dropbox._path == "/":
                to_path = "/" + path_names[i]
            else:
                to_path = dropbox._path + "/" + path_names[i]
            from_path =from_p[i]

            dropbox.move(from_path, to_path)

            progress += progress_step
            progress_var.set(progress)
            progress_bar.update()
            newroot.update()
            i=i+1
            time.sleep(0.1)
        var3.set("")
        buttonMove.pack_forget()
        popup.destroy()
        dropbox.list_folder(msg_listbox2)
        frame3.destroy()
        label3.destroy()

    buttonMove = tk.Button(frame3, borderwidth=4, text="Move", width=10, pady=8, command=move_confirm, bg='#b5d9ff')
    buttonMove.pack(padx=2, pady=2)
    frame3.grid(row=4, column=2, ipadx=10, ipady=10)


def download_file():
    print("Download file")

    for each in selected_items2:
        if dropbox._path == "/":
            path = "/" + dropbox._files[each]['name']
        else:
            path = dropbox._path + "/" + dropbox._files[each]['name']
        newroot.update()
        #hutatu non eta zein izenekin gorde
        archivo_guardado = tkFileDialog.asksaveasfilename(title='Gorde fitxategia: '+ path, filetypes=(
        ("all files", "*.*"), ("pdf files", ".pdf"), ("txt files", ".txt")))

        dropbox.download(path, archivo_guardado)
        time.sleep(0.1)


def upload_file():
    print("upload_file")
    fitx=tkFileDialog.askopenfilenames()

    popup, progress_var, progress_bar = helper.progress("Upload", "Uploading files...")
    progress = 0
    progress_var.set(progress)
    progress_bar.update()
    progress_step = float(100.0 / len(fitx))
    for fichero in fitx:
        #fichero = filedialog.askopenfilename(title="Igo nahi duzun fitxategia hautatu")
        print(fichero)

        #fitxategiaren azpenengo izena soilik hartuko dugu:
        split=fichero.split("/")
        izena=split[len(split)-1]

        if dropbox._path == "/":
            path = "/" + izena
        else:
            path = dropbox._path + "/" + izena

        data = open(fichero,'rb')
        print(data)

        edukia = data.read()

        dropbox.transfer_file(path,edukia)
        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        newroot.update()
    popup.destroy()
    dropbox.list_folder(msg_listbox2)

def share_link():
    print("Get share link")
    if len(selected_items2)!=0:
        def next(pos):
            if pos<len(selected_items2):
                each = selected_items2[pos]
                if dropbox._path == "/":
                    path = "/" + dropbox._files[each]['name']
                else:
                    path = dropbox._path + "/" + dropbox._files[each]['name']
                newroot.update()

                # Sortu lehio emergentea
                popupShareLink = tk.Toplevel(newroot)
                popupShareLink.config(bg='#f2f9fc')
                popupShareLink.geometry('600x150')
                popupShareLink.title('Dropbox - Share file link')
                popupShareLink.iconbitmap('./favicon.ico')
                helper.center(popupShareLink)

                frame = tk.Frame(popupShareLink, padx=10, pady=10, bg='#f2f9fc')
                frame.pack(fill=tk.BOTH, expand=True)

                def actualizar_sharedLink():
                    link = dropbox.list_shared_link(
                        path)  # link-a itzuliko du, jada shared_link bat badu eta false besteka
                    d(link)

                def d(link):
                    def createShareLink():
                        popup, progress_var, progress_bar = helper.progress("CreateShareLink", "Creating share link...")
                        progress = 0
                        progress_var.set(progress)
                        progress_bar.update()
                        progress_step = float(100.0)
                        dropbox.create_share_link(path)
                        progress += progress_step
                        progress_var.set(progress)
                        progress_bar.update()
                        newroot.update()
                        actualizar_sharedLink()
                        popup.destroy()

                    def deleteShareLink():
                        popup, progress_var, progress_bar = helper.progress("DeleteShareLink", "Deleting share link...")
                        progress = 0
                        progress_var.set(progress)
                        progress_bar.update()
                        progress_step = float(100.0)

                        dropbox.revoke_shared_link(link)
                        progress += progress_step
                        progress_var.set(progress)
                        progress_bar.update()
                        newroot.update()
                        actualizar_sharedLink()
                        popup.destroy()

                    if link == False:  # ez du shared link
                        label.config(text=path + " ez du share link-ik.")
                        label.pack(side=tk.TOP)
                        link1.config(text='')
                        link1.pack(side=tk.TOP)
                        s_button.config(text="Create share link", command=lambda: createShareLink())
                        s_button.pack(side=tk.TOP)

                    else:  # shared_link_bat du jada
                        label.config(text=path + "-ren fitxategiaren share link-a")
                        label.pack(side=tk.TOP)

                        def callback():
                            webbrowser.open_new(r"" + link + "")

                        link1.config(text=link)
                        link1.pack(side=tk.TOP)
                        link1.bind("<Button-1>", lambda e: callback())
                        s_button.config(text="Delete share link", command=lambda: deleteShareLink())
                        s_button.pack(side=tk.TOP)

                link = dropbox.list_shared_link(path)  # link-a itzuliko du, jada shared_link bat badu eta false besteka

                label = tk.Label(frame, bg='#f2f9fc')
                s_button = tk.Button(frame, width=12, pady=6, bg='#b5d9ff')

                link1 = Label(frame, fg="blue", cursor="hand2", bg='#f2f9fc')
                d(link)

                def destroypopupShareLink():
                    popupShareLink.destroy()
                    next(pos+1)

                send_button = tk.Button(frame, text="Back", command=lambda: destroypopupShareLink(), width=8, pady=6,
                                        bg='#b5d9ff')
                send_button.pack(side=tk.TOP)
                dropbox._root = popupShareLink
        next(0)
        time.sleep(0.1)


def list_users():
    print("List users")
    for each in selected_items2:
        if dropbox._path == "/":
            path = "/" + dropbox._files[each]['name']
        else:
            path = dropbox._path + "/" + dropbox._files[each]['name']
        newroot.update()

        users,u=dropbox.list_members(path)

        tkMessageBox.showinfo(path + "-ren erabiltzaileak", path + "-k dituen erabiltzaile zerrenda: " + users)

        time.sleep(0.1)


def create_file():
    print("Create file")

    # Sortu lehio emergentea
    popupCreateFile = tk.Toplevel(newroot)
    popupCreateFile.config(bg='#f2f9fc')
    popupCreateFile.geometry('300x200')
    popupCreateFile.title('Dropbox - Create .txt file')
    popupCreateFile.iconbitmap('./favicon.ico')
    helper.center(popupCreateFile)

    frame = tk.Frame(popupCreateFile, padx=10, pady=10,bg='#f2f9fc')
    frame.pack(fill=tk.BOTH, expand=True)

    labelIzena = tk.Label(frame, text="Fitxategiaren izena + luzapena sartu:",bg='#f2f9fc')
    labelIzena.pack(side=tk.TOP)
    entry_izena = tk.Entry(frame, width=35)
    entry_izena.pack()
    labelEduki = tk.Label(frame, text="Barneko edukia idatzi:",bg='#f2f9fc')
    labelEduki.pack()
    entry_eduki = tk.Entry(frame, width=35)
    entry_eduki.pack(ipady=30)

    def create_file_confirm():
        print("Create file confirm")
        popup, progress_var, progress_bar = helper.progress("create file", "Creating files...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()
        progress_step = float(100.0 / 1)
        if dropbox._path == "/":
            path = "/" + entry_izena.get()
        else:
            path = dropbox._path + "/" + entry_izena.get()
        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        newroot.update()
        dropbox.create_file(path,entry_eduki.get())
        popup.destroy()
        dropbox.list_folder(msg_listbox2)
        popupCreateFile.destroy()

    send_button = tk.Button(frame, text="Create", command=create_file_confirm, bg='#b5d9ff')
    send_button.pack(side=tk.TOP)
    dropbox._root = popupCreateFile

def revoke_member():
    print("Revoke member")
    if len(selected_items2)!=0:
        def next(pos):
            if pos<len(selected_items2):
                each=selected_items2[pos]
                if dropbox._path == "/":
                    path = "/" + dropbox._files[each]['name']
                else:
                    path = dropbox._path + "/" + dropbox._files[each]['name']
                newroot.update()
                e, arrayMembers = dropbox.list_members(path)
                arrayMembers.append("all")

                # Sortu lehio emergentea
                app = tk.Tk()
                app.config(bg='#f2f9fc')
                app.geometry('300x150')
                app.title('Dropbox - Revoke member')
                app.iconbitmap('./favicon.ico')
                helper.center(app)
                text="Fitxategia: "+dropbox._files[each]['name']+ "\n   Hautatu ezabatu nahi duzun pertsona:"
                labelTop = tk.Label(app,
                                    text=text, bg='#f2f9fc')
                labelTop.grid(column=0, row=0)

                comboExample = ttk.Combobox(app,
                                            values=arrayMembers)
                print(dict(comboExample))
                comboExample.grid(column=0, row=1)

                print(comboExample.current(), comboExample.get())

                def actualizar_member():
                    e, arrayMembers = dropbox.list_members(path)
                    arrayMembers.append("all")
                    comboExample['values'] = arrayMembers
                    comboExample.set('')

                def revoke_member_confirm():
                    popup, progress_var, progress_bar = helper.progress("Revoke", "Revoking members...")
                    progress = 0
                    progress_var.set(progress)
                    progress_bar.update()
                    progress_step = float(100.0 / 1)
                    print("Revoke member confirm")
                    if comboExample.get() == 'all':
                        dropbox.revoke_all(path)
                    else:
                        if comboExample.get() != '':
                            dropbox.revoke_file_member(path, comboExample.get())
                    actualizar_member()

                    progress += progress_step
                    progress_var.set(progress)
                    progress_bar.update()
                    newroot.update()
                    popup.destroy()

                def back_confirm():
                    app.destroy()
                    next(pos+1)


                revoke_button = tk.Button(app, text="Revoke", command=revoke_member_confirm, width=8, pady=5, bg='#b5d9ff')
                revoke_button.grid(column=0, row=2)

                back_button = tk.Button(app, text="Back", command=back_confirm, width=8, pady=5, bg='#b5d9ff')
                back_button.grid(column=0, row=3)

                app.mainloop()
                dropbox._root = app
        next(0)


def user_info():
    print("User info")
    info=dropbox.user_info()
    # Sortu lehio emergentea

    popupUserInfo = tk.Toplevel(newroot)
    popupUserInfo.config(bg='#f2f9fc')
    popupUserInfo.geometry('600x450')
    popupUserInfo.title('Dropbox - User info')
    popupUserInfo.iconbitmap('./favicon.ico')

    frame = tk.Frame(popupUserInfo, padx=10, pady=10,bg='#f2f9fc')
    frame.pack()

    labelIzena = tk.Label(frame, text="Erabiltzailearen datuak:",bg='#f2f9fc')
    labelIzena.pack()
    labelEduki = tk.Label(frame, text=info,bg='#f2f9fc')   #anchor='w'
    labelEduki.pack()

    def back_confirm():
        popupUserInfo.destroy()

    back_button = tk.Button(frame, text="Back", command=back_confirm, bg='#b5d9ff')
    back_button.pack()
    dropbox._root = popupUserInfo



##########################################################################################################

def check_credentials(event= None):
    egela.check_credentials(username.get(), password.get())

def on_selecting1(event):
    global selected_items1
    widget = event.widget
    selected_items1 = widget.curselection()
    print selected_items1

def on_selecting2(event):
    global selected_items2
    widget = event.widget
    selected_items2 = widget.curselection()
    print selected_items2

def on_double_clicking2(event):
    widget = event.widget
    selection = widget.curselection()
    if selection[0] == 0 and dropbox._path != "/":
        head, tail = os.path.split(dropbox._path)
        dropbox._path = head
    else:
        selected_file = dropbox._files[selection[0]]
        if selected_file['.tag'] == 'folder':
            if dropbox._path == "/":
                dropbox._path = dropbox._path + selected_file['name']
            else:
                dropbox._path = dropbox._path + '/' + selected_file['name']
    var.set(dropbox._path)
    dropbox.list_folder(msg_listbox2)


##########################################################################################################
# Login eGela
root = tk.Tk()
root.config(bg='#f2f9fc')
root.geometry('250x150')
root.iconbitmap('./favicon.ico')
root.title('Login eGela')
helper.center(root)
egela = eGela.eGela(root)

login_frame = tk.Frame(root, padx=10, pady=10,bg='#f2f9fc')
login_frame.pack(fill=tk.BOTH, expand=True)

labelU = tk.Label(login_frame, text="User name:",bg='#f2f9fc')
labelU.pack()
username = tk.Entry(login_frame, width=35)
username.pack()
labelP = tk.Label(login_frame, text="Password:",bg='#f2f9fc')
labelP.pack()
password = tk.Entry(login_frame, width=35, show="*")
password.pack()
password.bind("<Return>", check_credentials)

button = tk.Button(login_frame, borderwidth=4, text="Login", width=10, pady=8, command=check_credentials, bg='#b5d9ff')
button.pack(side=tk.BOTTOM)

root.mainloop()

if not egela._login:
       exit()
# eGela-ko PDF-etako erreferentziak hartu
pdfs = egela.get_pdf_refs()

# Login Dropbox
root = tk.Tk()
root.config(bg='#f2f9fc')
root.geometry('250x100')
root.iconbitmap('./favicon.ico')
root.title('Login Dropbox')
helper.center(root)

login_frame = tk.Frame(root, padx=10, pady=10,bg='#f2f9fc')
login_frame.pack(fill=tk.BOTH, expand=True)
# Login and Authorize in Drobpox
dropbox = Dropbox.Dropbox(root)

label = tk.Label(login_frame, text="Login and Authorize\nin Drobpox",bg='#f2f9fc')
label.pack(side=tk.TOP)
button = tk.Button(login_frame, borderwidth=4, text="Login", width=10, pady=8, command=dropbox.do_oauth, bg='#b5d9ff')
button.pack(side=tk.BOTTOM)

root.mainloop()

##########################################################################################################
# eGela -> Dropbox

newroot = tk.Tk()
newroot.config(bg='#f2f9fc')
newroot.geometry("1100x550")
newroot.iconbitmap('./favicon.ico')
newroot.title("eGela -> Dropbox")
helper.center(newroot)

newroot.rowconfigure(0, weight=1)
newroot.rowconfigure(1, weight=5)
newroot.columnconfigure(0, weight=6)
newroot.columnconfigure(1, weight=1)
newroot.columnconfigure(2, weight=6)
newroot.columnconfigure(3, weight=1)

# PDF-zerrendaren etiketa(0,0)   #
var2 = tk.StringVar()
var2.set("PDF-ak Web Sistemak ikastaroan")
label2 = tk.Label(newroot, textvariable=var2,bg='#f2f9fc')
label2.config(font='Helvetica 10')
label2.grid(column=0, row=0, ipadx=5, ipady=5)

# Dropbox fitxategien zerrendaren etiketa (0,2)
var = tk.StringVar()
var.set("Dropbox path: " + dropbox._path)
label = tk.Label(newroot, textvariable=var,bg='#f2f9fc')
label.config(font='Helvetica 10')
label.grid(row=0, column=2, ipadx=5, ipady=5)

# PDF-en zerrenda duen Frame-a(1,0)
selected_items1 = None
messages_frame1 = tk.Frame(newroot)
msg_listbox1 = make_listbox(messages_frame1)
msg_listbox1.bind('<<ListboxSelect>>', on_selecting1)
msg_listbox1.pack(side=tk.LEFT, fill=tk.BOTH)
messages_frame1.pack()
messages_frame1.grid(row=1, column=0, ipadx=10, ipady=2, padx=2, pady=2)

# Frame >>> botoiarekin (1,1)
frame1 = tk.Frame(newroot,bg='#f2f9fc')
button1 = tk.Button(frame1, borderwidth=4, text=">>>", width=10, pady=8, command=transfer_files, bg='#c4e1ff')
button1.pack()
frame1.grid(row=1, column=1, ipadx=5, ipady=5)

# Dropbox fitxategien zerrenda duen Frame-a (1,2)
selected_items2 = None
messages_frame2 = tk.Frame(newroot,bg='#f2f9fc')
msg_listbox2 = make_listbox(messages_frame2)
msg_listbox2.bind('<<ListboxSelect>>', on_selecting2)
msg_listbox2.bind('<Double-Button-1>', on_double_clicking2)
msg_listbox2.pack(side=tk.RIGHT, fill=tk.BOTH)
messages_frame2.pack()
messages_frame2.grid(row=1, column=2, ipadx=10, ipady=2, padx=2, pady=2)

#1 columna
frame1columna = tk.Frame(newroot,bg='#f2f9fc')
button2 = tk.Button(frame1columna, borderwidth=4, text="Delete", width=12, pady=8, command=delete_files, bg='#c4e1ff')
button2.pack(padx=2, pady=2)
button4 = tk.Button(frame1columna, borderwidth=4, text="Copy", width=12, pady=8, command=copy, bg='#c4e1ff')
button4.pack(padx=2, pady=2)
button5 = tk.Button(frame1columna, borderwidth=4, text="Rename", width=12, pady=8, command=rename_file, bg='#c4e1ff')
button5.pack(padx=2, pady=2)
button6 = tk.Button(frame1columna, borderwidth=4, text="Move", width=12, pady=8, command=move, bg='#c4e1ff')
button6.pack(padx=2, pady=2)
frame1columna.grid(column=3, row=1, ipadx=10, ipady=10)

#2 columna
frame2columna = tk.Frame(newroot,bg='#f2f9fc')
button3 = tk.Button(frame2columna, borderwidth=4, text="Create folder", width=12, pady=8, command=create_folder, bg='#c4e1ff')
button3.pack(padx=2, pady=2)
buttonCreateFile = tk.Button(frame2columna, borderwidth=4, text="Create file", width=12, pady=8, command=create_file, bg='#c4e1ff')
buttonCreateFile.pack(padx=2, pady=2)
buttonUploadFile = tk.Button(frame2columna, borderwidth=4, text="Upload file", width=12, pady=8, command=upload_file, bg='#c4e1ff')
buttonUploadFile.pack(padx=2, pady=2)
buttonDownloadFile = tk.Button(frame2columna, borderwidth=4, text="Download file", width=12, pady=8, command=download_file, bg='#c4e1ff')
buttonDownloadFile.pack(padx=2, pady=2)
frame2columna.grid(column=4, row=1, ipadx=10, ipady=10)

#3 columna
frame3columna = tk.Frame(newroot,bg='#f2f9fc')
buttonFileUsers = tk.Button(frame3columna, borderwidth=4, text="List Users", width=12, pady=8, command=list_users, bg='#c4e1ff')
buttonFileUsers.pack(padx=2, pady=2)
buttonShareFile = tk.Button(frame3columna, borderwidth=4, text="Share to member", width=12, pady=8, command=share_to_email, bg='#c4e1ff')
buttonShareFile.pack(padx=2, pady=2)
buttonLink = tk.Button(frame3columna, borderwidth=4, text="Revoke member", width=12, pady=8, command=revoke_member, bg='#c4e1ff')
buttonLink.pack(padx=2, pady=2)
buttonLink = tk.Button(frame3columna, borderwidth=4, text="Share link", width=12, pady=8, command=share_link, bg='#c4e1ff')
buttonLink.pack(padx=2, pady=2)
frame3columna.grid(column=5, row=1, ipadx=10, ipady=10)

#user info
frameuser = tk.Frame(newroot,bg='#f2f9fc')
buttonUserInfo = tk.Button(frameuser, borderwidth=4, text="User info", width=12, pady=8, command=user_info, bg='#c4e1ff')
buttonUserInfo.pack(padx=2, pady=2)
frameuser.grid(column=4, row=5, ipadx=10, ipady=10)


#---------------------------------------------------



#----------------------------------------
def search():
    print("search")
    dropbox.search(msg_listbox2,entrySearch.get())

#search
frameSearch = tk.Frame(newroot,bg='#f2f9fc')
entrySearch = Entry(frameSearch)
entrySearch.pack(side = LEFT )
frameSearch.grid(row=5, column=2, ipadx=100, ipady=10)
buttonSearch = tk.Button(frameSearch, borderwidth=4, text="Bilatu", width=10, pady=5, command=search, bg='#b5d9ff')
buttonSearch.pack( side = LEFT )

#-------------------------------------

for each in pdfs:
    msg_listbox1.insert(tk.END, each['pdf_name'])
    msg_listbox1.yview(tk.END)

dropbox.list_folder(msg_listbox2)

newroot.mainloop()