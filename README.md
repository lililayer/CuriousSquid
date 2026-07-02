# CuriousSquid
Compagnie-related, search and analytic OSINT engine

This framework is a work-in-progress, please contact me if you see anything to improve it.

Discover the great french fortunes hidden behind the smaller ones

## FUNCTIONALITY
* StartingTentacle.py downloads the mapping data available for the given company via pappers.fr. It sorts the data and stores it in /Outputs in three files:
  - “SOA_session.txt” contains the entire dataset,
  - "SOE_session.txt" contains the list of related companies,
  - “SOP_session.txt” contains the list of related individuals.

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
and then extract all in /Rscs/offshores
... or you can use this bash script to do it automaticly :
```bash
chmod +x init_data.sh
./init_data.sh
```

## USAGE
```bash
python3 CuriousSquid.py -s <siren>
```
