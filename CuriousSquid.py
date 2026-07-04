import pycurl
from io import BytesIO
import requests
import subprocess
import random
import click
import json
from io import StringIO
import os

###########################################
### COLLECT DATA FROM STARTING TENTACLE ###
###########################################

es = []
sirens = []
starting_Sirens = []
def DisassembleEntreprises(content, silent_mode = False):
    entreprises = content.split('\n')
    if entreprises[len(entreprises)-1] == '':
        entreprises.remove('')
    if not silent_mode:
        print(f'Companies : \n {entreprises}')
        print('\033[0m')
    return entreprises
    

########################
### TENTACLE FILTERS ###
########################

def check_url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

### FORTUNE FILTER ###

matches = []
def GetFortuneMatches(c_name):
    url = f'https://fortune.com/company/{c_name}/'
    if not check_url_exists(url):
        print(f'\033[0;91m Fortune 500 not matched ! ({url}) \033[0m')
        return -1
    print(f'\033[1;32m FORTUNE 500 MATCHED : {url} \033[0m')
    matches.append(url)
    return url

def GetMatchContent():
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    http_response_code = None
    b = BytesIO()
    headers = []
    headers.append('accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8')
    headers.append('accept-language: fr-FR,fr;q=0.9')
    headers.append('cache-control: no-cache')
    headers.append('pragma: no-cache')
    headers.append('priority: u=0, i')
    headers.append('referer: https://fortune.com/ranking/global500/')
    headers.append('sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"')
    headers.append('sec-ch-ua-mobile: ?0')
    headers.append('sec-ch-ua-platform: "Linux"')
    headers.append('sec-fetch-dest: document')
    headers.append('sec-fetch-mode: navigate')
    headers.append('sec-fetch-site: same-origin')
    headers.append('sec-fetch-user: ?1')
    headers.append('sec-gpc: 1')
    headers.append('upgrade-insecure-requests: 1')
    headers.append('user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
    
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.WRITEDATA, b)
    try:
        c.perform()
        http_response_code = c.getinfo(pycurl.HTTP_CODE)
        print(http_response_code)
    except:
        print(f"{e}")
    finally:
        c.close()
    return 0

def GetFortuneInfoAll(es):
    print('\nChecking matches :\n')
    i = 1
    l = len(es)
    for e in es:
        print("\033[0m\n\033[3;90m" + str(i) + " / " + str(l) + "...")
        print('\033[3;90m'+e+'\033[0m')
        company_name = e.replace(' ', '-').lower()
        GetFortuneMatches(company_name)
        if '-sas' in company_name:
            GetFortuneMatches(company_name.replace('-sas', ''))
        if '-sa' in company_name:
            GetFortuneMatches(company_name.replace('-sa', ''))
        if 'sci-' in company_name:
            GetFortuneMatches(company_name.replace('sci-', ''))
        if 'france-sa' in company_name:
            GetFortuneMatches(company_name.replace('france-sa', ''))
        i += 1
    
    if(len(matches) > 0):
        print(f'\nmatches : {matches}\n')
    else:
        print('No match found...\n')
        return -1
    return 0

### FORBES FILTER ###

ceos = []
def CheckCEO(_p):
    url = f'https://www.forbes.com/profile/{_p}/'
    print('\033[3;90mChecking for : ' + _p + '\033[0m')
    if check_url_exists(url):
        print("\033[1;32mMATCHED ! " + url + '\033[0m')
        ceos.append(url)
    else:
        print('\033[0;91mNot matched for ' + url + '\033[0m')
        
    url = f'https://www.forbes.com/sites/forbeswealthteam/article/{_p}-definitive-guide/'
    if check_url_exists(url):
        print("\033[1;32mMATCHED ! " + url + '\033[0m')
        ceos.append(url)
    else:
        print('\033[0;91mNot matched for ' + url + '\033[0m')

def AnalysePersonalities(personalities):
    ps = personalities.split('\n')
    if ps[len(ps)-1] == '':
        ps.remove('')
    print(ps)
    print('\033[0m')
    i = 1
    l = len(ps)
    for _p in ps:
        print("\033[0m\n\033[3;90m" + str(i) + " / " + str(l) + "...")
        CheckCEO(_p)
        i += 1
    if len(ceos) == 0:
        print('\n\033[1;91mNo personnalities founded on forbes...' + '\033[0m')
        return 0
    print('\nFounded personnalities :')
    print(ceos)
    return 1

