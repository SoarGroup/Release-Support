_**In an effort to make the issues list focused on things that can get immediate attention and don't require re-design or major refactoring, I've moved some of the issues that we've classified as architectural suggestions or feature-requests here.   **_

***
**Jon Voight: Many kernel data structures are still in 32 bits that could be 64 bits, such as the hash tables. These things need to be moved to 64 bits.**

***
**Bob Marinier 2008-06-13: Removed duplicate SML names**

Some of the constants contained in sml::sml_Names (sml_Names.h in ConnectionSML) are redundant with constants contained in soar_TraceNames (soar_TraceNames.h in shared). These should be removed from sml_Names in order for it to be clear which constants are used by the kernel vs. the ones used exclusively by SML.

***

**Bob Marinier 2007-05-26: Make run non-blocking**

Currently, running Soar is a blocking call. Given the way we (at UM at least) typically design environments, Doug says it makes more sense for run to be non-blocking. Dave Ray points out, however, that in some cases blocking is better, and in the typical SoarTech case, running is asynchronous, so it doesn't matter much.

This kind of change would break existing code, so the possibilities include waiting until Soar9 (in which lots of stuff will break anyway), or to leave existing stuff the way it is and just introduce new methods that are non-blocking (so people have a choice). If it makes sense, the flexible route is probably best. I don't know if this interacts with the threading model stuff (bug 1001) at all.

From Douglas Pearson on May 27, 2007 01:52:34

I think if we allowed run to be non-blocking only in the case where there's a separate thread already running in the kernel it shouldn't be too hard to do.

Basically, if you're hard core (or use Tcl) you control the threads and deal with the blocking problems. If you want an easy life (but a bit slower) you let us take over the threading.

Which suggests making it an optional mode would be the way to go.

From Dave Ray on May 27, 2007 07:15:34

I think if you add some threading helper support as discussed in bug 1001, then this bug basically goes away. That is, leave run as a blocking call and providing non-blocking run support through the threading helper. I don't think there's any need to add any special modes to the run command or anything. Some considerations driving these conclusions:

To make run non-blocking, you have to have a dedicated thread which is a non-starter for Tcl-based systems. Having run block is really nice for building unit tests and batch runs where you want to create an agent, run it a few steps, and then do something else. We've done this quite a bit at SoarTech. That said, this may be a separate bug report, but it would be nice if the run control could tell give more details about which agents are currently running and provide the ability to add an agent to the set of running agents. It seems like it's pretty easy to naively cause a reentrant run call within a callback which the run control code doesn't seem to handle that well. A situation like
this:

run agent A
update event
run agent B
... weird things happen ...

***

**Bob Marinier 2007-10-28: add exec-like RHS function that automatically puts spaces between args**

When calling RHS functions, generally you would use either "cmd" (for calling Soar commands) or exec (for calling custom RHS functions). "cmd" automatically puts spaces between the arguments, but exec does not (because people might want to concatenate the args).

Dave Ray makes two points about exec: concatenating arguments is definitely the less common case, and there is already a concat RHS function that does this explicitly. I didn't even know there was a concat function (it's not documented; looking at the code, it appears to have been added by gSKI).

Changing exec now would be bad for compatibility reasons, so Dave and I agree that the best option is to introduce a new exec-like function that automatically puts the spaces between the args (this should result in cleaner Soar code, too). Dave suggests that, "in the great Unix tradition", this function be called execv.

From Dave Ray on October 28, 2007 14:00:27

That's funny. I didn't even know that concat was a gSKI thing. In any case, it's definitely useful.

I was partly joking by suggesting execv, but I can't really think of anything better that's still compact enough to not be annoying to type.

Also, I don't think that just putting spaces between the arguments will be sufficient for the general case. If any of the arguments have spaces in them, you've got problems. I'd suggest one of two approaches:

Expand the RHS function interface to allow for multiple arguments rather than the single pArgument we have now. They could come in as a vector of strings. This is what the original gSKI RHS function API did.

If the first approach requires too much fussing with the API, define a standard way to format the arguments, with escapes as necessary and provide an API function that knows how to parse them. Something like:

pArgument = "Argument with spaces", 33, "Argument with "quotes""

And then an API function something like this:

vector args = sml::ParseRhsArguments(pArgument) @ghost
     
From Douglas Pearson on October 28, 2007 22:50:05

That's a good point about handling arguments with embedded spaces. Another option rather than defining our own escape/parameter API would be to encode the arguments as XML and then pass the string form as the parameter. We already have all of the code for encoding and decoding available and this would give us even more extensibility than an array of strings for the long-term.

From Douglas Pearson on October 28, 2007 22:52:43

I meant to also say, we could still offer a method to parse the XML back as an array of strings -- so the client side could still just see it in that form.

***

**Bob Marinier 2006-05-22: Make java debugger context menu not block trace printing**

Start debugger
Load TOH
run
While running, right-click in trace window. Leave context menu up while
Soar runs.
When TOH completes, click somewhere to remove context menu.
Notice that the message "An agent halted during the run." doesn't get printed
until after the context menu is removed.

***

**_garfieldnate commented on Feb 20, 2015_: Switch Soar to use smart pointers**

Much of the code base is tangled together due to the extensive requirement of an agent* argument throughout most functions. One of the reasons this is so is because of the memory allocation mechanism used; the memory manager (mem.h/cpp) maintains separate memory pools for each agent, and each allocation requires specifying which agent's memory pool to use.

