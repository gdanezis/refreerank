# refreerank
A project using the UK REF data sets to collaboratively re-rank the publishing venues in Computer Science

### Objective
The UK Research Excellence Framework (REF) that took place in 2014 was a peer-reviewed process that attempted to objectively rank UK Higher Education academic departments based on the quality of their research. Academic staff from each department were asked to submit their top four outputs from between 2009 and 2014 for peer review. The submitted pieces were reviewed -- at great expense (of time and money) -- and the departments were ranked based on the opinions of the reviewers. These submissions, as well as the outcomes, can be accessed from the [REF 2014 website](http://results.ref.ac.uk/DownloadSubmissions).

Despite being peer-reviewed, the REF process was not uncontroversial: A number of top UK scientists devoted a very large amount of time to evaluating the thousands of submitted works; the final judgments of quality depend on what is still a relatively small college of experts and may still contain biases; the task of selecting the experts to sit on [the expert panels](http://www.ref.ac.uk/panels/panelmembership/) implies a pre-existing judgment of research quality. The [final rankings produced](https://www.timeshighereducation.co.uk/sites/default/files/Attachments/2014/12/17/g/o/l/sub-14-01.pdf) were widely discussed.

*Was all of this expense necessary?*

We note that the in mere act of selecting papers for review, authors and institutions are inherently making a value judgment about the quality of their recent work. Thus, it can be assumed that, for any particular author, the works selected tend to be of a higher quality than works that they did not choose to include.

This selection enables us to perform an independent evaluation of publication venues, and hence academic institutions. By aggregating over the subjective quality decisions of tens of institutions and hundreds of authors, we create a participatory ranking system. We show that, when applied to the field of Computer Science, this peer-to-peer ranking reproduces some of the findings of the REF, whilst also creating some surprises.

### What we did
We matched the [works submitted for evaluation](http://results.ref.ac.uk/DownloadSubmissions/ByUoa/11) with publications recorded in the [dblp database](http://dblp.uni-trier.de/), an open-source aggregation of computer science research. From this database, we were also able to identify other published work that authors chose not to submit to the REF process. Based on the combination of these selected and unselected works, we evaluated various publication venues (conferences and journals) to see whether research presented at some venues was systematically selected by authors for inclusion in the REF submission over research that they presented in other (presumably less prestigious) venues.

From this evaluation, we made flow graphs describing researchers' quality judgments about different publication venues. Using these flow graphs, we constructed new departmental rankings based on the quality of their researchers' publication venues, as evaluated by their peers. As a side effect, we were able to visualize the connectivity of different research fields within Computer Science, identifying genuine areas of interdisciplinary research.


### Results

Peer12   | REF        | Peer4      | Peer All    | University
-------- | ---------- | ---------- | ----------- | -------------------------
**  0** (0.26) | ** +1**	(342) | ** +0**	(0.15) | ** +0**	(0.34) | **University College London**
**  1** (0.24) | ** +3**	(331) | ** +0**	(0.14) | ** +0**	(0.33) | **University of Oxford**
**  2** (0.22) | **+10**	(315) | ** +0**	(0.13) | ** +0**	(0.26) | **University of Edinburgh**
**  3** (0.16) | **+18**	(301) | ** +0**	(0.11) | ** +1**	(0.18) | **University of Nottingham**
**  4** (0.15) | ** -1**	(334) | ** +0**	(0.09) | ** -1**	(0.20) | **Imperial College London**
**  5** (0.12) | ** +0**	(325) | ** +2**	(0.07) | ** +2**	(0.14) | **King's College London**
**  6** (0.12) | **+27**	(290) | ** -1**	(0.08) | ** -1**	(0.17) | **University of Southampton**
**  7** (0.11) | **+22**	(295) | ** +1**	(0.07) | ** +1**	(0.13) | **University of Glasgow**
**  8** (0.10) | ** -1**	(319) | ** -2**	(0.07) | ** +2**	(0.12) | **University of Cambridge**
**  9** (0.10) | ** -7**	(335) | ** +2**	(0.06) | ** +0**	(0.13) | **University of Liverpool**
** 10** (0.10) | ** +8**	(305) | ** +3**	(0.05) | ** -4**	(0.14) | **Newcastle University**
** 11** (0.09) | ** +0**	(315) | ** -2**	(0.06) | ** +2**	(0.10) | **Lancaster University**
** 12** (0.09) | ** -4**	(319) | ** +0**	(0.06) | ** +0**	(0.11) | **University of Manchester**
** 13** (0.09) | ** +6**	(303) | ** -3**	(0.06) | ** -2**	(0.11) | **University of Birmingham**
** 14** (0.08) | ** +8**	(301) | ** +1**	(0.05) | ** +0**	(0.09) | **University of Bristol**
** 15** (0.07) | **+33**	(265) | ** -1**	(0.05) | ** +3**	(0.08) | **City University London**
** 16** (0.07) | ** +0**	(309) | ** +0**	(0.05) | ** +0**	(0.08) | **University of York**
** 17** (0.07) | **-17**	(346) | ** +2**	(0.04) | ** +0**	(0.08) | **University of Warwick**
** 18** (0.06) | ** -4**	(311) | ** -1**	(0.04) | ** +3**	(0.07) | **Swansea University**
** 19** (0.06) | **-10**	(318) | ** +3**	(0.04) | ** +0**	(0.07) | **Queen Mary University of London**
** 20** (0.06) | ** +8**	(297) | ** +5**	(0.04) | ** +3**	(0.06) | **Aberystwyth University**
** 21** (0.06) | **-11**	(316) | ** +0**	(0.04) | ** +1**	(0.07) | **Royal Holloway, University of London**
** 22** (0.05) | **+15**	(285) | ** -4**	(0.04) | ** +4**	(0.06) | **University of Bath**
** 23** (0.05) | **+16**	(283) | ** +1**	(0.04) | ** -3**	(0.07) | **Brunel University London**
** 24** (0.05) | **-11**	(314) | ** +3**	(0.04) | ** +4**	(0.05) | **University of St Andrews**
** 25** (0.05) | ** -2**	(301) | **+14**	(0.03) | **-10**	(0.09) | **Cardiff University**
** 26** (0.05) | **+10**	(289) | ** +0**	(0.04) | ** -1**	(0.06) | **Open University**
** 27** (0.05) | **-21**	(319) | ** +2**	(0.03) | ** -3**	(0.06) | **University of Sheffield**
** 28** (0.05) | ** -4**	(300) | ** -5**	(0.04) | ** +2**	(0.05) | **University of Leicester**
** 29** (0.05) | **+36**	(246) | ** -9**	(0.04) | ** +3**	(0.05) | **Middlesex University**
** 30** (0.05) | ** -5**	(299) | ** +3**	(0.03) | ** -3**	(0.06) | **University of Durham**
** 31** (0.05) | **+20**	(264) | ** -3**	(0.03) | ** -2**	(0.05) | **University of Ulster**
** 32** (0.04) | **-12**	(303) | ** +3**	(0.03) | ** -1**	(0.05) | **Birkbeck College**
** 33** (0.04) | ** -3**	(295) | ** -1**	(0.03) | ** +0**	(0.05) | **University of Leeds**
** 34** (0.04) | ** +4**	(284) | ** -3**	(0.03) | ** +2**	(0.05) | **University of Kent**
** 35** (0.04) | ** +9**	(271) | ** -5**	(0.03) | ** -1**	(0.05) | **Heriot-Watt University**
** 36** (0.04) | ** -2**	(290) | ** +1**	(0.03) | ** -1**	(0.05) | **University of Essex**
** 37** (0.04) | ** +4**	(276) | ** -3**	(0.03) | ** +2**	(0.04) | **University of Lincoln**
** 38** (0.03) | **+18**	(260) | ** +2**	(0.02) | ** +0**	(0.04) | **De Montfort University**
** 39** (0.03) | ** +1**	(277) | ** +3**	(0.02) | ** -2**	(0.04) | **Queen's University Belfast**
** 40** (0.03) | ** -5**	(290) | ** -4**	(0.03) | ** +2**	(0.03) | **University of Dundee**
** 41** (0.03) | **+14**	(261) | ** +0**	(0.02) | ** +3**	(0.03) | **University of Strathclyde**
** 42** (0.03) | **-10**	(293) | ** -4**	(0.03) | ** +3**	(0.03) | **University of Sussex**
** 43** (0.03) | **-12**	(293) | ** +3**	(0.02) | ** -3**	(0.04) | **University of Aberdeen**
** 44** (0.03) | **+23**	(244) | ** -1**	(0.02) | ** -3**	(0.03) | **University of Bedfordshire**
** 45** (0.03) | ** +7**	(264) | ** +2**	(0.02) | ** +1**	(0.03) | **University of Surrey**
** 46** (0.02) | **-19**	(297) | ** +4**	(0.02) | ** -3**	(0.03) | **Oxford Brookes University**
** 47** (0.02) | ** -1**	(269) | ** -3**	(0.02) | ** +1**	(0.03) | **University of Stirling**
** 48** (0.02) | ** -6**	(274) | ** +5**	(0.01) | ** +2**	(0.02) | **Teesside University**
** 49** (0.02) | **+25**	(230) | ** -4**	(0.02) | ** +2**	(0.02) | **Coventry University**
** 50** (0.02) | **+19**	(240) | ** +5**	(0.01) | ** -3**	(0.03) | **University of the West of Scotland**
** 51** (0.02) | **+15**	(245) | ** +0**	(0.01) | ** +2**	(0.02) | **Loughborough University**
** 52** (0.02) | **-35**	(307) | ** -4**	(0.02) | ** +3**	(0.02) | **University of East Anglia**
** 53** (0.02) | ** +5**	(258) | ** -4**	(0.02) | ** +5**	(0.02) | **Goldsmiths' College**
** 54** (0.02) | ** +9**	(248) | ** -2**	(0.01) | ** -2**	(0.02) | **University of Hertfordshire**
** 55** (0.02) | ** -6**	(264) | ** -1**	(0.01) | ** +2**	(0.02) | **Aston University**
** 56** (0.02) | **-13**	(273) | ** +3**	(0.01) | ** +0**	(0.02) | **University of Portsmouth**
** 57** (0.02) | **-42**	(310) | ** +0**	(0.01) | ** -3**	(0.02) | **University of Exeter**
** 58** (0.01) | ** +3**	(251) | ** +0**	(0.01) | ** +1**	(0.02) | **University of Huddersfield**
** 59** (0.01) | ** -9**	(264) | ** +2**	(0.01) | **-10**	(0.02) | **University of Northumbria at Newcastle**
** 60** (0.01) | ** +2**	(251) | ** -4**	(0.01) | ** +1**	(0.01) | **Glasgow Caledonian University**
** 61** (0.01) | ** -4**	(260) | ** -1**	(0.01) | ** +5**	(0.01) | **Kingston University**
** 62** (0.01) | **+10**	(234) | ** +2**	(0.01) | ** +3**	(0.01) | **Liverpool John Moores University**
** 63** (0.01) | **-18**	(270) | ** +2**	(0.01) | ** +1**	(0.01) | **University of the West of England, Bristol**
** 64** (0.01) | ** +4**	(241) | ** +5**	(0.01) | ** -1**	(0.01) | **Edinburgh Napier University**
** 65** (0.01) | **-11**	(262) | ** -3**	(0.01) | ** +4**	(0.01) | **Manchester Metropolitan University**
** 66** (0.01) | ** -6**	(252) | ** +1**	(0.01) | ** +1**	(0.01) | **University of Hull**
** 67** (0.01) | **-41**	(298) | ** +1**	(0.01) | ** -5**	(0.01) | **University of Plymouth**
** 68** (0.01) | ** +7**	(218) | ** -2**	(0.01) | ** +2**	(0.01) | **University of Westminster**
** 69** (0.01) | ** +1**	(240) | ** -6**	(0.01) | ** +2**	(0.01) | **University of Brighton**
** 70** (0.01) | **-23**	(267) | ** +0**	(0.01) | ** +2**	(0.01) | **Bangor University**
** 71** (0.01) | ** +0**	(235) | ** +0**	(0.01) | ** -3**	(0.01) | **University of Derby**
** 72** (0.01) | ** +4**	(216) | ** +0**	(0.01) | ** +1**	(0.01) | **Robert Gordon University**
** 73** (0.01) | ** +0**	(232) | ** +3**	(0.00) | **-13**	(0.02) | **Glynd?r University**
** 74** (0.01) | ** +4**	(214) | ** +1**	(0.00) | ** +1**	(0.01) | **University of Greenwich**


### How it works

### Datasets
[REF Submissions for Computer Science](http://results.ref.ac.uk/DownloadSubmissions/ByUoa/11)
[DBLP](http://dblp.uni-trier.de/faq/How+can+I+download+the+whole+dblp+dataset)
