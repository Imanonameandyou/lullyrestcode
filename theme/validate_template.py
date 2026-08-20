#!/usr/bin/env python3
"""Validate a built template's settings against the theme's section schemas.

Run from inside the pulled theme directory BEFORE `shopify theme push`. The CLI
reports "pushed successfully" for a rejected JSON template unless you read its
full output, and a rejected template leaves the PREVIOUS version live on the
theme — so a push can silently no-op. This catches the type errors that cause it.

Usage:  cd <pulled-theme>  &&  python3 <repo>/theme/validate_template.py
"""
import json,re,os,sys
TH="."
def schema(path):
    s=open(path,encoding="utf-8").read()
    m=re.search(r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',s,re.S)
    return json.loads(m.group(1)) if m else None
def types_for(stype):
    """map setting id -> schema type, for a section and its blocks"""
    p=os.path.join(TH,"sections",stype+".liquid")
    if not os.path.exists(p): return None,{}
    d=schema(p)
    if not d: return None,{}
    sec={x["id"]:x["type"] for x in d.get("settings",[]) if x.get("id")}
    blk={}
    for b in d.get("blocks",[]):
        blk[b.get("type")]={x["id"]:x["type"] for x in b.get("settings",[]) if x.get("id")}
    return sec,blk
def check(val,t,where,out):
    if t in ("select","radio","text","textarea","url","color","font_picker","image_picker","video_url","liquid"):
        if not isinstance(val,str): out.append(f"{where}: {t} needs string, got {type(val).__name__} ({val!r})")
    elif t=="checkbox":
        if not isinstance(val,bool): out.append(f"{where}: checkbox needs bool, got {val!r}")
    elif t in ("range","number"):
        if not isinstance(val,(int,float)) or isinstance(val,bool): out.append(f"{where}: {t} needs number, got {val!r}")
    elif t=="richtext":
        if not (isinstance(val,str) and re.match(r'^\s*<(p|ul|ol|h[1-6])\b',val)):
            out.append(f"{where}: richtext must open with <p>/<ul>/<ol>/<h1-6>, got {str(val)[:50]!r}")
tpl=re.sub(r'/\*.*?\*/','',open("templates/product.lullyrest.json",encoding="utf-8").read(),flags=re.S)
d=json.loads(tpl); out=[]
for key in d["order"]:
    sec=d["sections"][key]; st=sec["type"]
    stypes,btypes=types_for(st)
    if stypes is None:
        out.append(f"[section file missing] {st}"); continue
    for sid,v in sec.get("settings",{}).items():
        if sid in stypes: check(v,stypes[sid],f"{st}.{sid}",out)
    for bk in sec.get("block_order",[]):
        b=sec["blocks"][bk]; bt=b["type"]
        if bt not in btypes:
            continue
        for sid,v in b.get("settings",{}).items():
            if sid in btypes[bt]: check(v,btypes[bt][sid],f"{st}/{bt}.{sid}",out)
print("\n".join(out) if out else "ALL SETTINGS VALID")
