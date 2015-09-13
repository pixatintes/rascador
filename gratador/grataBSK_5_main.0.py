
__author__ = 'albert'

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import sys


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
        self.links={}
        
        
        for link in self.post_link:
            print(link)

    def aconsegueix(self, direccio):
        '''
        aconsegueix la pagina
        :return:
        '''
        
        with urllib.request.urlopen(direccio) as resposta:

            la_pagina = resposta.read()

        return la_pagina
    
    
    def categories(self, tag='td', classe='subject lockedbg2'):
        posts =[]    
        for url in self.urls:      
#            print(url)        
            bs = BeautifulSoup(self.aconsegueix(url), 'html.parser')
            divs= bs.find_all(tag , attrs={'class':classe})
            for div in divs:
                    link = div.a['href']
                    posts.append(link)
#                    print(link)        
        return  posts    

        
    
    def buscar(self, busca):
        
        trobat=[]
        
        posts = self.categories('td', 'subject lockedbg2')
        for post in posts:
            bs=BeautifulSoup(self.aconsegueix(post),'html.parser')
            
            llista=bs.find_all('div', attrs={'class':'inner'})
            for item in llista:
                text= item.stripped_strings
                inner = ""
                for s in text:
                    inner = repr(s).upper()
                    #print(inner,'\n\n')
                    if busca.upper() in inner:
                        trobat.append(post)
                        break
        return trobat
                    
def main(busca,num):

        Pagina(busca,num)
                    
if __name__ == "__main__":
        
        total = len(sys.argv)
#        print(total)
        if total == 1:                # Sense arguments, fixem tot
                arg1 = 'gmt'
                arg2 = 1
        elif total == 2:                # 1 argument, fixem arg2
                arg1 = str(sys.argv[1])
                arg2 = 1
        else:                # l'ultim es pag, la resta busq
                arg2 = int(str(sys.argv[int(total)-1]))
                arg1 = ''
                for i in range(int(total)-2):
                        val = str(sys.argv[i+1])
                        arg1 = ' '.join([arg1, val])
                print(arg1)

        main(arg1, arg2)

        print(arg1, '\n',arg2)
 







