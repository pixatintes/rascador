#!/bin/sh

Answer=`zenity --entry --title="Grata laBsk" --text="Paraula clau a buscar:" --entry-text "gmt"`

VALUE=`zenity --scale --text="Pàgines a buscar:" --value="1" --min-value="1" --max-value="25" –step="1"`

order="python3 grataBSK_5_main.0.py $Answer $VALUE"
echo $order

python3 grataBSK_5_main.0.py $Answer $VALUE > r.txt
cat r.txt
RESULT=`cat r.txt`
firefox $RESULT
rm r.txt


