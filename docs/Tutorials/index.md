# The Soar 9 Tutorial

John E. Laird

University of Michigan

July 19, 2017

Updated for Soar 9.6.0

## Acknowledgments

This tutorial is the culmination of work by many people, and has been
refined and expanded significantly over several years. 

Below we recognize the individuals who have contributed to the Soar
Tutorial:

- Soar:  Mazin Assanie, Karen Coulter, Nate Derbinsky, Randy Jones, Bob
- Wray, Joseph Xu  
- Soar Debugger:  Mazin Assanie, Doug Pearson  
- Eaters:  Mazin Assanie, Clare Bates Congdon, Randy Jones, Scott
- Wallace, Jonathan Voigt  
- Tanksoar:  Mazin Assanie, John Duchi, Mike van Lent, Jonathan Voigt  
- Visual Soar:  Brian Harleton, Brad Jones , Andrew Nuxoll  
- Documentation and other Tools:  Mazin Assanie, Clare Bates Congdon,
- Karen Coulter, Taylor Lafrinere, Bob Marinier, Alex Roper, Jonathan
- Voigt  

## Introduction

This is a guide for learning to create software agents in Soar, version
9. It assumes no prior knowledge of Soar or computer programming.

The goals of this document are:

  - Introduce you to the basic operating principles of Soar.
  - Teach you how to run Soar programs and understand what they do.
  - Teach you how to write your own Soar programs.

This is about the nuts and bolts of writing Soar programs, but not about
the theory behind Soar. For that, you should read Chapter 2 and 3 of the
Soar Manual or the Gentle Introduction to Soar: 2006 Update.

This tutorial takes the form of a sequence of lessons. Each lesson
introduces concepts one by one and gives you a chance to use them by
creating Soar agents. Each lesson builds on the previous ones, so it is
important to go through them in order. To make the best use of this
tutorial, we recommend that you read the tutorial, do the exercises, run
the programs, and write your own Soar agents. The programs are available
as part of the tutorial installation. Please use the most recent
version. Although the tutorial is long, you should be able to work
through it quickly.

What is Soar? We call Soar a unified architecture for developing
intelligent systems. That is, Soar provides the fixed computational
structures in which knowledge can be encoded and used to produce action
in pursuit of goals. In many ways, it is like a programming language,
albeit a specialized one. It differs from other programming languages in
that it has embedded in it a specific theory of the appropriate
primitives underlying reasoning, learning, planning, and other
capabilities that we hypothesize are necessary for intelligent behavior.
Soar is not an attempt to create a general purpose programming language.
You will undoubtedly discover that some computations are difficult or
awkward to do in Soar (such as complex math) and they are more
appropriately encoded in a programming language such as C, C++, or Java.
Our hypothesis is that Soar is appropriate for building autonomous
agents that use large bodies of knowledge to generate action in pursuit
of goals.

The tutorial comes in six parts. Part I introduces Soar using a simple
puzzle task called the Water Jug to introduce the basic concepts of
Soar. This is the classic type of toy problem that people in AI now rail
against as being completely unrepresentative of real world problems.
Maybe true, but it is simple and easy to understand. After working
through Part I, you should be able to write simple Soar programs. Part
II uses a Pac-man like game called Eaters to introduce interaction with
external environments. Part III uses a grid-based tank game called
Tank-Soar and introduces Soar’s subgoaling mechanism as it is used for
task decomposition. Part IV uses Missionaries and Cannibals problems to
further explore internal problem solving and search. Part V uses
Missionaries and Cannibals along with the Water Jug to introduce
look-ahead planning and procedural learning. Part VI is a tutorial that
explores the basics of Soar’s reinforcement learning mechanism. Part VII
is a short tutorial on the basics of using Soar’s long-term semantic
memory system. And finally part VIII discusses how to use Soar’s
episodic memory system.

Soar has its own editor, called VisualSoar, which we highly recommended
for use in developing Soar programs. VisualSoar is part of the standard
installation and is also available from the Soar homepage.
