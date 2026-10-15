#!/bin/bash

# modify 'siren=xxxxxxxxx' and page=x in the url below to adapt the script to the targeted compagny and files lists

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
