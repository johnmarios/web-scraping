#ομαδα 56
#Οι βιβλιοθήκες που χρησιμοποιήσαμε

import os
import os.path
import tkinter as tk
import tkinter.ttk as ttk
import requests
import urllib.request
from functools import reduce 
from bs4 import BeautifulSoup
from threading import Thread
from PIL import Image

urlv =  'https://images.wisegeek.com/leather-bound-books.jpg'# σύνδεσμος της εικόνας 


comp1 = '''Η Ελληνική Ψυχολογική Εταιρεία αποφάσισε να εκδώσει την "Ψυχολογία",
           για να δώσει τη δυνατότητα στους Έλληνες ψυχολόγους να
           κοινοποιήσουν σε ένα έγκυρο επιστημονικό βήμα την εργασία τους και
           να πληροφορηθούν για την εργασία των συναδέλφων τους. Η Ψυχολογία
           δηλαδή φιλοδοξεί να λειτουργήσει ως ο καταλύτης που θα επιταχύνει την
           παραπέρα ανάπτυξη των ψυχολογικών σπουδών και της έρευνας στη χώρα.
        '''# η περιγραφή των τόμων της ψυχολογίας

comp2 = 'Επιλέξτε τον τρόπο που θέλετε να κατεβάσετε τα τεύχη του περιοδικού "Ψυχολογία":'

forbidden = ("<", ">", ":", "'", "/", "\\", "|", "?", "*")#χαρακτήρες οι οποίοι δεν επιτρέπονται στο όνομα αρχείου
url1 = "http://pandemos.panteion.gr/index.php?lang=el&op=record&pid=cid:19"#αρχική σελίδα 
maindir = os.getcwd()#κύριο path

