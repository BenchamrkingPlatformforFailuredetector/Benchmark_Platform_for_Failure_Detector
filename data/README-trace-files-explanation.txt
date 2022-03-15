==== Receptions Log (traceX.log) ====

Each traceX  file keeps track of the receptions on a single node X, along the 
following format: 
	<site> <numseq> <timestamp send> <timestamp receive> <hops>
Say that file trace0.log contains a line: 
	7 1 10965460869347846 2439202704391108 14
This tells that node 0 received a second heartbeat (counter starts at 0) from 
node 7 at time 2439202704391108 according to the local clock of node 0.
It also tells that node 7 sent its heartbeat #1 to node 0 at 10965460869347846 
(local clock of N7) and that 14 hops were required to reach the destination.



==== Emissions Logs (sentintervalX.log and sentX.log) ====

Each couple of files sentintervalX and sentX keep track of the heartbeat 
emissions from a single node X.

sentintervalX files list the time intervals corresponding to the emission of 
every heartbeat from a single node X to all the other nodes, along the following 
format:
	<numseq> <timestamp start send> <timestamp end send>
For instance, consider the following line in sentinterval0.log: 
	0 2439202316247486 2439202316394754
This means that, according to its local clock, node 0 called the function for 
sending its heartbeat #0 to all the other nodes at time 2439202316247486 and 
the call returned at time 2439202316394754.


sentX files list all of the heartbeat emission dates from a single node X, along 
the following format:
	<site> <numseq> <timestamp send>
For instance, consider the following line in sent0.log: 
	7 1 2439202416433527
This means that, according to its local clock, node 0 sent its heartbeat #1 to 
node 7 at time 2439202416433527.



==== List of Nodes ====

Below is the list of PlanetLab nodes on which these traces were collected:
ple4.ipv6.lip6.fr (France)
planetlab1.jhu.edu (USA, Maryland)
planetlab2.csuohio.edu (USA, Ohio)
75-130-96-12.static.oxfr.ma.charter.com (USA, Massachussets)
planetlab1.cnis.nyit.edu (USA, New York)
saturn.planetlab.carleton.ca (Canada, Ontario)
planetlab-03.cs.princeton.edu (USA, New Jersey)
prata.mimuw.edu.pl (Poland)
planetlab3.upc.es (Spain)
pl1.eng.monash.edu.au (Australia)