import sys
from lxml import etree
import requests
from pyquery import PyQuery as pq
import pandas as pd

seed_pages = [
    'http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm',
    'http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm',
    'http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1415.htm'
]
def crawl_seed(seed):
    d = pq(seed)
    return d('a').map(lambda i, a: a.attrib.get('name', None)).filter(lambda i, s: s.startswith('cm20'))
meetings = []
for seed_page in seed_pages:
    meetings.extend(crawl_seed(seed_page))
print(meetings)

def crawl_xml(meeting):
    # This logic is translated from the official JS code
    yy, mm, dd = map(lambda i: int(meeting[i:(i + 2)]), [4, 6, 8])
    if mm >= 10:
        yr = 'yr%02d-%02d' % (yy, yy + 1)
    else:
        yr = 'yr%02d-%02d' % (yy - 1, yy)
    prefix = 'http://www.legco.gov.hk'
    url = '%(prefix)s/%(yr)s/chinese/counmtg/voting/cm_vote_20%(yy)02d%(mm)02d%(dd)02d.xml' % locals()
    return requests.get(url)

vote_xmls = []
for m in meetings:
    vote_xmls.append(crawl_xml(m))
    print('progress: %s/%s %s' % (len(vote_xmls), len(meetings), '#' * len(vote_xmls)))
    sys.stdout.flush()

vote_xmls = filter(lambda r: r.ok, vote_xmls)
vote_xmls = [r.content for r in vote_xmls]
print(len(vote_xmls))

# Information fields, useful for reviewing the result
info_fields = ['vote-date', 'vote-time', 'motion-en', 'mover-en', 'mover-type', 'vote-separate-mechanism']
def xml_to_records(xml):
    doc = etree.XML(xml)
    records = []
    for topic in doc.xpath('//legcohk-vote/meeting/vote'):
        info = [topic.xpath(f)[0].text for f in info_fields]
        date = info[0]
        topic_id = '%s-%s' % (date, topic.attrib['number'])
        for member in topic.xpath('individual-votes/member'):
            member_id = member.attrib['name-en'] # Use English name as ID for sipmlicity
            vote = member.xpath('vote')[0].text
            records.append((topic_id, member_id, vote) + tuple(info))
    return records

records = []
for vote_xml in vote_xmls:
    records.extend(xml_to_records(vote_xml))

# More:
# http://nbviewer.ipython.org/urls/course.ie.cuhk.edu.hk/~engg4030/tutorial/tutorial7/Legco-Preprocessing.ipynb
def clean_record(t):
    # According to the numbers, they seem to be the same person
    t = list(t)
    if t[1] == 'Dr Joseph LEE':
        t[1] = 'Prof Joseph LEE'
    # Other normalization if any
    # ...
    return tuple(t)
records = [clean_record(r) for r in records]

df = pd.DataFrame(records, columns = ['topic_id', 'member_id', 'vote'] + info_fields)
df.to_csv('records-all-with-info.csv', encoding='utf-8')
df.head()
