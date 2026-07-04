# CuriousSquid
Compagnie-related, search and analytic OSINT engine

This framework is a work-in-progress, please contact me if you see anything to improve it.

Simultaneous filtering on French corporate networks : Fortune 500, Forbes, Offshore Leaks
and more...


## FUNCTIONALITY
* StartingTentacle.py downloads the mapping data available for the given company via pappers.fr. It sorts the data and stores it in `/Outputs/` in three files:
  - `SOA_session.txt` contains the entire dataset,
  - `SOE_session.txt` contains the list of related companies,
  - `SOP_session.txt` contains the list of related individuals.

* Several tools are then available: 
  - View the raw data
  - Search for keywords in StartingTentacle dataset
  - Check if CuriousSquid finds any related individuals listed on the Forbes website
  - Check if CuriousSquid finds any related companies listed on the Fortune website
  - Search for data included in the BODACC database
  - Check if certain companies appear in offshore money-laundering company leaks

## INITIALISATION
Offshores filter algorythme require public offshores leaks. You can download them on the official website : 
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

You can modify the way CuriousSquid use StartingTentacle options in its `main` function (by default, it stores output files in `/Ouputs/`).
