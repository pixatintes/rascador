from bs4 import BeautifulSoup
import os
import json
import urllib.request
import urllib.parse


BASE_DIR = os.path.dirname(__file__)
CONFIGFILE = BASE_DIR + os.path.abspath('/conf.json')


def get_bs(url):
    """
    :param url: Web amb la que crear un...
    :return: Objecte beautifulsoup
    """
    return BeautifulSoup(aconsegueix(url), 'html.parser')



def aconsegueix(direccio):
    """
    aconsegueix la pagina
    :return: retorna una pagina web
    """
    with urllib.request.urlopen(direccio) as res:
        return res.read()


def getconfig():
    f = open(CONFIGFILE, mode='r+')
    conf = json.load(f)
    return conf


def setconfig(*args, **kargs):
    try:
        conf = getconfig()
    except:
        conf = dict()
    print('variables:', args, kargs)
    if args:
        for a in args:
            conf[a]=list()
            print("s'ha afeit el joc {} a la llista".format(a))

    for k in kargs.keys():
        if k in conf.keys():

            conf[k].append(kargs[k])
            print("S'ha afegit el post '{}' al joc '{}'".format(kargs[k], k))

        else:
            conf[k] = [kargs[k], ]
            print("El joc '{}' s'ha afegit i s'hi ha agregat el post '{}'".format(k, kargs[k]))

    f = open(CONFIGFILE, mode='w+')
    json.dump(conf, f, indent=4)
    f.close()
    return True


def delconfig(*args):
    jocs = getconfig()
    borrat = list()
    for j in jocs.keys():
        if j in args:
            print('per borrar',j)
            borrat.append(j)
    for j in borrat:
        del jocs[j]
        print("El joc '{}' s'ha eliminat de la llista".format(j))
    print('despres de borrar', jocs)
    f = open(CONFIGFILE, mode='w+')
    json.dump(jocs, f, indent=4)
    f.close()
    return borrat