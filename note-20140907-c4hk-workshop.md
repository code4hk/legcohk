## Introduction

Data source:
http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm

   * Voting records in XML.
   * Many other materials, e.g. hansards, in DOC or PDF

Main problems:

   * Scraping: the file naming convention is not very good; no full list; reverse engineering from its own JS.
   * Cleaning: e.g. member name prefix "Dr", "Prof".
   * Principal Component Analysis: 

Online viewer of the notebook: http://nbviewer.ipython.org/github/hupili/legcohk/blob/master/LegCoHK.ipynb

## Further readings

   * Confusion of PCA or the results.
   File an issue
   (some are already explained): https://github.com/code4hk/legcohk/issues?q=is%3Aissue+is%3Aclosed
   * PCA, using Hong Kong Lecgo data as example.
   Self-contained. Including pre-processing, linear algebra basics, and PCA: http://project.hupili.net/engg4030/
   * Other tutorial slides from CUHK/ENGG4030 course: (Spring 2014 version)
   http://project.hupili.net/engg4030/
   * LegcoWatch, full spectrum data scraping, cleaning and API provisioning. https://github.com/legco-watch/legco-watch
