#!/bin/bash

echo "Generating Soar CLI latex files. (../cli_help.cpp)"

rm -rf tex
mkdir tex

echo "Downloading wiki files from repository..."

git clone https://github.com/SoarGroup/Soar.wiki.git

echo "Converting to html..."

for file in Soar.wiki/ManualsAndFAQs/CLI/cmd_*.md; do
	base=`basename $file`
	stripped=${base%.*}
	stripped=${stripped#cmd_}
	stripped=${stripped//_/-}

	pandoc $file -f gfm -t latex -o tex/$stripped.tex
    python3 soarman_format.py tex/$stripped.tex
	sed -i 's/\[c\]{@{}llll@{}}/{@{\\extracolsep{\\fill}}llll@{}}/g' tex/$stripped.tex
	sed -i 's/\[c\]{@{}lll@{}}/{@{\\extracolsep{\\fill}}lll@{}}/g' tex/$stripped.tex
	sed -i 's/\[c\]{@{}ll@{}}/{@{\\extracolsep{\\fill}}ll@{}}/g' tex/$stripped.tex
	#sed -i 's/@{}llll@{}/@{}p{4cm}p{6cm}p{4cm}p{2cm}@{}/g' tex/$stripped.tex
	#sed -i 's/@{}lll@{}/@{}p{3cm}p{5cm}p{8cm}@{}/g' tex/$stripped.tex
	#sed -i 's/@{}ll@{}/@{}p{8cm}p{8cm}@{}/g' tex/$stripped.tex
done

# make sure every command listed on the wiki is included in the
# interface section of the manual

echo "Making sure every command listed on the wiki is included in the interface section of the manual..."

for f in tex/*
do
	f=${f%.*}
	if ! grep -q "input{wikicmd/$f}" ../interface.tex
	then
		unused=1
		echo UNUSED: $f
	fi
done

echo "Cleaning up..."
rm -rf Soar.wiki

if [ -n "$unused" ]
then
    echo "Unused file $n found.  Make sure it is in interface.tex.\nFailed to generate all CLI latex files."
	exit 1
fi

echo "Successfully generated CLI latex files from wiki entries!"