### BODAC ###

class BRecord:
    def __init__(self, ri, ts, fl, t):
        self.recordid = ri
        self.record_timestamp = ts
        self.familleavis_lib = fl
        self.text = t
        
def Bodacc(default_siren):
    print('bodacc-datadila.opendatasoft.com')
    sir = str(input(f"Setup siren ({default_siren}) > "))
    if sir == "" or sir == None:
        sir = str(default_siren)
    url = f"https://bodacc-datadila.opendatasoft.com/api/records/1.0/search/?dataset=annonces-commerciales&q={sir}&rows=999"
        
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    http_response_code = None
    b = BytesIO()
    #headers = []
    #c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.WRITEDATA, b)
    try:
        c.perform()
        http_response_code = c.getinfo(pycurl.HTTP_CODE)
        if http_response_code == 200:
            print("HTTP RESPONSE CODE OK...\n")
            response_body = b.getvalue().decode('utf-8')
            json_response = json.loads(response_body)
            records = json_response['records']
            brs = []
            text = ""
            i = 0
            print('\t ID \t|\tRECORDID \t\t\t\t : RECORD_TIMESTAMP\t\t (FAMILLEAVIS_LIB)')
            for r in records:
                br = BRecord(r['recordid'], r['record_timestamp'], r['fields']['familleavis_lib'], json.dumps(r, indent=2, ensure_ascii=False))
                brs.append(br)
                print("\t" + str(i) + "\t|\t" + br.recordid + " : " + br.record_timestamp + " \t (" + br.familleavis_lib + ")")
                i+=1
            p = False
            while not p:
                try:
                    _input = int(input("show ID (-1 = main menu) > "))
                    if _input == -1: 
                        p = True;
                    else:
                        print(brs[_input].text + '\n')
                except:
                    print("bad format / index out of range")
    except Exception as e:
        print(f"{e}")
    finally:
        c.close()
    return 0

### OFFSHORES LEAKS ###

def OffshoresGrep(filename, search):
    #os.system(f"cat {filename} | grep -i \"{search}\"")
    cmd = ['cat', filename]
    cat_result = subprocess.run(cmd, capture_output=True, text=True)
    cmd = ['grep', '-i', search]
    grep_result = subprocess.run(cmd, input=cat_result.stdout, capture_output=True, text=True)
    return grep_result.stdout

def OffshoresAutoMode(startContent):
    folder = "./Rscs/offshores/"
    files = [ folder + "nodes-addresses.csv", folder + "nodes-entities.csv", folder + "nodes-intermediaries.csv", folder + "nodes-officers.csv", folder + "nodes-others.csv", folder + "relationships.csv"]
	
    companies = DisassembleEntreprises(startContent, True)
    print("This may take a few minutes...")
    gs = [""]
    for f in files:
        print(f"CHECKING IN {f}...\n")
        for c in companies:
            g = OffshoresGrep(f, c)
            if not g in gs:
                print(f"\033[3;90m {c} \033[0m")
                print(g)
                gs.append(g)
    return 0

###################
### APPLICATION ###
###################

### APPLICATION FUNCTIONS ###

### Display Starting Tentacle Data ###
def F(allStartOutputFile):
    os.system(f"gnome-terminal -- less {allStartOutputFile}")
    return 0

### Manual search   ###
def G(allStartOutputFile):
    search = str(input('\033[0;95msearch > '))
    print('\033[0m')
    cmd = ['cat', allStartOutputFile]
    result2 = subprocess.run(cmd, capture_output=True, text=True)

    cmd = ['grep', '-i', search]
    result3 = subprocess.run(cmd, input=result2.stdout, capture_output=True, text=True)
    print(result3.stdout)
    print(result3.stderr)
    return 0

### Get Forbes infos ###
def B(startingOutputPersonalitiesFile):
    print('\033[3;90mDisassembling personalities :')
    f = open(startingOutputPersonalitiesFile)
    personalities = f.read()
    f.close()
    AnalysePersonalities(personalities)
    return 0

### Get Fortunes infos ###
def T(startContent):
    print('\033[3;90mDisassembling companies :')
    es = DisassembleEntreprises(startContent)
    # get fortune infos :
    print('Getting infos, please wait...')
    GetFortuneInfoAll(es)
    return 0

