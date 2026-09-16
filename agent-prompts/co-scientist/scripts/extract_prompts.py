from pathlib import Path
import sys, re, json, hashlib, textwrap
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / '.extraction-deps'))
import pypdf
from pypdf import PdfReader
pdf = root / 'source/41586_2026_10644_MOESM1_ESM.pdf'
reader = PdfReader(pdf)
pages = [p.extract_text(extraction_mode='layout') for p in reader.pages]
source_url = 'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf'
article_url = 'https://www.nature.com/articles/s41586-026-10644-y'
citation = 'Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y'
(root/'source/supplementary-extracted-layout.txt').write_text('\n'.join(f'\n<!-- PDF PAGE {i+1} -->\n{t}' for i,t in enumerate(pages)),encoding='utf-8')

def clean(text):
    text = re.sub(r'^\s*None\s*$', '', text, flags=re.MULTILINE)
    return textwrap.dedent(text).strip()

def note_excerpt(first,last):
    return '\n\n'.join(f'<!-- PDF page {i+1} -->\n\n{pages[i].strip()}' for i in range(first-1,last))

license_header = f'''Source: [{citation}]({article_url})  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF]({source_url}). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf {pypdf.__version__}, layout text extraction.
'''
(root/'original/00-orchestration-pseudocode.md').write_text('# Official Co-Scientist orchestration pseudocode\n\n'+license_header+'\nSupplementary Note 8, PDF pages 56–61. This is published pseudocode, not executable source code and not the full prompt library.\n\nExtraction changes: PDF page labels added; original text, including the printed `None` labels, retained. Layout may contain line wrapping and page-dependent indentation.\n\n```text\n'+note_excerpt(56,61)+'\n```\n',encoding='utf-8')
(root/'original/00-all-published-prompts.md').write_text('# Official published Co-Scientist prompts\n\n'+license_header+'\nComplete Supplementary Note 9, PDF pages 62–69. These are the eight published templates for five specialized roles; Note 9 contains no standalone Supervisor or Proximity template.\n\nExtraction changes: PDF page labels added; original text, including the printed `None` labels, retained. Layout may contain line wrapping and page-dependent indentation.\n\n```text\n'+note_excerpt(62,69)+'\n```\n',encoding='utf-8')

specs = [
 ('01-generation-literature-review.md','Generation: hypothesis generation after literature review','9.1',62,62,'You are an expert tasked',''),
 ('02-generation-scientific-debate.md','Generation: hypothesis generation after scientific debate','9.1',63,64,'You are an expert participating','9.2 Prompt for the Reflection agent'),
 ('03-reflection-observations.md','Reflection: observations explained or contradicted by a hypothesis','9.2',64,65,'You are an expert in scientific hypothesis evaluation.','9.3 Prompts for the Ranking agent'),
 ('04-ranking-comparison.md','Ranking: hypothesis comparison during tournament','9.3',65,66,'You are an expert evaluator tasked','●   Prompt for hypothesis comparison via simulated scientific debate during tournament'),
 ('05-ranking-scientific-debate.md','Ranking: hypothesis comparison via simulated scientific debate','9.3',66,67,'You are an expert in comparative analysis','9.4 Prompts for the Evolution agent'),
 ('06-evolution-feasibility.md','Evolution: hypothesis feasibility improvement','9.4',67,68,'You are an expert in scientific research and technological feasibility analysis.','●   Prompt for hypothesis generation through out-of-the-box thinking'),
 ('07-evolution-out-of-the-box.md','Evolution: hypothesis generation through out-of-the-box thinking','9.4',68,68,'You are an expert researcher tasked','9.5 Prompt for the Meta-review agent'),
 ('08-meta-review.md','Meta-review: review synthesis','9.5',69,69,'You are an expert in scientific research and meta-analysis.',''),
]
records=[]
for filename,title,section,first,last,start,end in specs:
    chunks=[]
    for page_no in range(first,last+1):
        piece=pages[page_no-1]
        if page_no==first:
            offset=piece.index(start)
            line_start=piece.rfind('\n',0,offset)+1
            piece=piece[line_start:]
        if page_no==last and end:
            piece=piece[:piece.index(end)]
        chunks.append(clean(piece))
    content='\n\n'.join(chunks)
    assert content.startswith('You are an expert')
    assert '●   Prompt' not in content and '\nNone\n' not in content
    placeholders=sorted(set(re.findall(r'\{([^{}\n]+)\}',content)))
    placeholders=[p for p in placeholders if len(p)<80]
    label=f'{first}' if first==last else f'{first}–{last}'
    intro = f'# {title}\n\n'+license_header+f'\nSupplementary Note {section}; PDF page(s) {label}.\n\nChanges: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.\n\n'
    intro+='Template fields as printed: '+', '.join('`{'+p+'}`' for p in placeholders)+'.\n\n'
    (root/'original'/filename).write_text(intro+'```text\n'+content+'\n```\n',encoding='utf-8')
    records.append({'file':'original/'+filename,'title':title,'note':section,'pdf_pages':[first,last],'placeholders':placeholders,'prompt_sha256':hashlib.sha256(content.encode()).hexdigest(),'prompt_characters':len(content)})

manifest={'title':'Co-Scientist published prompt extraction','retrieved_on':'2026-09-15','citation':citation,'article_url':article_url,'pdf_url':source_url,'license':'CC-BY-4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','license_evidence':'Article Rights and permissions states Creative Commons Attribution 4.0; no separate restrictive credit line identified in Notes 8–9.','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pdf_pages':len(reader.pages),'extraction':{'package':'pypdf','version':pypdf.__version__,'mode':'layout','changes':['PDF to UTF-8 text','page labels added to complete-note copies','prompt-box None labels and page breaks omitted only from per-template copies','common margin indentation removed per extracted page segment'],'limits':['PDF text extraction can alter line wrapping and reading order; use the saved PDF as the authoritative source.','Printed syntax inconsistencies are retained.','Published research templates are not proof of the complete current hosted-service instructions.']},'templates':records,'no_standalone_prompt_published_in_note9':['Supervisor','Proximity']}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for file in sorted((root/'original').glob('*.md')):
    print(f'{file.name}: {file.stat().st_size} bytes')
print('Templates:',len(records),'PDF SHA256:',manifest['pdf_sha256'])
