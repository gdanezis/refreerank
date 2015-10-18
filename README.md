# refreerank
A project using the UK REF data sets to collaboratively re-rank the publishing venues in Computer Science

### Objective
The UK Research Excellence Framework (REF) that took place in 2014 was a peer-reviewed process that attempted to objectively rank UK Higher Education academic departments based on the quality of their research. Academic staff from each department were asked to submit their top four outputs from between 2009 and 2014 for peer review. The submitted pieces were reviewed -- at great expense (of time and money) -- and the departments were ranked based on the opinions of the reviewers. These submissions, as well as the outcomes, can be accessed from the [REF 2014 website](http://results.ref.ac.uk/DownloadSubmissions).

Despite being peer-reviewed, the REF process was not uncontroversial: A number of top UK scientists devoted a very large amount of time to evaluating the thousands of submitted works; the final judgments of quality depend on what is still a relatively small college of experts and may still contain biases; the task of selecting the experts to sit on [the expert panels](http://www.ref.ac.uk/panels/panelmembership/) implies a pre-existing judgment of research quality. The [final rankings produced](https://www.timeshighereducation.co.uk/sites/default/files/Attachments/2014/12/17/g/o/l/sub-14-01.pdf) were widely discussed.

*Was all of this expense necessary?*

We note that the in mere act of selecting papers for review, authors and institutions are inherently making a value judgment about the quality of their recent work. Thus, it can be assumed that, for any particular author, the works selected tend to be of a higher quality than works that they did not choose to include.

This selection enables us to perform an independent evaluation of publication venues, and hence academic institutions. By aggregating over the subjective quality decisions of tens of institutions and hundreds of authors, we create a participatory ranking system. We show that, when applied to the field of Computer Science, this peer-to-peer ranking reproduces some of the findings of the REF, whilst also creating some surprises.

### What we did
We matched the [works submitted for evaluation](http://results.ref.ac.uk/DownloadSubmissions/ByUoa/11) with publications recorded in the [dblp database](http://dblp.uni-trier.de/), an open-source record of computer science publications, using [custom fuzzy matching techniques](https://github.com/gdanezis/refreerank/blob/master/matchauthors.py). From this database, we were also able to identify other published work that authors chose not to submit to the REF process between 2008 and 2014. Based on the combination of these selected and unselected works, we evaluated various publication venues (conferences and journals) to see whether research presented at some venues was systematically selected by authors for inclusion in the REF submission over research that they presented in other (presumably less prestigious) venues.

To estimate the venue quality, we made flow graphs describing researchers' quality judgments about different publication venues: given a set of selected and unselected publications at specific venues, we build a directed graph from all the venues of unselected papers to all the venues of selected ones. We then compute the stationary distribution of this directed graph, representing the probability of reaching a venue after a large number of steps in this graph. Heuristically, the steps follow the subjective quality judgments and high quality venues are more likely to be reached.

Once we estimate a quality score for venues we use them as proxies for judging the quality of research per department: for each author put forward we chose their best 12 papers evaluated by venue, and aggregate their score into the score of the institution. We experimented with selecting the top-4 or even all papers, without any major effect on most rankings. We call this the _Peer Score_, and the resulting ranking the _Peer Rank_. We publish the [full procedure for computing them](https://github.com/gdanezis/refreerank/blob/master/extractUKdblp.py).

### Results

The following table summarizes the _Peer Rank_ and _Peer Score_ of the top-75 UK Computer Science departments. We also compare the Peer Rank with the REF Output rank, and provide the difference in ranks. We observe some departments are not majorly re-ranked, while others see their position change significantly.

Peer Rank (Score)   | REF Rank (Diff.)   | Computer Science Department
-------- | ---------- | ----------------------------------------------
1 (0.26) | 2 (+1) | University College London
2 (0.24) | 5 (+3) | University of Oxford
3 (0.22) | 13 (+10) | University of Edinburgh
4 (0.16) | 22 (+18) | University of Nottingham
5 (0.15) | 4 (-1) | Imperial College London
6 (0.12) | 6 (+0) | King's College London
7 (0.12) | 34 (+27) | University of Southampton
8 (0.11) | 30 (+22) | University of Glasgow
9 (0.10) | 8 (-1) | University of Cambridge
10 (0.10) | 3 (-7) | University of Liverpool
11 (0.10) | 19 (+8) | Newcastle University
12 (0.09) | 12 (+0) | Lancaster University
13 (0.09) | 9 (-4) | University of Manchester
14 (0.09) | 20 (+6) | University of Birmingham
15 (0.08) | 23 (+8) | University of Bristol
16 (0.07) | 49 (+33) | City University London
17 (0.07) | 17 (+0) | University of York
18 (0.07) | 1 (-17) | University of Warwick
19 (0.06) | 15 (-4) | Swansea University
20 (0.06) | 10 (-10) | Queen Mary University of London
21 (0.06) | 29 (+8) | Aberystwyth University
22 (0.06) | 11 (-11) | Royal Holloway, University of London
23 (0.05) | 38 (+15) | University of Bath
24 (0.05) | 40 (+16) | Brunel University London
25 (0.05) | 14 (-11) | University of St Andrews
26 (0.05) | 24 (-2) | Cardiff University
27 (0.05) | 37 (+10) | Open University
28 (0.05) | 7 (-21) | University of Sheffield
29 (0.05) | 25 (-4) | University of Leicester
30 (0.05) | 66 (+36) | Middlesex University
31 (0.05) | 26 (-5) | University of Durham
32 (0.05) | 52 (+20) | University of Ulster
33 (0.04) | 21 (-12) | Birkbeck College
34 (0.04) | 31 (-3) | University of Leeds
35 (0.04) | 39 (+4) | University of Kent
36 (0.04) | 45 (+9) | Heriot-Watt University
37 (0.04) | 35 (-2) | University of Essex
38 (0.04) | 42 (+4) | University of Lincoln
39 (0.03) | 57 (+18) | De Montfort University
40 (0.03) | 41 (+1) | Queen's University Belfast
41 (0.03) | 36 (-5) | University of Dundee
42 (0.03) | 56 (+14) | University of Strathclyde
43 (0.03) | 33 (-10) | University of Sussex
44 (0.03) | 32 (-12) | University of Aberdeen
45 (0.03) | 68 (+23) | University of Bedfordshire
46 (0.03) | 53 (+7) | University of Surrey
47 (0.02) | 28 (-19) | Oxford Brookes University
48 (0.02) | 47 (-1) | University of Stirling
49 (0.02) | 43 (-6) | Teesside University
50 (0.02) | 75 (+25) | Coventry University
51 (0.02) | 70 (+19) | University of the West of Scotland
52 (0.02) | 67 (+15) | Loughborough University
53 (0.02) | 18 (-35) | University of East Anglia
54 (0.02) | 59 (+5) | Goldsmiths' College
55 (0.02) | 64 (+9) | University of Hertfordshire
56 (0.02) | 50 (-6) | Aston University
57 (0.02) | 44 (-13) | University of Portsmouth
58 (0.02) | 16 (-42) | University of Exeter
59 (0.01) | 62 (+3) | University of Huddersfield
60 (0.01) | 51 (-9) | University of Northumbria at Newcastle
61 (0.01) | 63 (+2) | Glasgow Caledonian University
62 (0.01) | 58 (-4) | Kingston University
63 (0.01) | 73 (+10) | Liverpool John Moores University
64 (0.01) | 46 (-18) | University of the West of England, Bristol
65 (0.01) | 69 (+4) | Edinburgh Napier University
66 (0.01) | 55 (-11) | Manchester Metropolitan University
67 (0.01) | 61 (-6) | University of Hull
68 (0.01) | 27 (-41) | University of Plymouth
69 (0.01) | 76 (+7) | University of Westminster
70 (0.01) | 71 (+1) | University of Brighton
71 (0.01) | 48 (-23) | Bangor University
72 (0.01) | 72 (+0) | University of Derby
73 (0.01) | 77 (+4) | Robert Gordon University
74 (0.01) | 74 (+0) | Glynd?r University
75 (0.01) | 79 (+4) | University of Greenwich


### How it works

### Datasets
[REF Submissions for Computer Science](http://results.ref.ac.uk/DownloadSubmissions/ByUoa/11)
[DBLP](http://dblp.uni-trier.de/faq/How+can+I+download+the+whole+dblp+dataset)
