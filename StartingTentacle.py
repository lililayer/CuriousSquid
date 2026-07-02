import pycurl
from io import BytesIO
import json
import click

sirens = []
personnes = []
entreprises = []

class Persona:
    def __init__(self, _id, _prenom, _nom, _date):
        self.id=_id
        self.prenom=_prenom
        self.nom=_nom
        self.date=_date
        return
    def __str__(self):
        return str(self.prenom) + ' ' + str(self.nom) + ' (' + str(self.date) + ')'

class Company:
    def __init__(self, _id, name, siren):
        self.id=_id
        self.name=name
        self.siren=siren
        if not siren in sirens:
            sirens.append(siren)
        return
    def __str__(self):
        return self.name
        
def GetPersonByID(_id):
    for p in personnes:
        if p.id==_id:
            return p
    return None

def GetCompanyByID(_id):
    for e in entreprises:
        if e.id==_id:
            return e
    return None

class LinkPersonaCompany:
    def __init__(self, persona, company):
        self.persona=persona
        self.company=company
        return
    
    def __str__(self):
        return str(self.company) + ' <-> ' + str(self.persona)

class LinkCompany2Company:
    def __init__(self, company1, company2):
        self.company1=company1
        self.company2=company2
        return
    
    def __str__(self):
        return str(self.company1) + ' <-> ' + str(self.company2)

def GetENBySiren(siren):
    for e in entreprises:
        if e.siren == siren:
            return e.name
    return None

def AnalyseJSON(json_response, deeper, siren):
    if deeper:
        print("________\nLooking for " + GetENBySiren(siren))
    print("\nEntreprises liées :\n")
    for item in json_response['entreprises']:
        e = Company(item['id'], item['nom_entreprise'], item['siren'])
        if not e in entreprises:
            entreprises.append(e)
            print('\t(siren :', e.siren+')', e.name)
    
    print("\n\nPersonnes liées :\n")
    for item in json_response['personnes']:
        p = Persona(item['id'], item['prenom'], item['nom'], item['date_naissance'])
        if not p in personnes:
            personnes.append(p)
            print('\t', p)
    
    if not deeper:
        print("\n\nLiens entreprise <-> personne :\n")
        for item in json_response['liens_entreprises_personnes']:
            l = LinkPersonaCompany(GetPersonByID(item[1]), GetCompanyByID(item[0]))
            print('\t',str(l))
        
        print("\n\nLiens entreprise <-> entreprise :\n")
        for item in json_response['liens_entreprises_entreprises']:
            l = LinkCompany2Company(GetCompanyByID(item[0]), GetCompanyByID(item[1]))
            print('\t',l)
    return

def GetINFOBySiren(siren, deeper=False):
    r=0
    # Initialize a BytesIO object to hold the response
    b = BytesIO()
    
    c = pycurl.Curl()
    
    c.setopt(c.URL, f'https://api.pappers.fr/v2/entreprise/cartographie?api_token=97a405f1664a83329a7d89ebf51dc227b90633c4ba4a2575&siren={siren}&inclure_entreprises_dirigees=true&inclure_entreprises_citees=false&inclure_sci=true&autoriser_modifications=true')
    
    # Set HTTP headers
    headers = ['accept: application/json, text/plain, */*']
    headers.append('accept-language: fr-FR,fr;q=0.6')
    headers.append('cache-control: no-cache')
    headers.append('origin: https://www.pappers.fr')
    headers.append('pragma: no-cache')
    headers.append('priority: u=1, i')
    headers.append('referer: https://www.pappers.fr/')
    headers.append('sec-ch-ua: "Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"')
    headers.append('sec-ch-ua-mobile: ?0')
    headers.append('sec-ch-ua-platform: "Linux"')
    headers.append('sec-fetch-dest: empty')
    headers.append('sec-fetch-mode: cors')
    headers.append('sec-fetch-site: same-site')
    headers.append('sec-gpc: 1')
    headers.append('user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
    c.setopt(c.HTTPHEADER, headers)
    
    # Set the response buffer
    c.setopt(c.WRITEDATA, b)
    
    try:
        c.perform()
        http_response_code = c.getinfo(pycurl.HTTP_CODE)
        
        if http_response_code == 200:
            # Get the response body as a string
            response_body = b.getvalue().decode('utf-8')
            json_response = json.loads(response_body)
            AnalyseJSON(json_response, deeper, siren)
            
        else:
            r=1
            print(f"Request failed with status code: {http_response_code}")
    
    except pycurl.error as e:
        r=2
        print(f"An error occurred: {e}")
    
    finally:
        c.close()
    
    return r
    
@click.command()
@click.option('-s', default="", help='Company\'s siren to investigate (format integer : xxxxxxxxx)')
@click.option('-o', default="", help='founded compagnies destinated file')
@click.option('-p', default="", help='founded personalities destinated file')
def main(s, o, p):
    
    ginfo_resp = GetINFOBySiren(s)
    if ginfo_resp != 0:
        print("Exiting...")
        exit()
        
    content = ''
    for e in entreprises:
        content += e.name + '\n'
    with open(f"{o}", "w") as file:
        file.write(content)
    content = ''
    for _p in personnes:
        content += _p.prenom.lower() + '-' + _p.nom.lower() + '\n'
    with open(f"{p}", "w") as file:
        file.write(content)
        
    return
    
if __name__ == '__main__':
    main()
    print("Exiting...")
    exit()
