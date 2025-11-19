#!/usr/bin/bash
#First you check if the directory exists and if not you create the archives directory
if [ ! -d "archives" ]; then
    mkdir -p archives
fi
#search for all files that have been created with the format expenses_date.txt so that we can move them
for file in expenses_*.txt; do
    if [ -f "$file" ]; then
        mv "$file" archives/
        sleep 0.5
        echo "======================KUDOS! MISSION SUCCESSFULL======================"
        echo "Expense files moved to the archive folder successfully"
        echo "---------------------------------------------------------------------"
        echo "To view expences from an archived file: Run ./archive_expenses.sh date "
        echo "Where date is the date of that archived file"
        echo ""
        echo "=====================THANK YOU & GOOD BYE=============================="
    fi
done
#create a way to display info when someone searches using date in the archive file
TIMESTAMP=$(date '+%Y-%m-%d')
echo "[$TIMESTAMP] Archived all expense files." >> archive_log.txt

if [ $# -eq 1 ]; then
    SEARCH_DATE="$1"
    if [ -f "archives/expenses_$SEARCH_DATE.txt" ]; then
        cat "archives/expenses_$SEARCH_DATE.txt"
    fi
fi
