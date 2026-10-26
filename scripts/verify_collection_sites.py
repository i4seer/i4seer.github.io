"""Verify the shared feature across all six local collection websites."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import hashlib,json,re,sys,xml.etree.ElementTree as ET
from sync_collection_sites import PROJECTS
ROOT=Path(__file__).resolve().parents[1]
class Feature(HTMLParser):
    def __init__(self):super().__init__();self.cards=0;self.images=[];self.titles=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and 'sc-card' in a.get('class','').split():self.cards+=1
        if tag=='img':self.images.append(a)
        if a.get('id'):self.ids.append(a['id'])
def verify():
    total=previews=0
    for slug,folder in PROJECTS.items():
        site=ROOT.parent/folder;cfg=json.loads((site/'data/seer-collections.json').read_text(encoding='utf-8'))
        others=[s for s in cfg['collections'] if s['slug']!=slug];assert len(others)==5
        homes=0;books=0
        for path in site.rglob('*.html'):
            if any(p.startswith('.') for p in path.relative_to(site).parts):continue
            total+=1;raw=path.read_text(encoding='utf-8');rel=path.relative_to(site).parts
            parsed=Feature();parsed.feed(raw);assert len(parsed.ids)==len(set(parsed.ids)),path
            assert raw.count('data-seer-collections')==1,path
            is_book=len(rel)==3 and rel[0]=='books'
            is_home=path==site/'index.html';is_dir=rel==('other-series','index.html')
            assert raw.count('sc-preview')<=1,(path,'duplicate preview')
            if is_home or is_book:assert raw.count('sc-preview')==1,(path,'missing preview')
            has_preview='sc-preview' in raw
            if has_preview or is_dir:
                section=re.search(r'<section class="seer-discovery.*?</section>',raw,re.S)[0]
                check=Feature();check.feed(section);assert check.cards==5,path
                assert all(s['website'] in section and s['image'] in section for s in others),path
                assert all(s['cover'] in section for s in others),(path,'missing refreshed cover preview')
                current=next(s for s in cfg['collections'] if s['slug']==slug)
                assert 'href="'+current['website']+'"' not in section,path
                for image in check.images:
                    assert all(image.get(key) for key in ['width','height','alt']),path
                    asset=site/urlsplit(image['src']).path.lstrip('/');assert asset.exists(),asset
                if is_home:homes+=1
                if is_book:books+=1
                if not is_dir:previews+=1
            footer=re.search(r'<div class="sc-footer-links">.*?</div>',raw,re.S)
            if '<footer' in raw:
                assert footer and all(s['website'] in footer[0] for s in others),path
                assert 'href="/other-series/"' in footer[0],path
        tree=ET.fromstring((site/'sitemap.xml').read_text(encoding='utf-8'))
        entries=[n.text for n in tree.iter() if n.tag.endswith('loc') and n.text and n.text.rstrip('/').endswith('/other-series')]
        assert entries==['https://'+(site/'CNAME').read_text().strip()+'/other-series/'],(site,entries)
        for s in cfg['collections']:
            assert hashlib.sha256((site/s['image'].lstrip('/')).read_bytes()).digest()==hashlib.sha256((ROOT/'images/series'/Path(s['image']).name).read_bytes()).digest()
            assert hashlib.sha256((site/s['cover'].lstrip('/')).read_bytes()).digest()==hashlib.sha256((ROOT/'images/series/covers'/Path(s['cover']).name).read_bytes()).digest()
        print(folder+f': PASS; home, {books} book pages, five-card directory, footer links, image sources, sitemap.')
    print(f'PASS: {total} HTML pages; {previews} discovery sections; six full grids; each shows exactly five other collections.')
if __name__=='__main__':verify()