def L(startContent):
    i = str(input(" Automatic / Manual (A/m) > ")).lower()
    if i == 'm':
        os.system("gnome-terminal -- python3 offshores_filter.py")
    else:
        OffshoresAutoMode(startContent)
    return 0

### APPLICATION MAIN ### 

cmds = 'efgbtsl'
@click.command()
@click.option('-s', default="", help='Company\'s siren to investigate (format integer : xxxxxxxxx)')
def main(s):
    session_id = random.randrange(0, 100000)
    
    ### GET Start infos ###
    
    print('\n\033[1;36m INITIALISATION (StartingTentacle.py)...\033[0m')
    
    startingOutputCompaniesFile = f'./Outputs/soe_{session_id}.txt'
    startingOutputPersonalitiesFile = f'./Outputs/sop_{session_id}.txt'
    result = subprocess.run(['python3', 'StartingTentacle.py', '-s', s, '-o', startingOutputCompaniesFile, '-p', startingOutputPersonalitiesFile], capture_output=True, text=True)
    allStartOutputFile = f'./Outputs/soa_{session_id}.txt'
    with open(allStartOutputFile, "w") as file:
        file.write(result.stdout)
    
    full_text = ""
    if "An error occurred" in result.stdout: 
        print("\033[1;91m" + result.stdout + "\033[0m")
        print("EXIT ERROR")
        exit()
    else:
        full_text = result.stdout
    print(result.stderr)
    f = open(startingOutputCompaniesFile)
    startContent = f.read()
    f.close()
    
    print("\n\033[1;34m ███████╗██╗   ██╗███╗   ██╗ █████╗ ██████╗ ███████╗███████╗    ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗\n ██╔════╝╚██╗ ██╔╝████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝\n ███████╗ ╚████╔╝ ██╔██╗ ██║███████║██████╔╝███████╗█████╗      ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   \n ╚════██║  ╚██╔╝  ██║╚██╗██║██╔══██║██╔═══╝ ╚════██║██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   \n ███████║   ██║   ██║ ╚████║██║  ██║██║     ███████║███████╗    ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   \n ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   \033[0m\n")
    
    #####################################################################################################
    #                                            CONSOLE                                                #
    #####################################################################################################
    
    print("\n\033[1;36m CURIOUS SQUID 1.5.7-04\n\033[0m")
    in_console = True
    main_console =  '\033[0m\n\t\033[1;35m[e]\033[0m\033[3;95m Exit'
    main_console += '\033[0m\n\t\033[1;35m[f]\033[0m\033[3;95m Show StartingTentacle infos'
    main_console += '\033[0m\033[0;95m\n\n\tImplemented tools :' + '\033[0m\t\t\033[1;95m|\033[0m\033[0;95m\tStartingTentacle filters :'
    main_console += '\033[0m\n\t\t\033[1;35m[g]\033[0m\033[3;95m Grep' + '\033[0m\t\t\033[1;95m|\033[0m\t\t\033[1;35m[b]\033[0m\033[3;95m Forbes'
    main_console += '\033[0m\n\t\t\033[1;35m[s]\033[0m\033[3;95m BODACC' + '\033[0m\t\t\033[1;95m|\033[0m\t\t\033[1;35m[t]\033[0m\033[3;95m Fortune'
    main_console += '\033[0m\n\t\t\t\t\t\033[1;95m|\033[0m\t\t\033[1;35m[l]\033[0m\033[3;95m Offshore leaks'

    main_console += '\033[0m\n\033[0;95m > \033[0m\033[4;95m'
    
    while in_console:
        print('\n\033[1;36m MAIN MENU\033[0m')
        i = str(input(main_console))
        print('\033[0m')
        if not i in cmds:
            print('\033[1;91mBad format !\033[0m')
        else:
            if i == 'e':
                in_console = False
            if i == 'f':
                F(allStartOutputFile)
            if i == 'g':
                G(allStartOutputFile)
            if i == 'b':
                B(startingOutputPersonalitiesFile)
            if i == 't':
                T(startContent)
            if i == 's':
                Bodacc(s)
            if i == 'l':
                L(startContent)
                
    print("\033[0m Exiting...")
    exit()
    return
if __name__ == '__main__':
    main()
    print("Exiting...")
    exit()
