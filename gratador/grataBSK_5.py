
__author__ = 'albert'

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup





class Pagina:
    def __init__(self,busca='gmt',num=1):
        '''
        constructor i defineix la pagina
        
        http://vk.com/prensa_y_revistas_en_espanol
        
        :param servername:
        :param path:
        :return:
        '''
        self.urls = ['http://labsk.net/index.php?board=22.00']
        count=0
        if num > 1:
                for i in range(num):
                        count = count + 20
                        url = 'http://labsk.net/index.php?board=22.' + str(count)
                        self.urls.append(url)

       
#        self.direccio = direccio
#        self.pagina = self.aconsegueix(self.direccio)
        self.post_link= self.buscar(busca)

        
        
        for link in self.post_link:
            print(link)

    def aconsegueix(self, direccio):
        '''
        aconsegueix la pagina
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
        usca tots els tags coincidens amb una classe
        retorna una llista
        '''
        if attr_key == None or attr_value == None:
            bs_list = bs.find_all(tag)
        else:
            bs_list = bs.find_all(tag , attrs={attr_key:attr_value})
        return bs_list
    
    
    
    def posts(self, tag='td',attr_key='class', attr_value='subject lockedbg2'):
        '''
        agafa i retorna una llista amb els elements "html" i de classe donades
        '''
        posts =[]                                                       #creem la llista a tornar
        for url in self.urls:                                           #iterem en la llista de pagines per buscar tots els posts
#            print(url)                                                    
            bs = self.__bs(self.aconsegueix(url))    #creem l'objecte __bs
            divs= self.__bs_busca(bs, tag, 'class', attr_value)             #busquem tots els 'tags' amb 'class' donades  
            for div in divs:                                            #iterem tag x tag
                    link = div.a['href']                                #busquem el link al post
                    posts.append(link)                                  #guardem el link al la llista de posts
#                    print(link)        
        return  posts

        
    
    def buscar(self, busca):
        '''
        busca dins del post si hi han coincidencies i retorna una llista amb els links dels posts coincidents
        '''
        #creem la llista a tornar
        trobat=[]                                           
        
        posts = self.posts('td', 'subject lockedbg2')                   #busquem tots els posts
        #iterem tots els posts
        for post in posts:
            #creem un '__bs' per cada post
            bs=self.__bs(self.aconsegueix(post))
            
            llista=self.__bs_busca(bs, 'div', 'class', 'inner')         #busquem lelement on hi ha el text del post
            for item in llista:                                         
                text= item.stripped_strings                             #convertim tots els elements de tex en una llista  d'string
                inner = ""
                for s in text:                                          #iterem en la llista destrings
                    inner = repr(s).upper()                             #ho passem a majuscules 
                    #print(inner,'\n\n')
                    if busca.upper() in inner:                          #comprobem si la busqueda te coincidencies
                        trobat.append(post)                             #si les te adjuntem el link del post a la llista
                        break                                           #deixem de buscar en el post           
        return trobat                                                   #retornem els links trobats
                    
                    
        
        
Pagina()



