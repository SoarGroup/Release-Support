SoarManual
  type=copy
	out=Documentation/
	Documentation/pdf/SoarManual.pdf=top
SoarTutorial
	type=copy
	out=Documentation/
	Documentation/pdf/Soar Tutorial Part 1.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 2.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 3.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 4.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 5.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 6.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 7 - RL.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 8 - SMem.pdf=SoarTutorial
	Documentation/pdf/Soar Tutorial Part 9 - EpMem.pdf=SoarTutorial
SoarTutorial_9.3.3
  type=multiplatform-zip
  out=SoarSuite/
  # Missing: PythonCLI.py
	# Missing: TestPythonSML.py, (joseph will re-add)
	Compiled/VisualSoar/VisualSoar.jar=bin
	Compiled/COMPILE_DIR/out/libJava_sml_ClientInterface.DLL_EXTENSION=bin
	Compiled/COMPILE_DIR/out/libSoar.DLL_EXTENSION=bin
	Compiled/COMPILE_DIR/out/SoarJavaDebugger.jar=bin
	Compiled/COMPILE_DIR/out/java=bin/java
	Documentation/Agents_readme.txt=Agents/
	Documentation/pdf/Soar Tutorial Part 1.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 2.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 3.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 4.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 5.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 6.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 7 - RL.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 8 - SMem.pdf=Documentation
	Documentation/pdf/Soar Tutorial Part 9 - EpMem.pdf=Documentation
	Documentation/pdf/SoarManual.pdf=Documentation
SoarSuite_9.3.3-source
  type=zip
  out=SoarSuite/
  SoarSuite/Core=Core
  SoarSuite/Java=Java
  SoarSuite/scons=scons
  SoarSuite/TestCLI=TestCLI
  SoarSuite/Tests=Tests
  SoarSuite/build_lsb.sh=top
  SoarSuite/build.bat=top
  SoarSuite/SConstruct=top
  Release/Soar Agents.txt=Agents/
  Release/Soar Tutorial.txt=Documentation
  Documentation/pdf/SoarManual.pdf=Documentation
  Release/Building_Soar.txt=top
  Release/license.txt=top
  Release/Release_Notes_9.3.2.txt=Documentation
  Compiled/VisualSoar/VisualSoar.jar=bin
  Agents/default=Agents/default
