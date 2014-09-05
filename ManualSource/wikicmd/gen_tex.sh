#!/bin/sh

rm -rf tex

if [ ! -d wiki ]
then
	git clone git@github.com:SoarGroup/Soar.wiki.git wiki
else
	pushd wiki
	git fetch
	git checkout HEAD
	popd
fi

cp -R wiki/Manuals\ and\ FAQs/CLI/ CLI
mkdir tex

for f in CLI/cmd-*.md
do
	c=`basename $f | cut -c 5- | rev | cut -c 4- | rev`
	perl markdown.pl --html4tags $f > $f.html
	html2latex $f.html
	mv $f.tex $c.tex
	tf=$c.tex
	mv $tf tex/$tf || exit 1
done

# make sure every command listed on the wiki is included in the
# interface section of the manual

for f in tex/*
do
	f=`echo $f | awk -F. '{print $1}'`
	if ! grep -q "input{wikicmd/$f}" ../interface.tex
	then
		unused=1
		echo UNUSED: $f
	fi
done

rm -rf CLI wiki

if [ -n "$unused" ]
then
	exit 1
fi
