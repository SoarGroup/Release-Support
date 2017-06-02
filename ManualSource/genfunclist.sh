rm -f funclist.tex

for f in wikicmd/tex/*
do
	cmd=`echo $f | awk -F[./] '{print $3}'`
	awk '
		function get_summary(filename)
		{
			if (filename == "alias") return "Controls aliases for Soar procedures."
			else if (filename == "chunk") return "Controls parameters for chunking."
			else if (filename == "debug") return "Accesses Soar’s internals."
			else if (filename == "decide") return "Controls operator-selection settings."
			else if (filename == "echo") return "Echoes arguments to the output stream."
			else if (filename == "epmem") return "Controls behavior of episodic memory."
			else if (filename == "explain") return "Explores how rules were learned."
			else if (filename == "gp") return "Defines a production template."
			else if (filename == "help") return "Gets information about Soar commands."
			else if (filename == "load") return "Loads files and libraries."
			else if (filename == "output") return "Controls Soar output settings."
			else if (filename == "preferences") return "Examines WME support."
			else if (filename == "print") return "Prints items in working or production memory."
			else if (filename == "production") return "Manipulates or analyzes Soar rules."
			else if (filename == "rl") return "Controls RL preference update settings."
			else if (filename == "run") return "Begins Soar’s execution cycle."
			else if (filename == "save") return "Saves various aspects of Soar memory."
			else if (filename == "smem") return "Controls behavior of semantic memory."
			else if (filename == "soar") return "Controls settings for running Soar."
			else if (filename == "sp") return "Defines a Soar production."
			else if (filename == "stats") return "Prints information on Soar agent statistics."
			else if (filename == "svs") return "Controls behavior of the Spatial Visual System."
			else if (filename == "trace") return "Controls the run-time tracing of Soar."
			else if (filename == "visualize") return "Creates visualizations of memory or processing."
			else if (filename == "wm") return "Controls settings related to working memory."
			else return ""
		}
		BEGIN {cmd="'$cmd'"}
		/^\\index/ {
			insummary=1; next 
		}
		/^\\subsubsection/ { 
			if (cmd != "file-system")
				printf("\\soar{%s} & %s & \\pageref{%s} \\\\\n", cmd, get_summary(cmd), cmd)
			exit
		}
		insummary == 1 {
			s = s " " $0
		}
	' $f >>funclist.tex
done

