
__author__ = 'albert'

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import sys,json,pickle 
import easygui as eg
import webbrowser as web



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
        

        self.exp()
        
        for link in self.trobat:
            print(link)
        
    
    def _aconsegueix(self, direccio):
        '''
        _aconsegueix la pagina
        :return:
        '''
        with urllib.request.urlopen(direccio) as resposta:              #crida una pagina
            la_pagina = resposta.read()                                 #llegeix la pagina
        return la_pagina                                                #retorna la pagina com a text

    def get_urls(self,num=1, base='http://labsk.net/index.php?board=22.00'):
        
        self.pagines=[base]
        
        if num > 1:
            count=0
            
            for i in range(num):
                    count = count + 20
                    url = 'http://labsk.net/index.php?board=22.' + str(count)
                    self.pagines.append(url)
        

        
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
    
    
    def exp(self, nom=None):
        file = eg.filesavebox(msg="Guardar fitxer",
                              title="exporta fitxer: laBSK")
        
        if nom == None:
            nom = ""+self.busqueda + ".obj"
        with open(file, mode='wb') as f:
            pickle.dump(self,f)
            
    def imp(self):
        extension = ["*.obj"]
 
        file = eg.fileopenbox(msg="Obrir fitxer",
        title="importa fitxer: laBSK",
        default='',
        filetypes=extension)
        
        with open(file, mode='rb') as f:
            imp=pickle.load(f)
        return imp    
    def mostra(self):
        for post in self.trobat:
            web.open_new_tab(post)
    
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
#                    print(link)        
    

        
    
    def buscar(self, busca):
        '''
        busca dins del post si hi han coincidencies i retorna una llista amb els links dels posts coincidents
        '''
        #creem la llista a tornar
        self.busqueda = busca
        self.posts('td','class', 'subject lockedbg2')                   #busquem tots els posts
        #iterem tots els posts
        for post in self.url_posts:
            #creem un '__bs' per cada post
            bs=self.__bs(self._aconsegueix(post))
            
            llista=self.__bs_busca(bs, 'div', 'class', 'inner')         #busquem lelement on hi ha el text del post
            if self.__bs_busca_text(llista, busca):                      #si les te adjuntem el link del post a la llista
                self.trobat.append(post)                          
                                             
    
    
                    
def main(busca,num):

        Pagina(busca,num)
                    
                    
                    
                    
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
        
    