class Downloader:    
    """
    Η κλάση Downloader κατεβάζει τα αρχεία και τα ταξινομεί 
    σε φακέλους και υποφακέλους με τα αντίστοιχα ονοματά τους
    """
    def __init__(self, url, main_dir):
        """
        αποθηκεύουμε  στο self.volume_info μέσω της self.getVolumesInfo το αρχικό όνομα του πρώτου 
        συνδέσμου που εντοπίζεται επεξεργασμένο γιά να μπορεί να γίνει όνομα 
        αρχείου(Ψυχολογία: το περιοδικό της Ελληνικής Ψυχολογικής Εταιρείας), 
        τον αριθμό των συνδέσμων που περιέχει(οι Τόμοι), 
        και τους συνδέσμους/ονόματα των τόμων(μια λίστα με πλειάδες που περιέχουν(σύνδεσμο, όνομα))
        """ 
        self.main_dir = main_dir
        self.url = url#ο αρχικός σύνδεσμος
        self.volume_info = self.getVolumesInfo() 
        self.parent_folder, self.volumes_length, self.volume_links = self.volume_info[0], self.volume_info[1], self.volume_info[2]
        if not os.path.isdir(self.parent_folder) and os.getcwd() != self.parent_folder:#Δημιουργόυμε τον αρχικό φάκελο εάν δεν υπάρχει 
            os.mkdir(self.parent_folder)
    
    def removeForbidden(self, name):
        """αφαιρεί τους ανεπίτρεπτους χαρακτήρες σε μιά συβλοσείρα ονόματος αρχείου"""
        name = reduce(lambda s, el: s.replace(el, "-"), forbidden, name)
        #χρησιμοποιείται μία ανώνυμη συνάρτηση ως πρώτο όρισμα, τη πλειάδα των ανεπίτρεπτων χαρακτήρων, και το αρχικό όνομα του αρχείου
        #η συνάρτηση reduce της βιβλιοθήκης functools εφαρμόζει τη συγκεκριμένη lambda συνάρτηση σε κάθε στοιχείο της ακολουθίας παίρνοντας ως πρώτο όρισμα το name 
        return name.strip()

    def getTagName(self, tag):
        """ Παίρνει ως όρισμα ένα bs4.element.Tag αντικείμενο και επιστρέφει το κείμενο συνδέσμου"""
        name = list(tag.children)#μετατρέπουμε το iterator που επιστρέφει η μέθοδος .children σε λίστα 
        return str(name[0])#επιστρέφουμε το πρώτο αντικείμενο της λίστας σε συμβολοσείρα το οποίο θα είναι το κείμενο συνδέσμου
    
    def getSoup(self, url):
        """Επιστρέφει ενά Beautiful Soup αντικείμενο γιά ένα hmtl γιά εύκολη επεξεργασία των ετικέτων hmtl κάθε σελίδας πέρνοντας ως αρχικό όρισμα τον σύνδεσμο της σελίδας"""
        with urllib.request.urlopen(url) as response:
            byteFile = response.read()#αρχείο σε byte που περιέχει το hmtl που πείραμε από τον σύνδεσμο
        myStr = byteFile.decode("utf-8")#αποκωδικοποιούμε το αρχείο
        SoupObject = BeautifulSoup(myStr, "html.parser")#δημιουργόυμε το Beautiful Soup αντικείμενο
        return SoupObject

    def getLinks(self, url, substring = ""):
        """
           Παίρνει ως ορίσματα ένα σύνδεσμο και μία συμβολοσείρα και επιστρέφει μία λίστα με πλειάδες που περιέχουν τον σχετικό
           σύνδεμο και τον σύνδεσμο κειμένου όλων τον a ετίκετων που περιέχουν συνδέσμους και το επιλεγμένο substring μέσα στο κείμενο της ετικέτας
        """
        soup = self.getSoup(url)
        return [(str(tag["href"]), self.getTagName(tag)) for tag in soup.find_all("a", href = True) if substring in str(tag)]
        #ψαχνει τα <a> tags (με την μέθοδο find_all) οπου υπαρχουν τα χαρκτηριστικα href τα οποια περιέχουν τους συνδεσμους και επιστρεφει με list comprehension λίστα με τις πλείαδες 
    
    def getVolumesInfo(self):
        """Επιστρέφει τις πληροφορίες που χρειαζομόστε για να κατεβαστούν οι τόμοι"""
        page1 = self.getLinks(self.url, substring = "Ψυχολογία: το περιοδικό της Ελληνικής Ψυχολογικής Εταιρείας")
        if not page1:
            return ("Ψυχολογία_NoResults", 0, [])
        page1_link, page1_name = page1[0][0], self.removeForbidden(page1[0][1])
        page2 = self.getLinks("http://pandemos.panteion.gr/" + page1_link, substring = "Τόμος")
        return page1_name, len(page2), page2
    
    def downloadVolumes(self, selected_volume_nums = []):
        """Παίρνει ως όρισμα ένα iterable αντικέιμενο που θα περιέχει τους αρίθμους των τόμων που θέλουμε να κατεβάσουμε"""
        os.chdir(os.path.join(self.main_dir, self.parent_folder))#Θέτουμε το path στον κύριο φάκελο
        for index in selected_volume_nums:
            the_volume = self.volume_links[index]
            volume_link, volume_name = the_volume[0], self.removeForbidden(the_volume[1])
            if not os.path.isdir(volume_name):#δημιουργούμε τον φάκελο έαν δεν υπάρχει
                os.mkdir(volume_name)
            pdf_links = self.getLinks("http://pandemos.panteion.gr/" + volume_link, substring = "pid=iid")
            #παρατηρόντας τον html κώδικα βλέπουμαι ότι η συμβολοσείρα "pid=iid" βρίσκεται σε κάθε ετικέτα που περίεχει σύνδεσμο σε σελίδα με pdf, έτσι απομονώνουμε τους συνδέσμους που θέλουμε
            for link, name in pdf_links:
                soup = self.getSoup("http://pandemos.panteion.gr/" + link)
                pdf_name = self.removeForbidden(name)
                for pdf in soup.select("a[href$='.pdf']"):#εντοπίζει τις ετικέτες a στις οποίες ο σχετικός σύνδεμος περιέχει .pdf αρχείο
                    pdfLink = "http://pandemos.panteion.gr/" + pdf["href"]#σύνδεσμος που περιέχει το pdf που θέλουμε
                    try:# Χρησιμοποιούμε Error handling 
                        with open(f"{os.path.join(volume_name, pdf_name)}.pdf", "wb+") as file:#διαβάζουμε το περιέχομενο του αρχείου και το αποθηκέυουμε με το ονομά του.
                            file.write(urllib.request.urlopen(pdfLink).read())
                    except:
                        pass


