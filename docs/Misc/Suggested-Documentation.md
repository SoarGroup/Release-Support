_**In an effort to make the issues list focused on things that can get immediate attention and don't require re-design or major refactoring, I've moved some of the issues that we've classified as documentation requests here.   **_

***
Bob Marinier 2006-01-26:  It seems clear that one of the reasons people get burned by the GDS is because they don't even know it exists, much less the constraints it places on good programming practices. This is because the only mention of it in the manual is in an appendix, and there is no tutorial on it.

I think it would be a good idea to add a short tutorial on th GDS to the current tutorials. It could be based on a simple counting example to demonstrate thepotential pitfalls and how to debug problems when you run into them. Karen also suggested doing something with the water-jug-look-ahead code, since it's a good example of why one would want to create o-supported structures in substates and how to properly do it.

It would be great if this tutorial was written in time for the Soar workshop, since then we could give an advanced tutorial on it.

***
bluechill commented on May 21, 2015:  We need better documentation on how to handle soar init in SML applications

```
On the Lego Mindstorms Domain agents if you do the following:

Run the agent
Stop the agent
Initialize Soar via init-soar
Source in the rules again (may not be necessary)
Run it again
You will run into a Soar bug which is because an assertion fails

trying to print m_Agent fails by trying to dereference invalid memory. parent is valid.

Backtrace:

(lldb) bt
* thread #2: tid = 0x45812f, 0x0000000100488caf libSoar.dylib`sml::WorkingMemory::CreateStringWME(this=0x0000000000000028, parent=0x0000000100d103e0, pAttribute=0x000000010003754c, pValue=0x0000000100037553) + 31 at sml_ClientWorkingMemory.cpp:840, stop reason = EXC_BAD_ACCESS (code=1, address=0x38)
  * frame #0: 0x0000000100488caf libSoar.dylib`sml::WorkingMemory::CreateStringWME(this=0x0000000000000028, parent=0x0000000100d103e0, pAttribute=0x000000010003754c, pValue=0x0000000100037553) + 31 at sml_ClientWorkingMemory.cpp:840
    frame #1: 0x00000001004948c9 libSoar.dylib`sml::Identifier::CreateStringWME(this=0x0000000100d103e0, pAttribute=0x000000010003754c, pValue=0x0000000100037553) + 57 at sml_ClientIdentifier.cpp:448
    frame #2: 0x00000001000082d1 soar_client`RemoteSoarCommunicator::inputPhaseCallback(this=0x00007fff5fbef8d0) + 641 at RemoteSoarCommunicator.cpp:135
    frame #3: 0x0000000100009065 soar_client`SoarManager::runEventHandler(eventID=smlEVENT_AFTER_OUTPUT_PHASE, data=0x00007fff5fbeef30, agent=0x0000000100d0f400, phase=sml_OUTPUT_PHASE) + 101 at SoarManager.cpp:114
    frame #4: 0x0000000100484c63 libSoar.dylib`sml::Agent::ReceivedRunEvent(this=0x0000000100d0f400, id=smlEVENT_AFTER_OUTPUT_PHASE, pIncoming=0x0000000101880b70, (null)=0x0000000100f0e3c0) + 643 at sml_ClientAgent.cpp:144
    frame #5: 0x00000001004848fb libSoar.dylib`sml::Agent::ReceivedEvent(this=0x0000000100d0f400, pIncoming=0x0000000101880b70, pResponse=0x0000000100f0e3c0) + 139 at sml_ClientAgent.cpp:106
    frame #6: 0x0000000100496bc9 libSoar.dylib`sml::Kernel::ProcessIncomingSML(this=0x0000000100d0cdf0, pConnection=0x0000000100d06d40, pIncomingMsg=0x0000000100f0c8e0) + 729 at sml_ClientKernel.cpp:452
    frame #7: 0x00000001004968dd libSoar.dylib`sml::Kernel::ReceivedCall(pConnection=0x0000000100d06d40, pIncoming=0x0000000100f0c8e0, pUserData=0x0000000100d0cdf0) + 45 at sml_ClientKernel.cpp:335
    frame #8: 0x00000001005181e3 libSoar.dylib`sml::Callback::Invoke(this=0x0000000100d0efe0, pIncomingMessage=0x0000000100f0c8e0) + 51 at sml_Connection.h:114
    frame #9: 0x000000010050a7b0 libSoar.dylib`sml::Connection::InvokeCallbacks(this=0x0000000100d06d40, pIncomingMsg=0x0000000100f0c8e0) + 688 at sml_Connection.cpp:451
    frame #10: 0x000000010050dbac libSoar.dylib`sml::EmbeddedConnectionAsynch::ReceiveMessages(this=0x0000000100d06d40, allMessages=true) + 124 at sml_EmbeddedConnectionAsynch.cpp:331
    frame #11: 0x000000010050e989 libSoar.dylib`sml::EventThread::Run(this=0x0000000100d0d210) + 121 at sml_EventThread.cpp:79
    frame #12: 0x0000000100515b1e libSoar.dylib`ThreadStartFunction(pThreadObject=0x0000000100d0d210) + 30 at thread_Thread.cpp:25
    frame #13: 0x0000000100515ad0 libSoar.dylib`LinuxThreadFunc(thread_args=0x0000000100d0efd0) + 48 at thread_OSspecific.cpp:105
    frame #14: 0x00007fff92a2b268 libsystem_pthread.dylib`_pthread_body + 131
    frame #15: 0x00007fff92a2b1e5 libsystem_pthread.dylib`_pthread_start + 176
    frame #16: 0x00007fff92a2941d libsystem_pthread.dylib`thread_start + 13

This seems like this might be cause by keeping around sml::Identifiers etc. outside of SML and then using them after a reinit. If so, we should either change SML to not allow that or make it very clear that that is the cause of the issue (if, indeed, it is).
```

Mazin commented on Sep 28, 2016: 

Yes, I think that is indeed the case. I believe Nate faced this issue with SimpleEaters as well. The environment needs to register for reinit events to make sure it keeps its aborts anything pending that might now have stale symbols.