"""Check generated pages, local links, shared registry, redirects, and source art."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];ERRORS=[]
class Document(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.h1=0;self.images=[];self.canonicals=[];self.stack=[];self.nesting=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(tag)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='img':self.images.append(a)
        if tag=='link' and a.get('rel')=='canonical':self.canonicals.append(a['href'])
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
    def handle_endtag(self,tag):
        if tag in self.stack:
            if self.stack[-1]!=tag:self.nesting.append((tag,self.stack[-1]))
            self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
        else:self.nesting.append(('unexpected',tag))
docs={}
for path in ROOT.rglob('*.html'):
    if any(x.startswith('.') for x in path.relative_to(ROOT).parts):continue
    doc=Document();raw=path.read_text(encoding='utf-8');doc.feed(raw);docs[path]=doc
    if doc.h1!=1:ERRORS.append(f'{path}: expected one H1')
    if len(doc.ids)!=len(set(doc.ids)):ERRORS.append(f'{path}: duplicate IDs')
    if len(doc.canonicals)!=1:ERRORS.append(f'{path}: canonical')
    if doc.nesting or doc.stack:ERRORS.append(f'{path}: HTML nesting {doc.nesting} {doc.stack}')
    if 'window.SEER_SERIES' in raw or 'data-series-grid' in raw or 'Standalone Novels' in raw:ERRORS.append(f'{path}: stale catalog')
    for image in doc.images:
        if not all(image.get(k) for k in ['src','alt','width','height']):ERRORS.append(f'{path}: image metadata')
refs=0
for path,doc in docs.items():
    for link in doc.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)
        if not u.path:target=path
        if target.is_dir():target=target/'index.html'
        refs+=1
        if not target.exists():ERRORS.append(f'{path}: missing {link}')
        if u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:ERRORS.append(f'{path}: fragment {link}')
for asset in json.loads((ROOT/'docs/artwork-sources.json').read_text()):
    if hashlib.sha256((ROOT/asset['asset']).read_bytes()).hexdigest()!=asset['sha256']:ERRORS.append('Art mismatch: '+asset['series'])
series=json.loads((ROOT/'data/series.json').read_text(encoding='utf-8'))
assert len(series)==6 and len({s['website'] for s in series})==6
assert {s['website'] for s in series}=={'https://seerworlds.com/','https://journey.i4seer.com/','https://seerfrights.com/','https://seerwarns.com/','https://fairies.i4seer.com/','https://stories.i4seer.com/'}
for route in ['index.html','series/index.html','press/index.html']:
    raw=(ROOT/route).read_text(encoding='utf-8')
    assert all(s['website'] in raw and s['image'] in raw for s in series)
    assert '/standalone/' not in raw and '/series/seer-fairies/' not in raw
css=(ROOT/'style.css').read_text(encoding='utf-8')
for url in re.findall(r"url\(['\"]?([^)'\"]+)",css):
    assert (ROOT/url.lstrip('/')).exists(),url
assert len(docs)==13
if ERRORS:print('\n'.join(ERRORS));sys.exit(1)
print(f'PASS: {len(docs)} pages/redirects, {refs} local links and assets, six series, six exact source images, unique IDs, valid nesting, metadata and CSS assets.')
