"""Sync the same self-contained discovery feature to all six local series websites.
Run after updating the publisher's data/series.json or shared feature templates.
"""
from pathlib import Path
from datetime import datetime
import json,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
PROJECTS={'seer-worlds':'SEERWORLDS_WEB','journey':'SEERJOURNEYS_WEB','seer-frights':'SEERFRIGHTS_WEB','seer-warns':'SEERWARNS_WEB','seer-fairies':'SEERFAIRIES_WEB','seer-stories':'SEERTheSeries_WEB'}
def main():
    registry=json.loads((ROOT/'data/series.json').read_text(encoding='utf-8'))
    assert len(registry)==6 and {s['slug'] for s in registry}==set(PROJECTS)
    backup=Path(tempfile.gettempdir())/('seer-collection-refresh-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    backups=[]
    for slug,folder in PROJECTS.items():
        site=ROOT.parent/folder
        assert site.is_dir() and (site/'CNAME').exists(),site
        expected=next(s['host'] for s in registry if s['slug']==slug)
        assert (site/'CNAME').read_text().strip()==expected
        for p in site.rglob('*.html'):
            if any(part.startswith('.') for part in p.relative_to(site).parts):continue
            raw=p.read_text(encoding='utf-8');footer=re.search(r'<footer\b.*?</footer>',raw,re.S)
            if not footer:continue
            count=len(re.findall(r'<div[^>]*>\s*<h([345])[^>]*>(?:Other series|More stories|More Seer|Other collections)</h\1>',footer[0]))
            assert count==1,(p,'Expected one cross-series footer',count)
            backups.append((p,backup/folder/p.relative_to(site)))
        for rel in ['sitemap.xml','routes.json','scripts/build_site.py','scripts/update_collections.py','data/seer-collections.json','assets/seer-collections/collections.css']:
            p=site/rel
            if p.exists():backups.append((p,backup/folder/rel))
    for original,dest in backups:
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,dest)
    for slug,folder in PROJECTS.items():
        site=ROOT.parent/folder
        for directory in ['scripts','data','docs','assets/seer-collections']:(site/directory).mkdir(exist_ok=True,parents=True)
        shutil.copyfile(ROOT/'scripts/collection_feature.py',site/'scripts/update_collections.py')
        shutil.copyfile(ROOT/'assets/collection-feature.css',site/'assets/seer-collections/collections.css')
        collections=[]
        for entry in registry:
            item=dict(entry);asset_name=Path(item['image']).name
            shutil.copyfile(ROOT/item['image'].lstrip('/'),site/'assets/seer-collections'/asset_name)
            item['image']='/assets/seer-collections/'+asset_name;collections.append(item)
        (site/'data/seer-collections.json').write_text(json.dumps({'current':slug,'collections':collections},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
        builder=site/'scripts/build_site.py'
        if builder.exists():
            text=builder.read_text(encoding='utf-8')
            if '# Refresh shared Seer Press discovery.' not in text:
                builder.write_text(text+"\n# Refresh shared Seer Press discovery.\nimport runpy\nrunpy.run_path(str(ROOT/'scripts/update_collections.py'),run_name='__main__')\n",encoding='utf-8',newline='\n')
        subprocess.run([sys.executable,str(site/'scripts/update_collections.py')],check=True)
        note=site/'docs/collection-discovery.md'
        note.write_text('''# Shared collection discovery

All six Seer Press collections share the same image-card feature. This site shows the other five collections, excluding itself. Home and individual book pages carry the compact cards; `/other-series/` provides a full grid with descriptions and audience labels. Every footer links to the other five websites and the local full grid. Existing cross-series sections are replaced.

The feature uses local assets and static HTML, with a separate namespaced stylesheet that matches this site’s palette. No carousel, remote image dependency, or JavaScript requirement. Site-specific content and maps remain intact.

Run `python scripts/update_collections.py` to refresh this site from `data/seer-collections.json`. Where `scripts/build_site.py` exists, it runs that refresh automatically. To update every local series site from the shared publisher registry, run `python C:/SEERWEB/scripts/sync_collection_sites.py`.

Shared feature source: C:/SEERWEB/scripts/collection_feature.py and C:/SEERWEB/assets/collection-feature.css. Artwork and approved site addresses come from C:/SEERWEB/data/series.json. Images use content-versioned URLs. CNAME and hosting configuration are preserved. This local refresh does not deploy the sites.
''',encoding='utf-8',newline='\n')
    print('Pre-refresh backup:',backup)
if __name__=='__main__':main()
