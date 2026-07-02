import csv
import os

def ReadCSV(file_name, collumns):
	rs = []
	with open(file_name, 'r', newline='', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			r = []
			for c in collumns:
				r.append(row[c])
			rs.append(r)
	return rs

def GetCSVRowByName(file_name, name):
	os.system(f"cat {file_name} | grep -i \"{name}\"")
	return 0

def StringApproximate(string1, string2):
	s1 = string1.lower()
	s2 = string2.lower()
	if s1 == s2 or s2 in s1:
		return True
	return False

def SearchEntitieName(rows, name):
	psbs = []
	for r in rows:
		if StringApproximate(r[0], name):
			psbs.append(str(r[0]))
			print(str(r[0]))
	return 0

def main():
	print("INITALISATION...")
	folder = "./Rscs/offshores/"
	addresses      = folder + "nodes-addresses.csv"
	entities       = folder + "nodes-entities.csv"
	intermediaries = folder + "nodes-intermediaries.csv"
	officers       = folder + "nodes-officers.csv"
	others         = folder + "nodes-others.csv"
	relationships  = folder + "relationships.csv"
	entities_rows = ReadCSV(entities, ['name'])
	exit = False
	while not exit:
		i = str(input(" [e] exit\n [s] search entitie name in entities leaks\n [g] grep filter in full leaks\n\t > "))
		if i == 'e':
			exit = True
		if i == 's':
			SearchEntitieName(entities_rows, str(input(" Search > ")))
		if i == 'g':
			entitie_name = str(input(" GREP filter > "))
			print("\nADDRESSES DATA : \n\t")
			GetCSVRowByName(addresses, entitie_name)
			print("\nENTITIES DATA : \n\t")
			GetCSVRowByName(entities, entitie_name)
			print("\nINTERMEDIARIES DATA : \n\t")
			GetCSVRowByName(intermediaries, entitie_name)
			print("\nOFFICERS DATA : \n\t")
			GetCSVRowByName(officers, entitie_name)
			print("\nOTHERS DATA : \n\t")
			GetCSVRowByName(others, entitie_name)
			print("\nRELATIONSHIPS DATA : \n\t")
			GetCSVRowByName(relationships, entitie_name)
	return 0

if __name__ == '__main__':
	main()
	exit()