class MyApp:
    def __init__(self, window):
        self.download_object= Downloader(url1, maindir)
        self.number_of_volumes= self.download_object.volumes_length
        self.w = window
        self.f1 = tk.Frame(window)
        self.f1.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.lbl1=tk.Label(self.f1, text=comp1, font = 'Arial 26', bg='#F4EEFF')# το πρώτο label
        self.lbl1.grid(row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.lbl2=tk.Label(self.f1, text=comp2, font = 'Arial 26', bg='#F4EEFF')#το δεύτερο label
        self.lbl2.grid(row=1, sticky=tk.N+tk.E+tk.S+tk.W)
        self.b1=tk.Button(self.f1, text= 'Πατήστε εδώ για λήψη σε μορφή PDF', font ='Arial 26 bold',bg='#DCD6F7',fg='#424874', command = lambda : self.progbarwindow(range(self.number_of_volumes)))#το πρώτο κουμπί το οποίο κατεβάζει όλους τους τόμους
        self.b1.grid(row=2, sticky=tk.N+tk.E+tk.S+tk.W)
        self.b2=tk.Button(self.f1, text= ' Πατήστε εδώ για να επίλεξτε τον τόμο που θέλετε', font ='Arial 26 bold',bg='#DCD6F7',fg='#424874', command = self.second_window)# το δεύτερο κουμπί που επιλεγεις τον τόμο
        self.b2.grid(row=3, sticky=tk.N+tk.E+tk.S+tk.W)
        self.b3=tk.Button(self.f1, text= 'Πατήστε εδώ για έξοδο', font ='Arial 26 bold',bg='#DCD6F7',fg='#424874', command = lambda : self.w.destroy())#κουμπί για έξοδο
        self.b3.grid(row=4, sticky=tk.N+tk.E+tk.S+tk.W)

    def second_window(self):
        '''δημιουργία δεύτερου παραθύρου'''
        self.w2=tk.Toplevel(self.w)#νέο παράθυρο
        self.w2.geometry('1000x700')#γεωμετρία παραθύρου
        self.w2.resizable(False,False)#αμετάβλητο
        #FRAMES
        self.imagefr = tk.Frame(self.w2)
        self.imagefr.place(anchor='nw')

        self.w2_frame = tk.Frame(self.w2) 
        self.w2_frame.place(relx=0.5, rely = 0.5, anchor = 'center')#τοποθετείται στο κέντρο
        
        #labels

        self.w2_lab1 = tk.Label(self.w2_frame,text = f'Επίλεξε τον τόμο που θες να κατεβάσεις, υπάρχουν {self.number_of_volumes} τόμοι: \nΓράψε τα νούμερα των τόμων που θες χωρισμένα με κόμματα.', font = 'Arial 20')
        self.w2_lab1.grid(row = 0,padx = '4', pady = '4')

        self.w2_lab2 = tk.Label(self.w2_frame, font = 'Arial 30', text = 'Volume:')
        self.w2_lab2.grid(row = 1, column=0, pady = '4',padx = '4', sticky=tk.W)#sticky καθορίζει το που θα τοποθετηθεί το label(δυτικά ως προς το παράθυρο)

        #entry
        
        self.enter_button = tk.Entry(self.w2_frame,  bg = '#DFD3C3', font = 'Arial 20',borderwidth= 4)#αναμένει την είσοδο του χρήστη
        self.enter_button.grid(row=1,padx='2', pady = '4')

        #main button

        self.install = tk.Button(self.w2_frame, text = 'Download', bg = 'grey', font = 'Arial 20', borderwidth='4', command = self.selected_input)#όταν πατιέται το κουμπί καλείται η συνάρτηση
        #select_input
        self.install.grid(row=2, sticky=tk.W + tk.E)

        #exit button

        self.exit = tk.Button(self.w2_frame, text = 'Exit', bg = 'grey',font = 'Arial 20',command=lambda:self.w2.destroy(), borderwidth='4')#καταστρέφει το παράθυρο με τη κλήση ανώνυμης συνάρτησης
        self.exit.grid(row = 3, sticky=tk.E + tk.W, pady = 5)

        #image creation
        self.response = requests.get(urlv)#παίρνει τον σύνδεσμο της εικόνας και στέλνει ένα HTTP request 
        if self.response.status_code == 200:# αν πάρει το σωστό response αποσπά την εικόνα από το περιεχόμενο της σελίδας
            with open('volumes.jpg', 'wb') as volumes:#δημιουργει αρχείο volumes.jpg
                volumes.write(self.response.content)#στο αρχείο τοποθετείται το περιεχόμενο του response
                volumes.close()
                img = Image.open('volumes.jpg')#μετατροπή εικόνας από jpg σε gif λόγω περιορισμού της tkinter
                img.save('volumes.gif')

        self.ph = tk.PhotoImage(file = 'volumes.gif')
        self.image = tk.Label(self.imagefr, image=self.ph)
        self.image.grid(row=0, column=0)#Θέτουμε την εικόνα
    
    def selected_input(self):
        '''Κατεβάζει τα επιλεγμένα τεύχη από το δεύτερο παράθυρο''' 
        try:
            self.inp = [int(i)-1 for i in self.enter_button.get().split(',') if (i.isdigit() and int(i)-1 <= 15)]#η είσοδος από τον χρήστη στο δεύτερο παράθυρο αποθηκεύεται σε λίστα
            self.progbarwindow(self.inp)#καλείται η συνάρτηση progbarwindow με όρισμα την από πάνω λίστα
        except:
            pass

    def progbarwindow(self,selected_volumes):

        if not len(selected_volumes):
            return#το παράθυρο δεν ανοίγει έαν δώσουμε άδεια λίστα 
        self.w3 = tk.Toplevel(self.w)
        self.w3.title('πρόοδος λήψης...')
        self.w3.geometry('300x50')
        
        self.thread = Thread(target=self.thread_download,args=(selected_volumes,))
        #χρησιμοποιούμε multithreading γιά να κατεβάσουμε τα περιοδικά και να τρέχει η μπάρα την ίδια στιγμή 
        self.thread.start()
        self.progbar()
        self.thread.join()
    
    def progbar(self):
        #η μπάρα προόδο
        self.dwnl_progress = ttk.Progressbar(self.w3, orient='horizontal', length=500, mode='indeterminate')
        self.dwnl_progress  .pack(pady=10)
        self.dwnl_progress.start(50)
        self.w3.mainloop()#αρχίζει το 3ο παράθυρο 
    
    def thread_download(self,selected_volumes):
        #το χρησιμοποιούμε ως όρισμα στο Thread 
        self.download_object.downloadVolumes(selected_volumes)
        self.w3.destroy()
           
#--------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title('Λήψη τευχών περιοδικού "ΨΥΧΟΛΟΓΙΑ"')#κύριο παράθυρο
    root.rowconfigure(0,minsize=100, weight=1)
    root.columnconfigure(0, minsize=200, weight=1)
    myapp = MyApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()