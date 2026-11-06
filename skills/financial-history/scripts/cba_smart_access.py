from pathlib import Path
import re,json,subprocess,xml.etree.ElementTree as E
from datetime import datetime
from tempfile import TemporaryDirectory
from decimal import Decimal
ns={'x':'http://www.w3.org/1999/xhtml'}
def minor(raw):return int(Decimal(raw.replace('$','').replace(',',''))*100)
def parse_text(p, source):
 text=p.with_suffix('.txt').read_text()
 period=re.search(r'Period\s+(\d{1,2} \w{3} \d{4})\s*-\s*(\d{1,2} \w{3} \d{4})',text)
 if not period:raise ValueError('Missing statement period.')
 start,end=[datetime.strptime(x,'%d %b %Y').date() for x in period.groups()]
 if not re.search(r'Account Number', text):
  raise ValueError('Missing account header.')
 def balance(label):
  m=re.search(label+r'\s+(\$?[\d,]+\.\d{2})\s*(CR|DR)',text)
  if not m:raise ValueError(f'Missing {label}.')
  return {'raw':m[1]+' '+m[2],'amount':minor(m[1])*(-1 if m[2]=='DR' else 1),'quote':m[0]}
 opening,closing=balance('OPENING BALANCE'),balance('CLOSING BALANCE')
 xml=p.with_suffix('.html')
 subprocess.run(['pdftotext','-bbox-layout',str(source),str(xml)],check=True)
 records=[];current=None;raw_date=None;date_location=None;pending=[];quotes=[];running=opening['amount'];checks=0
 for pi,page in enumerate(E.parse(xml).findall('.//x:page',ns),1):
  groups=[]
  for w in sorted(page.findall('.//x:word',ns),key=lambda w:(float(w.attrib['yMin']),float(w.attrib['xMin']))):
   # Ignore rotated reference codes in the page margin.
   if float(w.attrib['xMin']) < 50:continue
   y=float(w.attrib['yMin'])
   if not groups or abs(y-groups[-1][0])>2:groups.append((y,[w]))
   else:groups[-1][1].append(w)
  active=False
  for li,(y,ws) in enumerate(groups,1):
   ws=sorted(ws,key=lambda w:float(w.attrib['xMin']));line=' '.join(w.text or '' for w in ws);names={w.text:w for w in ws}
   if all(k in names for k in ['Date','Transaction','Debit','Credit','Balance']):
    cols={k:float(names[k].attrib['xMax']) for k in ['Debit','Credit']};tx=float(names['Transaction'].attrib['xMin']);debitx=float(names['Debit'].attrib['xMin']);active=True;continue
   if not active:continue
   if re.match(r'(Opening balance|Total Debits|Total Credits|Transaction Summary|Your account|Important|Please check|The information|Account fee)',line,re.I):active=False;continue
   date_text=' '.join(w.text or '' for w in ws if float(w.attrib['xMax']) < tx)
   dm=re.fullmatch(r'(\d{1,2} [A-Z][a-z]{2})(?: (\d{4}))?', date_text)
   if date_text and not dm:
    raise ValueError(f'Unreadable date column: page {pi}, row {li}: {date_text!r}')
   if dm:
    candidates=[]
    for year in range(start.year,end.year+1):
     try:dt=datetime.strptime(dm[1]+' '+str(year),'%d %b %Y').date()
     except ValueError:continue
     if start<=dt<=end and (not dm[2] or year==int(dm[2])):candidates.append(dt)
    if len(candidates)!=1:raise ValueError(f'Ambiguous or invalid date: {line}')
    current=candidates[0].isoformat();raw_date=dm[0];date_location=f'page:{pi}:visual-row:{li}'
   if 'OPENING BALANCE' in line or 'CLOSING BALANCE' in line:continue
   movements=[];printed=[]
   for w in ws:
    raw=w.text or ''
    if not re.fullmatch(r'\$?[\d,]+\.\d{2}',raw):continue
    x=float(w.attrib['xMax'])
    if x>cols['Credit']+25:printed.append(raw);continue
    col=min(cols,key=lambda k:abs(cols[k]-x))
    if abs(cols[col]-x)<5:movements.append((col,raw))
   desc=' '.join(w.text or '' for w in ws if tx-1<=float(w.attrib['xMin']) and float(w.attrib['xMax'])<debitx-5)
   if not movements:
    if desc and current and not line.startswith(('Statement','Account Number')):
     pending.append(desc);quotes.append(line)
    continue
   if not current or len(movements)!=1:
    raise ValueError(f'Missing transaction date or ambiguous amount: page {pi}: {line}')
   col,raw=movements[0]
   amount=minor(raw)*(1 if col=='Credit' else -1);running+=amount
   if printed:
    bal=minor(printed[-1])*(-1 if re.search(r'\bDR\b',line) else 1)
    if running!=bal:raise ValueError(f'Running balance mismatch: {current}: {line}')
    checks+=1
   records.append({'date':current,'raw_date':raw_date,'date_location':date_location,'kind':col,'raw':raw,'amount':amount,'description':' '.join(pending+[desc]).strip(),'quote':'\n'.join(quotes+[line]),'location':f'page:{pi}:visual-row:{li}'})
   pending=[];quotes=[];current=None;raw_date=None;date_location=None
 if running!=closing['amount']:raise ValueError('Closing balance mismatch.')
 return {'file':p.stem+'.pdf','start':start.isoformat(),'end':end.isoformat(),'opening':opening,'closing':closing,'records':records,'running_checks':checks}

def parse(pdf):
 """Read CBA Smart Access tables; reject missing dates and balance mismatches."""
 pdf=Path(pdf).resolve()
 with TemporaryDirectory(prefix='cba-statement-') as folder:
  text=Path(folder)/(pdf.stem+'.txt')
  subprocess.run(['pdftotext','-layout',str(pdf),str(text)],check=True)
  return parse_text(text,pdf)

if __name__=='__main__':
 import sys
 print(json.dumps(parse(sys.argv[1])))
