# Low Edu-Jes-Lipe

Painel público e estático de planejamento da operação de produtos low ticket.

- [Abrir o painel](https://jonatanfroes.github.io/low-sobrinhos/)
- [Catálogo de ideias](https://jonatanfroes.github.io/low-sobrinhos/banco-de-ideias/catalogo-ideias-low-ticket.html)

## Estado atual

67 ideias no banco. Os produtos **LEJL-004, LEJL-016 e LEJL-017 estão aprovados e em Produção**. Os outros 64 estão em Mineração. Nenhum teste foi iniciado.

Primeira leva planejada para **19 a 23 de outubro de 2026**. Mercado, oferta, responsáveis individuais e orçamento ainda serão definidos. A distribuição da equipe exibida no painel é uma proposta.

## Fluxo

Mineração → Produção → Em teste → Escala ou Encerrado.

Na Produção, primeiro definir modelagem próxima à referência, oferta (principal + dois order bumps, sem upsell) e mercado. Depois executar em paralelo: entregáveis; página/checkout/entrega; estrutura de anúncios/rastreamento/criativos. Começar a venda por página de vendas. Conferir a compra completa e definir orçamento antes de iniciar tráfego.

## Organização

- `index.html`: painel gerado e publicado no GitHub Pages.
- `dados/ideias.json`: banco de ideias e etapa atual de cada produto.
- `dados/operacao.json`: roteiro, produtos aprovados, proposta de equipe, tarefas e cronograma.
- `site/painel.template.html`: aparência e estrutura do painel.
- `scripts/gerar-painel.py`: gera o painel e sincroniza os dados no catálogo.
- `banco-de-ideias/`: catálogo, fontes e análises com versões HTML para leitura.

## Atualizar

1. Editar os dados ou o template.
2. Executar `python3 scripts/gerar-painel.py`.
3. Conferir os HTMLs e publicar o commit em `main`.

É possível abrir `index.html` diretamente no navegador, sem servidor. O painel é uma fotografia do planejamento: não salva edições ou movimentações feitas no navegador. A publicação usa a raiz da branch `main` no GitHub Pages.

## Fora do repositório

Entregáveis comerciais, arquivos finais, acessos, credenciais e dados internos de contas não são publicados. A pasta `entregaveis/`, a pasta `privados/` e arquivos de mídia estão no `.gitignore`. As referências públicas de terceiros são links de pesquisa, sem licença implícita de reprodução.

## Automações futuras

As skills para mineração, transcrição, modelagem de oferta/anúncios, página, cadastro de produto e análise de tráfego entram após estabilizar o primeiro fluxo manual. Ainda não foram implementadas neste repositório.
