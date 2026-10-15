# CuriousSquid
Compagnie-related OSINT engine

This framework is a work-in-progress, please contact me if you see anything to improve it.

Simultaneous filtering on French corporate networks : Fortune 500, Forbes, Offshore Leaks
and more...

## DEPENDENCIES
python librairies :
- os
- io
- csv
- json
- click
- pycurl
- random
- requests
- subprocess


## FUNCTIONALITY
* StartingTentacle.py downloads the mapping data available for the given company on pappers.fr. It sorts the data and stores it in `/Outputs/` in three files:
  - `SOA_session.txt` contains the entire dataset,
  - `SOE_session.txt` contains the list of related companies,
  - `SOP_session.txt` contains the list of related individuals.

* Several tools are then available: 
  - [f] View the raw data
  - [g] Search for keywords in StartingTentacle dataset
  - [b] Check if CuriousSquid finds any related individuals listed on the Forbes website
  - [t] Check if CuriousSquid finds any related companies listed on the Fortune website
  - [s] Search for data included in the BODACC database
  - [l] Check if certain companies appear in offshore money-laundering company leaks
  - [i] Find company administrative documents

* The request for the administrative document search tool is customizable :
```bash
#!/bin/bash

# modify 'siren=xxxxxxxxx' and 'page=x' in the url below to adapt the script to the targeted compagny and files lists

curl 'https://api.pappers.ai/v2/recherche-documents?api_token=97a405f1664a83329a7d89ebf51dc227b90633c4ba4a2575&q=&siren=xxxxxxxxx&tri_documents_date_depot_tous=desc&page=1&per_page=10' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'DNT: 1' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-Site: none' \
  -H 'Priority: u=0, i' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -o ./SqdEyes/output.json
```


## INITIALISATION
The algorithm for filtering and searching through the leaked offshore company files requires the ICIJ's public dataset. You can download them on there official website :

https://offshoreleaks.icij.org/pages/database

and then extract all in `/Rscs/offshores`

... or you can use this bash script to do it automaticly :
```bash
chmod +x init_data.sh
./init_data.sh
```

## USAGE
Start the curious console with `-s` followed by the siren's compagny (9 digits strung together) :
```bash
python3 CuriousSquid.py -s <siren>
```

You can also execute StartingTentacle with options : 
```bash
python3 StartingTentacle -s <siren> -o <output/file/for/companies.txt> -p <output/file/for/personalities.txt>
```

And same for SqdEyes :
```bash
python3 SqdEyes -d <path/to/directory> -s <siren>
```

You can modify the way CuriousSquid use StartingTentacle options in its `main`, and SqdEyes in `I` just above `main`.
