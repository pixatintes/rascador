
__author__ = 'albert'

import urllib.request,sys,pickle,smtplib
from bs4 import BeautifulSoup
import easygui as eg                #modul gui cridar i guardar fitxers
import webbrowser as web            #obre navegador
from email.mime.text import MIMEText#modul email

class Pagina:
    def __init__(self):
        '''
        constructor i defineix la pagina
        
        http://vk.com/prensa_y_revistas_en_espanol
        
        :param servername:
        :param path:
        :return:
        '''
        self.pagines = []  
        self.url_posts=[]
        self.busqueda = ""     
        self.trobat= []
        
    def _aconsegueix(self, direccio):
        '''
        _aconsegueix la pagina
        :return:
        '''
        with urllib.request.urlopen(direccio) as resposta:              #crida una pagina
            la_pagina = resposta.read()                                 #llegeix la pagina
        return la_pagina                                                #retorna la pagina com a text
        
    def __bs(self, url):
        '''
        creem l'objecte beautifulsoup
        '''
        bs=BeautifulSoup(url,'html.parser')
        return bs
    
    def __bs_busca(self,bs,tag,attr_key=None, attr_value=None):
        '''
        Busca tots els tags coincidens amb una classe
        retorna una llista
        '''
        if attr_key == None or attr_value == None:
            bs_list = bs.find_all(tag)
        else:
            bs_list = bs.find_all(tag , attrs={attr_key:attr_value})
        return bs_list
    
    def __bs_busca_text(self,bs,argument):
        '''
        Busca coincidencies en un objecte bs
        1- extreu el text 
        2- comprova coincidencies
        3- retorna boolean
        '''
        coincideix=False
        
        for item in bs:                                         
                text= item.stripped_strings                             #convertim tots els elements de tex en una llista  d'string
                inner = ""
                for s in text:                                          #iterem en la llista destrings
                    inner = repr(s).upper()                             #ho passem a majuscules 
                    #print(inner,'\n\n')
                    if argument.upper() in inner:                          #comprobem si la busqueda te coincidencies
                        coincideix=True
                        break                                            #deixem de buscar en el post        
        return coincideix
    
    def exp(self, file=None):
        '''
        exporta
        '''
        if file ==None:
            file = eg.filesavebox(msg="Guardar fitxer",
                                  title="exporta fitxer: laBSK")
        
        
        with open(file, mode='wb') as f:
            pickle.dump(self,f)
            
    def imp(self, file=None):
        '''
        importa un objecte 
        '''
        extension = ["*.obj"]
        if file ==None:
            file = eg.fileopenbox(msg="Obrir fitxer",
                                  title="importa fitxer: laBSK",
                                  default='',
                                  filetypes=extension)
        
        with open(file, mode='rb') as f:
            imp=pickle.load(f)
        return imp    
    
    def mostra(self):
        '''
        obre una pestanya nova al navegador amb els posts trobats
        '''
        for post in self.trobat:
            web.open_new_tab(post)
            
    def mail(self, desde=None, a=None, pwd=None):
        '''
        envia un correu electrònic amb els resutats trobats
        1-en cas de no estar declarats emisor i receptor
        es demanara
        2-si no s'ha donat la contrasenya 
        es demanará
        '''
        #configurar el mail
        COMMASPACE = ', '
        if desde==None or a==None:
            msg = "(nomes es pot enviar desde gmail)"
            title = "Enviar correu"
            fieldNames = ["From","To"]
            fieldValues = [desde,a]  # we start with blanks for the values
            fieldValues = eg.multenterbox(msg,title, fieldNames,fieldValues)
            
            sender = fieldValues[0]
            recipients = fieldValues[1]
        else:
            sender=desde
            
            
        if pwd==None:
            gmail_password = eg.passwordbox(msg="Entra la teva contrasenya", title="Password")
        else:
            gmail_password = pwd
            

            
        # Create the enclosing (outer) message
        
        cos = "S'han trobat els seguents links: \n"
        for link in self.trobat:
            cos = cos + link +'\n'
        outer=MIMEText(cos)
        outer['Subject'] = "Resultats a laBSK pel joc: {} " .format(self.busqueda)
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        
        composed = outer.as_string()
    
    
        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(sender, gmail_password)
                s.sendmail(sender, recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise
            
    def get_urls(self,num=1, base='http://labsk.net/index.php?board=22.00'):
            
            self.pagines=[base]
            
            if num > 1:
                count=0
                
                for i in range(num):
                        count = count + 20
                        url = 'http://labsk.net/index.php?board=22.' + str(count)
                        self.pagines.append(url)
        
    def posts(self, tag='td',attr_key='class', attr_value='subject lockedbg2'):
        '''
        agafa i retorna una llista amb els elements "html" i de classe donades
        '''
        for url in self.pagines:                                           #iterem en la llista de pagines per buscar tots els posts
#            print(url)                                                    
            bs = self.__bs(self._aconsegueix(url))    #creem l'objecte __bs
            divs= self.__bs_busca(bs, tag, 'class', attr_value)             #busquem tots els 'tags' amb 'class' donades  
            for div in divs:                                            #iterem tag x tag
                    link = div.a['href']                                #busquem el link al post
                    self.url_posts.append(link)                                  #guardem el link al la llista de posts
    
    def buscar(self, busca):
        '''
        busca dins del post si hi han coincidencies i retorna una llista amb els links dels posts coincidents
        '''
        #creem la llista a tornar
        self.busqueda = busca
        self.posts('td','class', 'subject lockedbg2')  
        count=len(self.url_posts)                 #busquem tots els posts        #iterem tots els posts
        i=0
        for post in self.url_posts:
            #creem un '__bs' per cada post
            bs=self.__bs(self._aconsegueix(post))
            xcent=str(int((i*100)/count))
            print(xcent,'%')
            i= i+1
            llista=self.__bs_busca(bs, 'div', 'class', 'inner')         
            if self.__bs_busca_text(llista, busca):                     #busquem lelement on hi ha el text del post
                if post not in self.trobat:                             #si no està guardat
                    self.trobat.append(post)                            #l'adjuntem el link del post a la llista
        
    
                    
def main(busca,num):

        p = Pagina()
        p.get_urls(num) 
        p.buscar(busca)
        p.trobat
        p.mostra()   
                    
                    
                    
if __name__ == "__main__":
        
        total = len(sys.argv)
        print(total)
        if total == 3:
                arg1 = str(sys.argv[1])
                arg2 = int(str(sys.argv[2]))
        elif total == 2:
                arg1 = str(sys.argv[1])
                arg2 = 1
        else:  
                arg1 = 'gmt'
                arg2 = 1
        
        main(arg1, arg2)
        
        print(arg1,arg2)
        
    


main('dawn', 1)
