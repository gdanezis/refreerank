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

### How it works

### Datasets
[REF Submissions for Computer Science](http://results.ref.ac.uk/DownloadSubmissions/ByUoa/11)
[DBLP](http://dblp.uni-trier.de/faq/How+can+I+download+the+whole+dblp+dataset)


