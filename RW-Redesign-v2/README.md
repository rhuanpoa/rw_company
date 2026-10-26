# Redesign — rwcompany.com.br

Site estático (HTML, CSS e JavaScript, sem framework), pronto para a Vercel, como o atual.
Nada aqui foi enviado ao GitHub nem publicado em produção.

## Estrutura

```
build.py                 gera o site a partir dos componentes e dos dados dos cases (CASES)
site/                    VERSÃO DE PRODUÇÃO — é esta pasta que vai para o repositório rw_company
  index.html             home (9 seções)
  cases/<slug>/          8 páginas de case
  assets/css/site.css    design system (edite este); site.min.css é gerado
  assets/js/site.js      interações (edite este); site.min.js é gerado
  assets/fonts|img|video fontes próprias, imagens AVIF/WebP, vídeos
  robots.txt, sitemap.xml, site.webmanifest, vercel.json (URLs limpas + cache de 1 ano em /assets)
preview/                 mesma coisa com links explícitos para index.html (usada no preview privado)
materiais/               capturas originais usadas nos cases
auditoria/               Lighthouse antes/depois e prints de revisão
```

## Como editar e gerar

```bash
python3 build.py            # gera site/ (produção)
python3 build.py --preview  # gera preview/
```

Textos dos cases: lista `CASES` em `build.py`. Contatos: constantes no topo de `build.py`.
Requer Python 3 com Pillow e Node (o `npx esbuild` minifica CSS e JS).

## Como subir quando aprovar

1. Crie uma branch no `rw_company` (ex.: `redesign`).
2. Substitua os arquivos pelo conteúdo de `site/` (os arquivos antigos do protótipo podem ficar ou sair).
3. Abra um PR e confira o deploy de preview da Vercel antes de fazer o merge.

## Medições (Lighthouse mobile, servidor local sem compressão)

| | Site atual | Redesign |
|---|---|---|
| Performance | 69 | 97 |
| Acessibilidade | 82 | 100 |
| Boas práticas | 100 | 100 |
| SEO | 100 | 100 |
| LCP | 4,4 s | 2,5 s |
| CLS | 0,176 | 0 |
| Peso da home | 487 KB | 261 KB |

Na Vercel, compressão e cache melhoram esses números; medir de novo no deploy de preview.

## Atenção na produção atual

O print da conversa do agente que está hoje em `assets/cases/truberpell-agente.webp` no site no ar
mostra o CPF de um cliente. No redesign ele está ocultado. Vale trocar esse arquivo na produção já.

## Materiais que deixariam os cases mais fortes

- Print de uma prévia real gerada pela IA na ferramenta da Horizonte.
- Gravação do app de prospecção com uma busca e resultados (dados borrados).
- Gravação do app de bazar com dados de demonstração.
- Logo da RW em SVG.
- Resultados mensuráveis dos projetos novos (Horizonte, agentes), quando houver.
