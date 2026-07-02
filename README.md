# CuriousSquid
compagnie-related, search and analytic OSINT engine

this framework is a work-in-progress, please contact me if you see anything to improve it.

Functionality:
* StartingTentacle.py downloads the mapping data available for the given company via pappers.fr. It sorts the data and stores it in /Outputs in three files:
  - “SOA_<session>.txt” contains the entire dataset,
  - "SOE_<session>.txt" contains the list of related companies,
  - “SOP_<session>.txt” contains the list of related individuals.

* Several tools are then available: 
  - View the raw data
  - Search for keywords in the data
  - Check if CuriousSquid finds any related individuals listed on the Forbes website
  - Check if CuriousSquid finds related companies listed on the Fortune website
  - Search for data included in the BODACC database
  - Check if certain companies appear in the offshore money-laundering company leaks
