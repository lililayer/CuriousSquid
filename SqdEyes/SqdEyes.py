import os 
import json
import click

def request_maker(s, d):
    content  = "#!/bin/bash\n\n"
    content += "# modify 'siren=xxxxxxxxx' and page=x in the url below to adapt the script to the targeted compagny and files lists\n\n"
    content += f"curl 'https://api.pappers.ai/v2/recherche-documents?api_token=97a405f1664a83329a7d89ebf51dc227b90633c4ba4a2575&q=&siren="+s+"&tri_documents_date_depot_tous=desc&page=1&per_page=10' \\\n"
    content += "  --compressed \\\n"
    content += "  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0' \\\n"
    content += "  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \\\n"
    content += "  -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' \\\n"
    content += "  -H 'Accept-Encoding: gzip, deflate, br, zstd' \\\n"
    content += "  -H 'DNT: 1' \\\n"
    content += "  -H 'Connection: keep-alive' \\\n"
    content += "  -H 'Upgrade-Insecure-Requests: 1' \\\n"
    content += "  -H 'Sec-Fetch-Dest: document' \\\n"
    content += "  -H 'Sec-Fetch-Mode: navigate' \\\n"
    content += "  -H 'Sec-Fetch-Site: none' \\\n"
    content += "  -H 'Priority: u=0, i' \\\n"
    content += "  -H 'Pragma: no-cache' \\\n"
    content += "  -H 'Cache-Control: no-cache' \\\n"
    content += f"  -o {d}/output.json\n"
    
    with open(f"{d}/page_request.sh", "w") as f:
        f.write(content)

@click.command()
@click.option('-d', default="", help='working directory')
@click.option('-s', default="", help='siren')
def main(d, s):
    print("INIT...")
    request_maker(s, d)
    os.system(f"nano {d}/page_request.sh")
    input("Press <enter> to continue...")
    print("REQUESTING...")
    os.system(f"{d}/page_request.sh")
    print("DONE")

    path = f"{d}/output.json"
    raw = ""
    with open(f"{path}", "r") as file:
        raw = file.read()
    data = json.loads(raw)
    tokens = []
    if "error" in data:
        print(f"PAPPERS :\n{data}")
        exit()
    for item in data["resultats"]:
        if item["type"] == "acte":
            print("\n\033[1;35mType : " + item["titres"][0]["type"] + f"\n\t\033[1;95m => \033[0m\033[3;95murl https://www.pappers.fr/document/telecharger?token={item['token']}&visualiser\033[0m")
            tokens.append(item["token"])
    print()

if __name__ == '__main__':
    main()
