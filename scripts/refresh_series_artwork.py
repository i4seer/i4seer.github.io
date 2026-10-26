"""Refresh the publisher registry from the six current local series sites.

Run this, build_site.py, then sync_collection_sites.py. No source books change.
"""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'seer-worlds':('SEERWORLDS_WEB','assets/seer-worlds-river-hero.webp','assets/covers/distance.webp','Distance','A white cliff city above blue trees and a sunlit sea, from the Distance cover artwork'),
 'journey':('SEERJOURNEYS_WEB','assets/hero-road.webp','assets/covers/book01.webp','Mile Twenty-Four','A forest road at sunset beside a stone mile marker numbered 24'),
 'seer-frights':('SEERFRIGHTS_WEB','images/seer-frights-series-hero.webp','images/cover-dont-go-into-the-swamp-front-web.webp',"Don’t Go into the Swamp",'Lantern light among the dark trees of the swamp, from the current Seer Frights artwork'),
 'seer-warns':('SEERWARNS_WEB','images/hero-home.webp','images/web/cover-the-good-father-front.webp','The Good Father','Two plates and an unfinished document on a dark kitchen table, from The Good Father cover artwork'),
 'seer-fairies':('SEERFAIRIES_WEB','assets/hero-crossroads.webp','assets/covers/the-puca.webp','The Púca','An engraved folklore scene at an uneasy country crossroads, from The Púca artwork'),
 'seer-stories':('SEERTheSeries_WEB','assets/hero-river.webp','assets/covers/the-river-run.webp','The River Run','A river runner in a wooden boat at a copper sunset, from The River Run cover artwork'),
}
def refresh():
    path=ROOT/'data/series.json';registry=json.loads(path.read_text(encoding='utf-8'));records=[]
    for entry in registry:
        slug=entry['slug'];folder,art,cover,title,alt=SOURCES[slug];site=ROOT.parent/folder
        assert entry['host']==(site/'CNAME').read_text().strip()
        for kind,source in [('art',art),('cover',cover)]:
            target=ROOT/'images/series'/(f'{slug}-20261026.webp' if kind=='art' else f'covers/{slug}.webp')
            target.parent.mkdir(parents=True,exist_ok=True)
            if kind=='cover':
                with Image.open(site/source) as original:
                    image=original.convert('RGB');image.thumbnail((400,640),Image.Resampling.LANCZOS);image.save(target,quality=88,method=6)
            else:shutil.copyfile(site/source,target)
            with Image.open(target) as image:size=list(image.size)
            records.append({'series':slug,'kind':kind,'source':str(site/source),'asset':target.relative_to(ROOT).as_posix(),
                'source_sha256':hashlib.sha256((site/source).read_bytes()).hexdigest(),
                'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'size':size})
            if kind=='art':entry['image']='/'+target.relative_to(ROOT).as_posix();entry['width'],entry['height']=size;entry['alt']=alt
            else:entry['cover']='/'+target.relative_to(ROOT).as_posix();entry['cover_width'],entry['cover_height']=size;entry['cover_title']=title
        if slug=='journey':entry['tagline']='The road did not end.'
    path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs/artwork-sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Refreshed six current series illustrations and six published covers.')
if __name__=='__main__':refresh()
