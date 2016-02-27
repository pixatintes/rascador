#!/bin/sh

#$list=`zenity --list --editable --print-column=ALL --checklist --separator=, --column=key --column=value --print-column=value  000 gmt 001 colditz 002 churchill 003 - 004 -`

#ans=$(zenity  --list  --text "Is linux.byexamples.com helpful?" --checklist  --column "Pick" --column "Opinion" TRUE Amazing FALSE Average FALSE "Difficult to follow" FALSE "Not helpful"); echo $ans

#echo $ans > l.txt

#Answer=`zenity --entry --title="Grata laBsk" --text="Paraula clau a buscar:" --entry-text "gmt"`

#VALUE=`zenity --scale --text="Pàgines a buscar:" --value="1" --min-value="1" --max-value="25" –step="1"`

#order="python3 grataBSK_5_main.py $Answer $VALUE"
order="python3 grataBSK_5_main_2.py"
echo $order
$order > r.txt
RESULT=`cat r.txt`
#firefox $RESULT

./send-email.py "Busqueda diaria laBsk" r.txt

rm r.txt

