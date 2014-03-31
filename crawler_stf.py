 #!/usr/local/bin/python
 # coding: utf-8
 
 
from pandas import DataFrame
import thread
import urllib2
from bs4 import BeautifulSoup
import string
from tempfile import TemporaryFile

def retorna_busca_mesmo(html, parametro, subs):
    i=0
    for sting in html.stripped_strings:
        print sting
        if (parametro in sting)==True:
            i=i+1
            return string.replace(sting, subs, "")
        i=i+1

def retorna_busca(html, parametro):
    i=0
    m=0
    for string in html.stripped_strings:
        if (parametro in string)==True:
            i=i+1
            m=m+1
            continue
        if  m==1:
            return string            
            i=i+1
        i=i+1


############Salva arquivos


def baixaSTF(base, n):
    url='http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base=' + base + '&s1=' + str(n) + '&processo=' + str(n)
    print(url)
    try:
        html=urllib2.urlopen(url).read()
        return html
    except:
         return False    

def verificaNenhum(html):
    # Verifica se 'nenhum resultado encontrado'
    for string in BeautifulSoup(html).stripped_strings:
         if ("Nenhum resultado" in string)==True:
             return False
         
############### ROTINA SEGUINTE SALVA ARQUIVOS
def SalvaArquivos(base, n=1, j=50):
    while n<j:
        html=baixaSTF(base, n)
        if html==False:
            continue
        if verificaNenhum(html)==False:
            n=n+1
            print('Nenhum resultado encontrado!',str(n))
            continue
        name_file="files_d/stf"+base+str(n)+".apo"
        print("Abrindo:", name_file)
        file__ = open(name_file, "wb+")
        file__.write(html)
        file__.close    
        n=n+1



#############################################Fecha

#################Scraper
def stfWorm(base, n):
    name_file="files_d/stf"+base+str(n)+".apo"
    try:
        htmla=open(name_file,"r")
    except:
        print("Erro " + str(n))
        return False
    html=BeautifulSoup(htmla)
    dispositivo=(retorna_busca(html, "Dispositivo Legal"))
    adi_n=(str(n))
    origem=(retorna_busca(html, "Origem"))
    relator=(retorna_busca(html, "Relator"))
    entrada=(retorna_busca(html, "Entrada no STF"))
    distribuicao=(retorna_busca(html, "Distribu"))
    requerente=(retorna_busca_mesmo(html, "Requerente", "Requerente:"))
    requerido=(retorna_busca_mesmo(html, "Requerido", "Requerido :"))
    fundamenta=(retorna_busca(html, "Fundamentação".decode('utf8')))
    if fundamenta!=None and 'Resultado da Liminar'.decode('utf8') in fundamenta:
        fundamenta=''
    rliminar=(retorna_busca(html, "Resultado da Liminar"))
    if rliminar!=None and 'Decisão Plenária da Liminar'.decode('utf8') in rliminar:
        rliminar=''
    dpliminar=(retorna_busca(html, "Decisão Plenária da Liminar".decode('utf8')))
    if dpliminar!=None and ('Resultado Final'.decode('utf8') in dpliminar):
        dpliminar=''
    rfinal=(retorna_busca(html, "Resultado Final"))
    if rfinal!=None and ('Decisão Final'.decode('utf8') in rfinal):
        rfinal=''
    dfinal=(retorna_busca(html, "Decisão Final".decode('utf8')))
    if dfinal!=None and ('Decisão Monocrática'.decode('utf8') in dfinal):
        dfinal=''
    dmliminar=(retorna_busca(html, "Decisão Monocrática da Liminar".decode('utf8')))
    if dmliminar!=None and ('Decisão Monocrática'.decode('utf8') in dmliminar):
        dliminar=''
    dmfinal=(retorna_busca(html, "Decisão Monocrática Final".decode('utf8')))
    if dmfinal!=None and ('Incidentes'.decode('utf8') in dmfinal):
        dmfinal=''
    incidentes=(retorna_busca(html, "Incidentes")) 
    if incidentes!=None and ('Ementa'.decode('utf8') in incidentes):
        incidentes=''
    ementa=(retorna_busca(html, "Ementa"))
    if ementa!=None and ('Index'.decode('utf8') in ementa):
        ementa=''
    index=(retorna_busca(html, "Index"))
    if index!=None and ('Fim do Documento'.decode('utf8') in index):
        index=''
    htmla.close()
    return [adi_n, origem,  relator, entrada, distribuicao, requerente, requerido, dispositivo, fundamenta, rliminar, dpliminar, rfinal, dfinal, dmliminar, dmfinal, incidentes, ementa, index]
    
