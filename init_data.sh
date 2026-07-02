#!/bin/bash

actual_user="$(whoami)"
if [[ $actual_user == "root" ]]; then
    echo "Warning, you are logged in root !"
    passed=0
    while [[ $passed == 0 ]]; do
        read -p "Do you want to continue ? (y/N) " doContinue
        if [ "$doContinue" = "y" -o "$doContinue" = "Y" ]
        then
            passed=1
        elif [ "$doContinue" = "n" -o "$doContinue" = "N" -o "$doContinue" = "" ]
        then
            exit 1
        fi
    done

fi

passed2=0
while [[ $passed2 == 0 ]]; do
    read -p "You will download offshore leaks, it require something like 700 Mo, de you want to continue ? (y/N) " doContinue2
    if [ "$doContinue2" = "y" -o "$doContinue2" = "Y" ]
    then
        passed2=1
    elif [ "$doContinue2" = "n" -o "$doContinue2" = "N" -o "$doContinue2" = "" ]
    then
        exit 1
    fi
done

echo "downloading offshore leaks..."
wget https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip -o ./Rscs/offshores/data.zip
echo "extracting data..."
unzip -d ./Rscs/offshores/ ./Rscs/offshores/data.zip
echo "done"
