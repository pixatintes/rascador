
__author__ = 'albert'


import os
from gratador.tools import  BASE_DIR, get_bs, getconfig, setconfig, delconfig


class Pagina:
    def __init__(self,busca='listtxt.txt',num=1):
        '''
        constructor i defineix la pagina

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

        values=[]
        if os.path.isfile(os.path.join(BASE_DIR,busca)):
            with open(busca) as f:
                for line in f:
                    values.append(line.strip())

        for i,v in enumerate(values):
                element = str(values[i])
                print(element)

                self.post_link= self.buscar(element)
                self.links={}
        
                for link in self.post_link:
                   print(link)


    
    def categories(self, tag='td', classe='subject lockedbg2'):
        posts =[]    
        for url in self.urls:      
            print([url])
            bs = get_bs(url)
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
            bs = get_bs(post)
            
            llista=bs.find_all('div', attrs={'class':'inner'})
            for item in llista:
                text= item.stripped_strings
                inner = ""
                for s in text:
                    inner = repr(s).upper()
                    #print(inner,'\n\n')

                    if busca.upper() in inner:
                        if post not in getconfig()[busca]:
                            setconfig(**{busca: post})
                        trobat.append(post)
                        break
        return trobat
                    
def main(busca,num):

        Pagina(busca,num)
                    



            