def requerente_p(requerente):
    if ", 00I" in requerente:
         return '1-PRESIDENTE' 
    elif ", 0II" in requerente:
         return '2-MESA_SENADO'  
    elif ", III" in requerente:
         return '3-MESA_CAMARA'
    elif ", 0IV" in requerente:
         return '4-MESA_ASSEMBLEIA_CAMARADF'
    elif ", 00V" in requerente:
         return '5-GOVERNADOR'
    elif ", 0VI" in requerente:
         return '6-PROCURADOR_GERAL'
    elif ", VII" in requerente:
         return '7-CFOAB'
    elif ", VIII" in requerente:
         return '8-PARTIDO'
    elif ", 0IX" in requerente:
         return '9-CSINDICAL_ENTIDADE'
    else:
         return ''
##########################



########### 

def inicio(base,x=1, p=5100):
    tipo=[]
    adi_n=[]
    origem=[]      
    relator=[]
    dispositivo=[]
    entrada=[]
    distribuicao=[]
    requerente=[]
    requerido=[]
    emenda=[]
    requerentep=[]
    adi_error=[]
    fundamenta=[]
    rliminar=[]
    dpliminar=[]    
    rfinal=[]
    dfinal=[]   
    dmliminar=[]
    dmfinal=[]
    incidentes=[] 
    ementa=[]
    index=[]
    for n in range(x, p):
         list=stfWorm(base, n)
         if (list==False):
             continue
         tipo.append(base)
         adi_n.append(list[0])
         origem.append(list[1])
         relator.append(list[2])
         entrada.append(list[3])
         distribuicao.append(list[4])
         requerente.append(list[5])
         requerido.append(list[6])
         dispositivo.append(list[7])
         fundamenta.append(list[8])
         rliminar.append(list[9])
         dpliminar.append(list[10])
         rfinal.append(list[11])
         dfinal.append(list[12])
         dmliminar.append(list[13])
         dmfinal.append(list[14])
         incidentes.append(list[15]) 
         ementa.append(list[16])
         index.append(list[17])
         print(list[7])
         if  list[7]!=None and ( ('Emenda' or 'emenda' or 'EMENDA') in list[7] ) :
             emenda.append(1)
         else:
             emenda.append(0)
         requerentep.append(requerente_p(list[5]))
         print(n)
    print(adi_n, origem, relator, entrada, distribuicao, requerente, requerido, dispositivo, emenda, requerentep)   
    df = DataFrame({'01_tipo': tipo, '02_numero': adi_n, '03_Origem': origem, '04_relator': relator, '05_data_entrada': entrada, '06_distribuicao': distribuicao, '07_requerente': requerente, '08_requerido': requerido, '09_dispositivo_legal': dispositivo, '10_emenda': emenda, '11_requerente_p': requerentep, '12_fundamentacao': fundamenta, '13_resultadoliminar': rliminar, '14_decisao_plenaria_liminar': dpliminar, '15_resultado_final': rfinal, '16_decisao_final': dfinal, '17_decisao_monocratica_liminar': dmliminar, '18_decisao_monocratica_final':dmfinal, '19_incidentes':incidentes, '20_ementa':ementa, '21_indexacao':index})
    print(df)
    df.to_excel('teste1.xlsx', sheet_name='sheet1', index=False)
