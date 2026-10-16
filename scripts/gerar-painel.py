#!/usr/bin/env python3
"""Gera o painel estático e sincroniza os dados do catálogo. Só usa a biblioteca padrão."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ideas = json.loads((ROOT / 'dados/ideias.json').read_text())
ops = json.loads((ROOT / 'dados/operacao.json').read_text())
e = lambda value: escape(str(value), quote=True)
products = {x['id']: x for x in ops['products']}

def sources(item):
    return '<div class="source-links">' + ''.join(
        f'<a href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{e(r["title"])} ↗</a>'
        for r in item['refs']) + '</div>'

lanes = []
for stage in ops['stages']:
    group = [i for i in ideas if i['stage'] == stage['id']]
    cards = []
    for item in group:
        product = products.get(item['id'])
        search = f'{item["id"]} {int(item["id"][-3:])} {item["title"]} {item["category"]}'.lower()
        context = '<small>' + e(item['category']) + '</small>'
        if product:
            context += '<p><strong>A iniciar.</strong> Modelagem, oferta e mercado ainda a definir.</p>'
        destination = ('#producao-' + item['id']) if product else ('banco-de-ideias/catalogo-ideias-low-ticket.html?idea=' + item['id'] + '#' + item['id'])
        cards.append(f'<article class="item" data-search="{e(search)}"><span class="id">{e(item["id"])}</span><h4>{e(item["title"])}</h4>{context}<a class="plan-link" href="{e(destination)}">{"Ver plano de produção" if product else "Ver ideia no catálogo"}</a>{sources(item)}</article>')
    lanes.append(f'<section class="lane {e(stage["id"])}" aria-labelledby="stage-{e(stage["id"])}"><div class="lane-head"><h3 id="stage-{e(stage["id"])}">{e(stage["label"])}</h3><output aria-live="polite">{len(group)}</output></div><div class="lane-body">{"".join(cards)}<p class="empty-lane" data-empty {"hidden" if group else ""}>{e(stage["next"])}</p></div></section>')

schedule = ''.join(f'<article class="day"><span class="date">{e(d["date"])}</span><h3>{e(d["label"])}</h3><p>{e(d["work"])}</p><p class="result"><strong>Saída:</strong> {e(d["result"])}</p></article>' for d in ops['schedule'])
plans = []
for p in ops['products']:
    item = next(i for i in ideas if i['id'] == p['id'])
    facts = [('Modelagem', p['model']), ('Mercado', p['market']), ('Oferta e bumps', p['offer']), ('Decisões', p['decision']), ('Revisão do produto', p['review'])]
    facts_html = ''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k, v in facts)
    plans.append(f'<article class="product-plan" id="producao-{e(p["id"])}"><div class="product-title"><h3>{e(p["id"])} · {e(p["name"])}</h3><span class="status">Produção · {e(p["status"])}</span></div><dl>{facts_html}</dl>{sources(item)}</article>')

task_names = {t['id']: t['task'] for t in ops['tasks']}
tasks = []
status_labels = {'pending': 'A iniciar', 'doing': 'Em andamento', 'done': 'Concluído', 'blocked': 'Bloqueado'}
for t in ops['tasks']:
    depends = '; '.join(task_names[k] for k in t['depends']) or 'Pode começar agora'
    statuses = ''.join(f'<td class="pending">{e(status_labels[p["taskStates"][t["id"]]])}<br><small>{e(p["taskOwners"][t["id"]])}</small></td>' for p in ops['products'])
    tasks.append(f'<tr><td class="task-title"><small>{e(t["phase"])}</small><br>{e(t["task"])}</td><td>{e(t["stream"])}</td><td><p>{e(t["output"])}</p></td><td>{e(depends)}</td>{statuses}</tr>')

values = {'BOARD': ''.join(lanes), 'SCHEDULE': schedule, 'PRODUCTS': ''.join(plans), 'TASKS': ''.join(tasks), 'TEAM': ''.join(f'<tr><td>{e(p["name"])}</td><td>{e(p["role"])}</td></tr>' for p in ops['team']), 'TEAM_NOTE': e(ops['teamNote']), 'RULES': ''.join(f'<li>{e(v)}</li>' for v in ops['principles']), 'UPDATED': '/'.join(reversed(ops['updated'].split('-')))}
output = (ROOT / 'site/painel.template.html').read_text()
for key, value in values.items():
    output = output.replace('{{' + key + '}}', value)
(ROOT / 'index.html').write_text(output)

catalog_path = ROOT / 'banco-de-ideias/catalogo-ideias-low-ticket.html'
catalog = catalog_path.read_text()
serialized = json.dumps(ideas, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
catalog = re.sub(r'^const ideas = .*;$', lambda _: 'const ideas = ' + serialized + ';', catalog, count=1, flags=re.M)
catalog_path.write_text(catalog)
print(f'Painel gerado: {len(ideas)} ideias; {len(products)} em Produção.')