It would be nice if we could switch to something like smart pointers. Mazin tells me that @bluechill worked on this last year and ran into complications, so he could explain what the ramifications/difficulties with switching to this approach are. @marinier Member marinier commented on Feb 20, 2015 The memory pools are critical to Soar's performance. Try testing with them disabled -- when I did this several years ago, I saw a 50% drop in performance. Memory pools allow Soar to avoid making lots of system calls to get memory, and it turns out that makes a huge difference.

That said, if you could tie a smart pointer mechanism to the memory pools, so devs didn't have to track the reference counts but we still got the performance gains, then that would be worthwhile. Note, however, that even in jsoar we need to use reference counts for many objects (although not as many as csoar) because some objects get trapped in lists and thus will always have a reference -- the reference counts indicate when these objects should be removed from these lists.

On Fri, Feb 20, 2015 at 1:42 AM, Nathan Glenn:

Much of the code base is tangled together due to the extensive requirement of an agent* argument throughout most functions. One of the reasons this is so is because of the memory allocation mechanism used; the memory manager (mem.h/cpp) maintains separate memory pools for each agent, and each allocation requires specifying which agent's memory pool to use.

It would be nice if we could switch to something like smart pointers. Mazin tells me that @bluechill worked on this last year and ran into complications, so he could explain what the ramifications/difficulties with switching to this approach are.
 
marinier commented on Feb 20, 2015:

So, I think you misunderstand the performance implications. The memory pools maintain pointers to blocks of memory that have already been obtained from the OS, so Soar can reuse these for future objects without having to do a malloc. It's the difference between doing a system call (malloc) and an array lookup -- a huge performance difference. And it turns out that Soar allocates and releases lots of objects, so avoiding all of the overhead of malloc/free makes a big difference.

That said, maybe smart pointers can be configured to use the memory pools. It is possible to configure most STL containers to use them, for example (Soar does this in some of the newer stuff). The configuration involves very ugly template definitions of the container objects. The only restriction is that the container has to always ask for objects of the same size (vectors do not do this, and thus can't use Soar memory pools -- but that's the only one I can think of that someone tried to use and didn't work).

Bob

On Fri, Feb 20, 2015 at 8:57 AM, Alex T. wrote:

So I did try to get a version running with smart pointers last year so we could see performance differences. Theoretically it shouldn't be a hit to performance because of how smart pointers work (they're reference counts internally) but what I ran into was that we use so many C style objects that in order to covert to smart pointers one basically needs to rewrite the RETE. If you dig into the code base you'll see weird casts to void* and back with our pointers and you can't do that with smart pointers without losing their functionality. So if someone was willing to convert Soar to not do that, smart pointers would be really nice and easy to do. But that is a big thing to try and do. I couldn't ever make it work. I might still have a version sort of working but there was a lot of memory problems because of that.

garfieldnate commented on Feb 20, 2015:

How about the implications of not having separate pools for each agent? Would this slow down threading or anything? @garfieldnate Member garfieldnate commented on Feb 20, 2015 I wonder if it would be possible to just implement the memory manager to have one pool per thread. That would eliminate the need to pass the agent around everywhere for allocating. @marinier Member marinier commented on Feb 21, 2015 I'm not sure what threads you are referring to -- there is only one thread for all agents in csoar (jsoar supports a separate thread for each agent). I guess the biggest issue of using a single unified set of pools (to be clear -- there are separate pools for each object type within each agent) is memory recovery. As it is set up now, pools can only grow, never shrink. But destroying an agent would free all of its pools. If there was only one set of pools for all agents, then memory could not be recovered by destroying an agent. That said, this is an unusual edge case that I don't recall ever coming up -- most systems are not creating and destroying lots of agents while running. Of course, the memory pools could be redesigned to allow for shrinkage, but I suspect this is difficult.

On Fri, Feb 20, 2015 at 10:10 PM, Nathan Glenn wrote:

I wonder if it would be possible to just implement the memory manager to have one pool per thread. That would eliminate the need to pass the agent around everywhere for allocating.


garfieldnate commented on Feb 21, 2015:

Good to know. I didn't realize there were no threads, but I think they are still good to keep in mind if we update how memory works.

It looks like smart pointers can be used with memory pools just fine. You just provide your allocate/delete methods in the constructor:

std::shared_ptr<MyClass> ptr(CreateMyObject(....), DeleteMyObject); @marinier Member marinier commented on Feb 21, 2015 Sounds like it may be worth trying, then. I recommend looking at where jsoar was able to eliminate reference counts and start there -- Symbols seem like the most obvious win.

On Sat, Feb 21, 2015 at 9:34 AM, Nathan Glenn wrote:

Good to know. I didn't realize there were no threads, but I think they are still good to keep in mind if we update how memory works.

It looks like smart pointers can be used with memory pools just fine. You just provide your allocate/delete methods in the constructor:

std::shared_ptr ptr(CreateMyObject(....), DeleteMyObject);


garfieldnate commented on Feb 21, 2015:

Hmm, symbols already use reference counting, so they're a natural place to start. This cracked me up a little: I can't remember all the places I add reference counts to symbols. Here's a bunch I can remember though. @garfieldnate Member garfieldnate commented on Feb 24, 2015 Recent changes in 9.5 have lead to some memory leaks and performance changes that must be cleaned up. Until memory management is stable and clean, this issue will be on hold. 

Mazin commented on Sep 28, 2016:

I did make a memory-agnostic memory manager about 1.5 years ago and a lot of stuff has been refactored out of the agent struct, but the agent pointer is still required nearly everywhere because of other dependencies. I'll change this to a request to switching to use smart pointers, since there's some useful info here about that, and it is a capability that we could get a lot of mileage out of, given the tangled nature of Soar.