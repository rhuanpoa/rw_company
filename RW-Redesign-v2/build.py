#!/usr/bin/env python3
"""Gera o site da RW Company (home + páginas de case) a partir de componentes compartilhados.

    python3 build.py            -> site/   (produção: URLs limpas, /cases/aurora/)
    python3 build.py --preview  -> preview/ (links explícitos para index.html)
"""
import html, json, shutil, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "site")
DOMAIN = "https://rwcompany.com.br"
WA_NUMBER = "5543991169059"
PHONE_LABEL = "(43) 99116-9059"
EMAIL = "rhuan0292@gmail.com"
INSTAGRAM = "https://instagram.com/rw.companyy"


def wa(msg="Olá! Vim pelo site da RW Company e quero conversar sobre meu negócio."):
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(msg)}"


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- ícones
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "play": '<path d="M7 4.5v15l13-7.5z" fill="currentColor" stroke="none"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.5 2.5M15.2 15.2l2.5 2.5M6.3 17.7l2.5-2.5M15.2 8.8l2.5-2.5"/>',
    "bot": '<rect x="4" y="7" width="16" height="12" rx="4"/><path d="M12 3v4M9 13h.01M15 13h.01M9.5 16h5"/>',
    "browser": '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    "app": '<rect x="6" y="2.5" width="12" height="19" rx="3"/><path d="M10 18.5h4"/><path d="M9 7h6M9 10.5h6M9 14h3"/>',
    "megaphone": '<path d="M4 10v4a1 1 0 0 0 1 1h2l5 4V5L7 9H5a1 1 0 0 0-1 1z"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12"/>',
    "flow": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 6h7M18 8.5v7M7.8 7.8l8.4 8.4"/>',
    "radar": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12l6-6"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "filter": '<path d="M4 5h16l-6 7v6l-4 2v-8z"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "repeat": '<path d="M4 9a7 7 0 0 1 12-3l2 2M20 15a7 7 0 0 1-12 3l-2-2"/><path d="M18 3v5h-5M6 21v-5h5"/>',
    "scale": '<path d="M4 17l5-5 4 4 7-7"/><path d="M15 9h5v5"/>',
    "handshake": '<path d="M3 12l4-4 4 2 3-2 3 1 4 3"/><path d="M7 14l3 3c.8.8 2 .8 2.8 0l4.2-4.2"/><path d="M3 12l3 3M21 12l-3 3"/>',
    "puzzle": '<path d="M9 3h3a2 2 0 1 1 4 0h3v6a2 2 0 1 0 0 4v6h-6a2 2 0 1 0-4 0H3v-6a2 2 0 1 1 0-4V3z"/>',
    "whatsapp": '<path d="M20.5 3.5A11 11 0 0 0 3.3 17.2L2 22l4.9-1.3A11 11 0 0 0 20.5 3.5zm-8.5 17a9 9 0 0 1-4.6-1.3l-.3-.2-2.9.8.8-2.8-.2-.3a9 9 0 1 1 7.2 3.8zm5-6.7c-.3-.1-1.6-.8-1.9-.9-.3-.1-.4-.1-.6.1l-.9 1.1c-.2.2-.3.2-.6.1a7.3 7.3 0 0 1-3.6-3.2c-.3-.5.3-.4.8-1.4.1-.2 0-.3 0-.5l-.9-2c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.3.8 3.1.7.5-.1 1.6-.7 1.8-1.3.2-.6.2-1.2.2-1.3-.1-.1-.3-.2-.6-.3z" fill="currentColor" stroke="none"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}


def sprite():
    out = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true">']
    for k, v in ICONS.items():
        out.append(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>')
    out.append("</svg>")
    return "".join(out)


def ico(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"/></svg>'


# ---------------------------------------------------------------- imagens
def picture(base, widths, alt, sizes, a="", eager=False, cls=""):
    """<picture> AVIF + WebP com srcset; width/height reais evitam layout shift."""
    from PIL import Image
    first = OUT_ASSETS / "img" / f"{base}-{widths[0]}.webp"
    w, h = Image.open(first).size
    srcset = lambda ext: ", ".join(f"{a}assets/img/{base}-{x}.{ext} {x}w" for x in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img{c} src="{a}assets/img/{base}-{widths[-1]}.webp" width="{w}" height="{h}" alt="{esc(alt)}" {load}></picture>')


# ---------------------------------------------------------------- dados dos cases (só fatos confirmados)
CASES = [
    {
        "slug": "aurora-sobremesas", "cat": "marketing", "wide": True,
        "kicker": "Marketing · Redes sociais", "name": "Aurora Sobremesas",
        "short": "Conteúdo, posicionamento e gestão do Instagram de uma confeitaria de Londrina, assumidos do zero.",
        "result": "+41% em 7 dias",
        "card_media": ("phone", "aurora", [472], "Perfil real da Aurora Sobremesas no Instagram"),
        "client": "Aurora Sobremesas, confeitaria e delivery de doces em Londrina/PR",
        "services": ["Marketing digital", "Redes sociais", "Posicionamento"],
        "tech": None, "status": "Em andamento", "link": None,
        "challenge": ["A Aurora vende doces por delivery em Londrina e precisava que o Instagram trabalhasse a favor das vendas: um perfil que apresentasse bem os produtos e fizesse mais gente conhecer a marca."],
        "solution": ["A RW assumiu o perfil do zero: conteúdo, posicionamento e gestão da conta.", ],
        "delivered": ["Planejamento e produção de conteúdo", "Posicionamento da marca no Instagram", "Gestão do perfil"],
        "result_big": "+41%", "result_text": "O perfil passou de 1.700 para 2.400 seguidores em apenas 1 semana de trabalho.",
        "media": [("video", "case-aurora", "Animação do resultado: 1.700 → 2.400 seguidores"), ("phone", "aurora", [472], "Perfil real da Aurora Sobremesas no Instagram")],
        "note": None,
    },
    {
        "slug": "horizonte-3d", "cat": "sites ia", "wide": True, "new": True,
        "kicker": "Landing page · IA", "name": "Horizonte 3D Print",
        "short": "Site da gráfica 3D com uma ferramenta em que o cliente envia uma foto e vê uma prévia da peça, gerada por IA, antes de pedir orçamento.",
        "result": "Prévia com IA",
        "card_media": ("browser", "horizonte-site", [640, 1200], "Página inicial da Horizonte 3D Print"),
        "client": "Horizonte 3D Print, impressão 3D de peças personalizadas",
        "services": ["Landing page", "Ferramenta com IA", "Orçamento pelo WhatsApp"],
        "tech": ["Next.js", "React", "TypeScript", "Supabase", "OpenAI (geração de imagem)", "Vercel"],
        "status": "No ar", "link": ("lp-horizonte.vercel.app", "https://lp-horizonte.vercel.app"),
        "challenge": ["Quem procura uma peça personalizada tem dificuldade de imaginar como ela vai ficar. A Horizonte queria apresentar o que faz e, ao mesmo tempo, ajudar o cliente a visualizar a peça antes de pedir orçamento."],
        "solution": ["Uma landing page com produtos, como funciona, sobre a empresa e perguntas frequentes, e uma ferramenta de personalização: o cliente envia uma imagem de referência, escolhe tamanho, finalidade e cores, e a IA gera uma prévia visual da peça.",
                     "Com a prévia pronta, o pedido segue para o WhatsApp da equipe com um código de orçamento."],
        "delivered": ["Prévia da peça gerada por IA a partir de uma foto", "Contas com 3 gerações gratuitas por visitante",
                      "Pedido de orçamento pelo WhatsApp com código de identificação", "Lista de remarketing de quem gerou prévia e ainda não pediu orçamento",
                      "Validação de arquivos e limite de uso para evitar abuso"],
        "result_big": None, "result_text": "Projeto recém-lançado. Os resultados serão publicados aqui quando houver dados.",
        "media": [("browser", "horizonte-site", [640, 1200, 1600], "Página inicial da Horizonte 3D Print"),
                  ("browser", "horizonte-ferramenta", [800, 1400], "Ferramenta de personalização com IA"),
                  ("browser", "horizonte-produtos", [800, 1400], "Seção de produtos")],
        "note": None,
    },
    {
        "slug": "agente-whatsapp-truberpell", "cat": "ia",
        "kicker": "Agente de IA · WhatsApp · CRM", "name": "Agente de vendas Truberpell",
        "short": "Atende no WhatsApp 24h, qualifica leads, gera orçamentos e links de pagamento, integrado ao CRM.",
        "result": "Atendimento 24h",
        "card_media": ("phonevideo", "case-agente-whatsapp", None, "Agente da Truberpell atendendo no WhatsApp"),
        "client": "Truberpell, indústria de higienização institucional",
        "services": ["Agente de IA", "Automação comercial", "Integração com CRM"],
        "tech": None, "status": "Em operação", "link": None,
        "challenge": ["Pedidos de orçamento chegam pelo WhatsApp a qualquer hora, e cada um exige consultar produto, preço, quantidade mínima e frete antes de responder."],
        "solution": ["Um agente de vendas que conversa com o cliente no WhatsApp: entende o pedido, informa preço e condições, calcula o total, pede os dados para o orçamento formal e envia o orçamento em PDF, tudo integrado ao CRM da empresa."],
        "delivered": ["Atendimento 24h no WhatsApp", "Qualificação do lead durante a conversa", "Orçamentos e links de pagamento", "Integração com o CRM"],
        "result_big": "24h", "result_text": "O agente atende a qualquer hora, inclusive fora do expediente.",
        "media": [("chat", None, None, None), ("image", "truberpell-agente", [1002], "Print real da conversa do agente com um cliente (dados pessoais ocultos)")],
        "note": "Print real do atendimento. O CPF do cliente foi ocultado.",
    },
    {
        "slug": "agente-instagram-horizonte", "cat": "ia",
        "kicker": "Agente de IA · Instagram", "name": "Agente no direct da Horizonte",
        "short": "Responde o direct do Instagram, entende o pedido, pergunta quantidade e passa o atendimento para o consultor.",
        "result": "Direct atendido",
        "card_media": ("phonevideo", "agente-instagram", None, "Gravação do agente respondendo no direct do Instagram"),
        "client": "Horizonte 3D Print, impressão 3D de peças personalizadas",
        "services": ["Agente de IA", "Instagram", "Automação comercial"],
        "tech": None, "status": "Em operação", "link": None,
        "challenge": ["Muitas pessoas chegam pelo Instagram perguntando sobre produtos e tamanhos. Sem resposta rápida, o interesse esfria."],
        "solution": ["Um agente que se apresenta como representante da Horizonte, responde sobre os produtos (como as placas 3D personalizadas, inclusive sob medida), pergunta a quantidade e passa as informações para o consultor responsável continuar o atendimento no próprio direct."],
        "delivered": ["Resposta imediata no direct", "Perguntas de qualificação (produto, tamanho, quantidade)", "Passagem do pedido resumido para o consultor"],
        "result_big": None, "result_text": "Agente em operação no Instagram da Horizonte 3D.",
        "media": [("phonevideo", "agente-instagram", None, "Gravação real do agente no direct do Instagram")],
        "note": "Gravação real da tela, acelerada nos trechos de digitação e espera.",
    },
    {
        "slug": "truberpell-site", "cat": "sites", "wide": False,
        "kicker": "Site institucional · E-commerce", "name": "Truberpell",
        "short": "Site completo para a indústria: empresa, produtos, segmentos e canais de contato, com formulário ligado ao CRM.",
        "result": "truberpell.com.br",
        "card_media": ("browser", "truberpell-site", [640, 1200], "Página inicial do site da Truberpell"),
        "client": "Truberpell, higienização institucional desde 1985",
        "services": ["Site institucional", "Loja virtual", "Integração com CRM"],
        "tech": ["Shopify (tema próprio em Liquid)", "Google Apps Script", "Pipedrive"],
        "status": "No ar", "link": ("truberpell.com.br", "https://truberpell.com.br"),
        "challenge": ["A Truberpell atende setores muito diferentes (restaurantes, hotelaria, clínicas, lanchonetes, postos) e precisava de um site que apresentasse a empresa e levasse cada tipo de cliente ao produto certo."],
        "solution": ["Um tema próprio na Shopify com páginas de produtos, segmentos, produtos personalizados, empresa, blog e trabalhe conosco.",
                     "O formulário do WhatsApp do site grava os contatos numa planilha e cria pessoa e negócio no Pipedrive, com a chave de acesso guardada no servidor, nunca exposta no navegador."],
        "delivered": ["Tema Shopify sob medida", "Páginas por segmento de cliente", "Formulário integrado ao Pipedrive com credencial protegida", "Manual de manutenção do site"],
        "result_big": None, "result_text": "Site no ar em truberpell.com.br.",
        "media": [("video", "case-truberpell", "Navegação pelo site da Truberpell"), ("browser", "truberpell-site", [640, 1200, 1600], "Página inicial do site da Truberpell"), ("phone", "truberpell-mobile", [430, 860], "Site da Truberpell no celular")],
        "note": None,
    },
    {
        "slug": "prospec", "cat": "apps",
        "kicker": "App próprio · Prospecção", "name": "Prospec: Radar de clientes",
        "short": "Pesquise “restaurantes em Londrina” e receba os negócios do Google Maps com nome, telefone, endereço e avaliação.",
        "result": "Leads em tempo real",
        "card_media": ("browser", "prospec", [1002], "Painel do app de prospecção"),
        "client": "Produto próprio da RW Company",
        "services": ["Sistema sob medida", "Prospecção comercial"],
        "tech": ["Python", "FastAPI", "Playwright", "WebSocket", "Exportação para Excel"],
        "status": "Em uso", "link": None,
        "challenge": ["Montar listas de prospecção copiando dados do Google à mão toma horas da equipe comercial."],
        "solution": ["Um sistema que busca estabelecimentos no Google Maps e extrai nome, telefone, endereço e avaliação em tempo real, com os resultados aparecendo na tela conforme são encontrados."],
        "delivered": ["Busca por segmento e cidade", "Resultados em tempo real", "Exportação para Excel e lista de telefones já formatados", "Aba de WhatsApp preparada para integração com API de envio"],
        "result_big": None, "result_text": "Ferramenta em uso na prospecção da própria RW Company.",
        "media": [("browser", "prospec", [1002], "Painel do app de prospecção")],
        "note": None,
    },
    {
        "slug": "bazar", "cat": "apps",
        "kicker": "App · Gestão", "name": "App de bazar",
        "short": "Catálogo de peças, vendas e caixa num app de celular que funciona até sem internet.",
        "result": "Funciona offline",
        "card_media": ("screen", "bazar-vendas", [462], "App de bazar: vendas da semana e últimas vendas"),
        "client": "Bazar Duo Garimpo",
        "services": ["Aplicativo sob medida", "Gestão de estoque e financeiro"],
        "tech": ["HTML, CSS e JavaScript", "PWA (instalável e offline)", "Supabase"],
        "status": "Em uso", "link": None,
        "challenge": ["Quem vende peça por peça precisa registrar a venda na hora, muitas vezes sem internet, e saber quanto tem em estoque e em caixa."],
        "solution": ["Um app que roda no navegador do celular e instala como aplicativo: catálogo de peças, registro de vendas e caixa. Os dados ficam no aparelho e sincronizam com a conta quando há rede. A venda nunca espera a internet."],
        "delivered": ["Catálogo de peças", "Registro de vendas e caixa", "Funcionamento offline", "Sincronização entre aparelhos com login"],
        "result_big": None, "result_text": "App em uso no dia a dia do bazar.",
        "media": [("screen", "bazar-vendas", [462], "App de bazar: vendas da semana e últimas vendas")],
        "note": None,
    },
    {
        "slug": "minhas-financas", "cat": "apps",
        "kicker": "App · Finanças pessoais", "name": "Minhas Finanças",
        "short": "Controle financeiro no celular: painel do mês, previsão de 12 meses, metas, parcelas e importação de extrato.",
        "result": "Previsão de 12 meses",
        "card_media": ("phones", "financeiro", None, "Telas do app Minhas Finanças com dados ilustrativos"),
        "client": "Aplicativo desenvolvido pela RW Company",
        "services": ["Aplicativo sob medida"],
        "tech": ["HTML, CSS e JavaScript", "PWA (instalável e offline)", "Supabase (login e sincronização)", "pdf.js"],
        "status": "Em uso", "link": None,
        "challenge": ["Planilhas de gastos não mostram o que ainda vai acontecer no mês nem quanto vai sobrar daqui a alguns meses."],
        "solution": ["Um app de finanças pessoais que separa o que já aconteceu do que está programado, projeta o saldo dos próximos 12 meses e acompanha metas e compras parceladas.",
                     "Importa extratos em OFX, CSV e PDF do Banco do Brasil, sem duplicar lançamentos, e sincroniza entre celular e computador."],
        "delivered": ["Painel do mês: já feito × programado", "Previsão de saldo para 12 meses", "Metas e parcelas", "Importação de extrato (OFX, CSV, PDF)", "Backup e funcionamento offline"],
        "result_big": None, "result_text": "App em uso.",
        "media": [("phones3", "financeiro", None, "Telas do app Minhas Finanças com dados ilustrativos")],
        "note": "Telas com dados ilustrativos, para preservar a privacidade de quem usa o app.",
    },
]

CHAT = [
    {"from": "me", "html": "oi<small>15:24 <b>✓✓</b></small>", "wait": 700},
    {"from": "bot", "html": "Olá! Sou a Elisangela da Truberpell, no que posso te ajudar hoje?<small>15:25</small>", "wait": 1500},
    {"from": "me", "html": "preciso de um orçamento de guardanapo folha simples para londrina paraná<small>15:26 <b>✓✓</b></small>", "wait": 900},
    {"from": "bot", "html": "Para Londrina/PR, o Guardanapo Truberpell 17x20, folha simples, fica R$ 164,90 por caixa com 6.000 unidades. O pedido mínimo é de 5 caixas; quantas caixas você precisa e qual será o tipo de uso?<small>15:26</small>", "wait": 2600},
    {"from": "me", "html": "8 caixas<small>15:27 <b>✓✓</b></small>", "wait": 900},
    {"from": "bot", "html": '<span class="wa__doc"><span class="wa__pdf">PDF</span><span>orcamento_43.pdf<br><span style="font-size:11.5px;color:#8696a0">PDF • 112 KB</span></span></span>Segue o orçamento para análise e aprovação.<small>15:28</small>', "wait": 1200},
]


# ---------------------------------------------------------------- componentes
def head(title, desc, path, a, og_type="website", extra_ld=None):
    canonical = DOMAIN + path
    ld = [{
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "RW Company",
        "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/icon-512.png", "image": DOMAIN + "/assets/img/og.png",
        "description": "Tecnologia, inteligência artificial, marketing e desenvolvimento para empresas.",
        "telephone": "+55-43-99116-9059", "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Londrina", "addressRegion": "PR", "addressCountry": "BR"},
        "areaServed": "BR", "sameAs": [INSTAGRAM],
    }]
    if extra_ld:
        ld += extra_ld
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#07090F">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="RW Company">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{a}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{a}site.webmanifest">
<link rel="preload" href="{a}assets/fonts/archivo-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a}assets/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}assets/css/site.min.css">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
"""


def header(a, home):
    h = "" if home else f"{a}{'index.html' if PREVIEW else ''}"
    links = [("sobre", "Sobre"), ("solucoes", "Soluções"), ("cases", "Cases"), ("ia", "IA"), ("processo", "Processo")]
    nav = "".join(f'<a class="nav__link" href="{h}#{i}">{t}</a>' for i, t in links)
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="progress" aria-hidden="true"></div>
<header class="header">
  <div class="container header__inner">
    <a class="brand" href="{h or '#topo'}" aria-label="RW Company, página inicial"><img src="{a}assets/img/logo-48.webp" srcset="{a}assets/img/logo-96.webp 2x" width="34" height="40" alt=""><span>RW COMPANY</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu"><span></span></button>
    <nav class="nav" id="nav" aria-label="Principal">
      {nav}
      <a class="btn btn--primary btn--sm" href="{wa()}" target="_blank" rel="noopener">Fale com um especialista</a>
    </nav>
  </div>
</header>
"""


def case_href(slug, a):
    return f"{a}cases/{slug}/" + ("index.html" if PREVIEW else "")


def footer(a, home):
    h = "" if home else f"{a}{'index.html' if PREVIEW else ''}"
    serv = ["Inteligência artificial", "Sites e landing pages", "Sistemas e aplicativos", "Marketing digital e tráfego pago", "Automação comercial", "Prospecção"]
    cases = "".join(f'<li><a href="{case_href(c["slug"], a)}">{esc(c["name"])}</a></li>' for c in CASES[:6])
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="{h or '#topo'}"><img src="{a}assets/img/logo-48.webp" srcset="{a}assets/img/logo-96.webp 2x" width="34" height="40" alt=""><span>RW COMPANY</span></a>
        <p>Tecnologia, inteligência artificial, marketing e desenvolvimento para empresas. Londrina/PR.</p>
      </div>
      <div><h2>Navegação</h2><ul>
        <li><a href="{h}#sobre">Sobre</a></li><li><a href="{h}#solucoes">Soluções</a></li><li><a href="{h}#cases">Cases</a></li>
        <li><a href="{h}#processo">Processo</a></li><li><a href="{h}#contato">Contato</a></li></ul></div>
      <div><h2>Serviços</h2><ul>{"".join(f'<li><a href="{h}#solucoes">{s}</a></li>' for s in serv)}</ul></div>
      <div><h2>Contato</h2><ul>
        <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp {PHONE_LABEL}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @rw.companyy</a></li>
        <li><span class="muted">Londrina/PR</span></li></ul></div>
    </div>
    <div class="footer__bottom"><span>© 2026 RW Company. Todos os direitos reservados.</span><span>Cases: {len(CASES)} projetos reais</span></div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp">{ico("whatsapp")}WhatsApp</a>
"""


def device(kind, base, widths, alt, a, sizes="(max-width: 680px) 90vw, 33vw"):
    if kind == "phone":
        return f'<div class="device-phone">{picture(base, widths, alt, "(max-width: 680px) 50vw, 230px", a)}</div>'
    if kind == "screen":
        return f'<div class="device-screen">{picture(base, widths, alt, "(max-width: 680px) 62vw, 300px", a)}</div>'
    if kind == "browser":
        return f'<div class="device-browser"><div class="device-browser__bar" aria-hidden="true"><i></i><i></i><i></i></div>{picture(base, widths, alt, sizes, a)}</div>'
    if kind == "phonevideo":
        return (f'<div class="device-phone"><video muted loop playsinline preload="none" data-inview poster="{a}assets/img/{base}-poster.webp" aria-label="{esc(alt)}">'
                f'<source data-src="{a}assets/video/{base}.webm" type="video/webm"><source data-src="{a}assets/video/{base}.mp4" type="video/mp4"></video></div>')
    if kind in ("phones", "phones3"):
        screens = ["dash", "previsao"] if kind == "phones" else ["dash", "previsao", "metas"]
        return '<div class="phones-duo">' + "".join(
            f'<div class="device-phone">{picture(f"{base}-{s}", [390, 780], alt, "(max-width: 680px) 40vw, 190px", a)}</div>' for s in screens) + "</div>"
    return ""


def case_card(c, a, i):
    kind, base, widths, alt = c["card_media"]
    if kind == "phonevideo":
        media = f'<div class="device-phone"><img src="{a}assets/img/{base}-poster.webp" alt="{esc(alt)}" loading="lazy" decoding="async" width="540" height="960"></div>'
    else:
        media = device(kind, base, widths, alt, a)
    wide = " case--wide" if c.get("wide") else ""
    new = '<span class="badge-new">NOVO</span>' if c.get("new") else ""
    return f"""<article class="case{wide}" data-cat="{c['cat']}" data-reveal style="--i:{i % 3}">
  {new}<div class="case__media">{media}</div>
  <div class="case__body">
    <p class="case__kicker">{esc(c['kicker'])}</p>
    <h3 class="case__title h-card"><a class="case__link" href="{case_href(c['slug'], a)}">{esc(c['name'])}</a></h3>
    <p class="case__text">{esc(c['short'])}</p>
    <div class="case__more"><span class="case__result">{esc(c['result'])}</span><span class="case__cta">Ver case {ico('arrow')}</span></div>
  </div>
</article>"""


def chat_phone(a, with_tabs):
    tabs = ""
    ig_panel = ""
    if with_tabs:
        tabs = f"""<div class="tabs" role="tablist" aria-label="Escolha o canal do agente">
          <button class="tab" role="tab" id="tab-wa" aria-controls="panel-wa" aria-selected="true">{ico('whatsapp')}WhatsApp</button>
          <button class="tab" role="tab" id="tab-ig" aria-controls="panel-ig" aria-selected="false" tabindex="-1">{ico('instagram')}Instagram</button>
        </div>"""
        ig_panel = f"""<div class="panel" id="panel-ig" role="tabpanel" aria-labelledby="tab-ig" hidden>
              <video muted loop playsinline preload="none" poster="{a}assets/img/agente-instagram-poster.webp" aria-label="Gravação real do agente da Horizonte 3D respondendo no direct do Instagram">
                <source data-src="{a}assets/video/agente-instagram.webm" type="video/webm"><source data-src="{a}assets/video/agente-instagram.mp4" type="video/mp4">
              </video>
            </div>"""
    return f"""<div class="ia__stage">
        {tabs}
        <div class="phone">
          <div class="phone__screen">
            <div class="phone__island" aria-hidden="true"></div>
            <div class="panel" id="panel-wa" {'role="tabpanel" aria-labelledby="tab-wa"' if with_tabs else 'role="region" aria-label="Conversa do agente de vendas da Truberpell no WhatsApp"'}>
              <div class="wa__head"><span class="wa__avatar"><img src="{a}assets/img/tp-avatar.webp" alt="" width="26" height="26"></span><span><span class="wa__name">Truberpell</span><br><span class="wa__status">online</span></span></div>
              <div class="wa__chat" aria-live="polite"></div>
            </div>
            {ig_panel}
          </div>
        </div>
        <button class="replay" type="button">{ico('repeat')}Ver a conversa de novo</button>
        <p class="ia__note">{'Conversas reais: agente de vendas da Truberpell no WhatsApp e agente da Horizonte 3D no Instagram (gravação acelerada). Dados de clientes ocultos.' if with_tabs else 'Conversa reproduzida a partir de um atendimento real da Truberpell. Dados do cliente ocultos.'}</p>
      </div>
      <script>window.RW_CHAT = {json.dumps(CHAT, ensure_ascii=False)};</script>"""


# ---------------------------------------------------------------- home
def build_home():
    a = ""
    tiles = [
        ("ia", "bot", "Inteligência artificial e agentes de IA",
         "Agentes que atendem no WhatsApp e no Instagram, qualificam leads, fazem orçamento e geram link de pagamento.",
         "Atendimento que não para e leads que chegam prontos."),
        ("sites", "browser", "Sites e landing pages",
         "Sites rápidos e profissionais, feitos para transformar visita em contato.",
         "Sua empresa apresentada com a credibilidade que ela tem."),
        ("mkt", "megaphone", "Marketing digital, publicidade e tráfego pago",
         "Posicionamento, conteúdo, gestão de perfil e campanhas no Meta e no Google focadas em lead e venda, não em curtida.",
         "Marca lembrada e escolhida."),
        ("auto", "flow", "Automação comercial",
         "Processos repetitivos rodando sozinhos, integrados ao seu CRM e às ferramentas que você já usa.",
         "Sua equipe livre para o que importa."),
        ("sistemas", "app", "Sistemas e aplicativos personalizados",
         "Aplicativos para organizar a operação: estoque, financeiro, vendas e o que o seu negócio precisar.",
         "Processos organizados, menos planilha solta."),
        ("prospec", "radar", "Prospecção e soluções de vendas",
         "Ferramentas que encontram empresas no Google com telefone e endereço para a sua equipe comercial abordar.",
         "Mais oportunidades entrando no funil."),
    ]
    tile_html = []
    for i, (k, ic, t, d, b) in enumerate(tiles):
        art = ""
        if k == "ia":
            art = ('<div class="tile__art" aria-hidden="true"><div class="mini-bubble mini-bubble--me">Vocês fazem placas personalizadas?</div>'
                   '<div class="mini-bubble">Fazemos sim, sob medida. Você precisa de quantas unidades?</div><div class="mini-bubble mini-bubble--me">10 unidades, por favor</div><div class="mini-bubble mini-bubble--typing"><i></i><i></i><i></i></div></div>')
        if k == "sites":
            art = f'<div class="tile__art" aria-hidden="true"><img src="{a}assets/img/horizonte-site-640.webp" width="640" height="400" alt="" loading="lazy" decoding="async"></div>'
        cls = {"ia": "tile--ia", "sites": "tile--sites", "sistemas": "tile--sistemas", "prospec": "tile--prospec"}.get(k, "")
        tile_html.append(f"""<article class="tile {cls}" data-reveal style="--i:{i % 3}">
        <span class="tile__ico">{ico(ic)}</span>{art}
        <h3 class="h-card">{t}</h3><p>{d}</p><p class="tile__benefit">{b}</p>
      </article>""")

    filters = [("all", "Todos"), ("marketing", "Marketing"), ("sites", "Sites"), ("ia", "Agentes de IA"), ("apps", "Apps e sistemas")]
    benefits = [
        ("bot", "Atendimento automatizado", "No WhatsApp e no Instagram, com a linguagem da sua empresa."),
        ("clock", "Disponível 24 horas", "Responde de madrugada, no fim de semana e no feriado."),
        ("filter", "Qualificação de leads", "Pergunta o que importa e entrega o contato pronto para a venda."),
        ("link", "Integração comercial", "Orçamento, link de pagamento e registro no CRM."),
        ("repeat", "Menos tarefa repetitiva", "Sua equipe deixa de responder a mesma pergunta o dia inteiro."),
        ("scale", "Escala sem fila", "Atende várias conversas ao mesmo tempo, sem deixar ninguém esperando."),
    ]
    steps = [
        ("01", "Entendemos seu negócio", "Diagnóstico: seus números, sua operação e onde estão as oportunidades."),
        ("02", "Planejamos a solução", "Montamos o plano com canais, ferramentas e metas claras."),
        ("03", "Desenvolvemos a tecnologia", "Colocamos tudo no ar: conteúdo, campanhas, site, sistemas e agentes de IA."),
        ("04", "Evoluímos juntos", "Medimos, ajustamos e reportamos resultado toda semana."),
    ]
    diffs = [
        ("puzzle", "Soluções sob medida", "Cada projeto parte do problema do cliente, não de um pacote pronto."),
        ("layers", "Marketing + tecnologia", "Estratégia, execução e desenvolvimento no mesmo time."),
        ("target", "Orientado ao seu negócio", "Construímos o que a sua operação precisa para vender e organizar."),
        ("handshake", "Atendimento consultivo", "Conversa direta com quem desenvolve, do diagnóstico ao acompanhamento."),
    ]

    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "RW Company", "url": DOMAIN + "/", "inLanguage": "pt-BR"}]
    page = head("RW Company | Tecnologia, IA e marketing para empresas",
                "Unimos tecnologia, inteligência artificial, marketing e desenvolvimento para transformar desafios empresariais em soluções digitais. Londrina/PR.",
                "/", a, extra_ld=ld)
    page += f"""<body>
{sprite()}
{header(a, True)}
<main id="conteudo">

  <!-- 1. HERO -->
  <section class="hero" id="topo" aria-labelledby="hero-title">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="hero__grid" aria-hidden="true"></div>
    <video class="hero__video" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1">
      <source data-src="assets/video/hero-loop.webm" type="video/webm"><source data-src="assets/video/hero-loop.mp4" type="video/mp4">
    </video>
    <div class="hero__shade" aria-hidden="true"></div>
    <svg class="hero__orbit" viewBox="0 0 400 400" aria-hidden="true"><circle cx="200" cy="200" r="196"/><circle class="dash" cx="200" cy="200" r="150"/><circle cx="200" cy="200" r="96"/></svg>
    <div class="container">
      <div class="hero__content">
        <p class="eyebrow hero-in" style="--i:0">Tecnologia · IA · Marketing · Londrina/PR</p>
        <h1 class="hero__title display h-hero" id="hero-title">
          <span class="mask"><span style="--i:1">O futuro do</span></span>
          <span class="mask"><span style="--i:2">seu negócio</span></span>
          <span class="mask"><span style="--i:3">começa <span class="accent">aqui.</span></span></span>
        </h1>
        <p class="lead hero-in" style="--i:5">Unimos tecnologia, inteligência artificial, marketing e desenvolvimento para transformar desafios empresariais em soluções digitais.</p>
        <div class="hero__actions hero-in" style="--i:6">
          <a class="btn btn--primary btn--lg" href="#cases">Conheça nossos projetos {ico('arrow', 'arrow')}</a>
          <a class="btn btn--ghost btn--lg" href="{wa()}" target="_blank" rel="noopener">Fale com um especialista</a>
        </div>
        <button class="hero__play hero-in" style="--i:7" type="button" data-open-video><span class="hero__play-ico">{ico('play')}</span>Assista ao nosso vídeo · 56 s</button>
      </div>
    </div>
    <div class="hero__proof hero-in" style="--i:8" aria-label="Resultados reais">
      <div class="chip-proof"><b>+41%</b><span>seguidores em 7 dias<br>Aurora Sobremesas</span></div>
      <div class="chip-proof"><b>24h</b><span>agente de IA atendendo<br>Truberpell</span></div>
    </div>
    <a class="scroll-cue" href="#sobre" aria-label="Role para a próxima seção"><span>ROLE</span><i></i></a>
  </section>

  <!-- 2. QUEM SOMOS -->
  <section class="section" id="sobre" aria-labelledby="sobre-title">
    <div class="container about">
      <div class="about__text">
        <p class="eyebrow" data-reveal>Quem somos</p>
        <h2 class="display h-section about__title mask-group" id="sobre-title">
          <span class="mask"><span style="--i:0">Mais que</span></span><span class="mask"><span style="--i:1">tecnologia.</span></span>
        </h2>
        <p class="lead" data-reveal><strong style="color:#fff;font-weight:600">Soluções que fazem negócios evoluírem.</strong> A RW Company é a parceira de transformação digital de empresas que querem vender mais e trabalhar melhor.</p>
        <p class="muted" data-reveal style="--i:1">Você não precisa contratar cinco fornecedores. Estratégia, execução e tecnologia ficam no mesmo time, do primeiro post ao último lead fechado.</p>
        <div class="about__stats" data-reveal style="--i:2">
          <div><b>{len(CASES)}</b><span>projetos reais neste portfólio</span></div>
          <div><b>3</b><span>canais de atendimento com IA:<br>WhatsApp, Instagram e site</span></div>
        </div>
      </div>
      <div class="pillars">
        <article class="pillar" data-reveal style="--i:0">{ico('puzzle')}<h3>Soluções personalizadas</h3><p>Sites, sistemas e apps feitos para a operação de cada cliente.</p></article>
        <article class="pillar" data-reveal style="--i:1">{ico('bot')}<h3>Inteligência artificial e automação</h3><p>Agentes que atendem, qualificam e orçam; processos que rodam sozinhos.</p></article>
        <article class="pillar" data-reveal style="--i:2">{ico('megaphone')}<h3>Marketing e posicionamento</h3><p>Conteúdo, redes sociais e tráfego pago para a marca ser escolhida.</p></article>
        <article class="pillar" data-reveal style="--i:3">{ico('chart')}<h3>Tecnologia nos processos comerciais</h3><p>Prospecção, CRM e orçamento conectados para vender com menos esforço.</p></article>
      </div>
    </div>
  </section>

  <!-- 3. SOLUÇÕES -->
  <section class="section" id="solucoes" aria-labelledby="sol-title" style="padding-bottom:0">
    <div class="container">
      <div class="sec-head">
        <div><p class="eyebrow" data-reveal>Nossas soluções</p><h2 class="display h-section mask-group" id="sol-title"><span class="mask"><span>O que nós fazemos</span></span></h2></div>
        <p class="lead" data-reveal>Seis frentes que se conectam. Você escolhe por onde começar.</p>
      </div>
      <div class="bento">
        {"".join(tile_html)}
      </div>
    </div>
    <div class="container connector" aria-hidden="true">
      <svg viewBox="0 0 1000 200" preserveAspectRatio="none">
        <defs><linearGradient id="cgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d97ff" stop-opacity="0"/><stop offset="1" stop-color="#7d97ff"/></linearGradient></defs>
        <path style="--i:0;--len:620" d="M125 0 C125 120 500 80 500 200"/>
        <path style="--i:1;--len:520" d="M375 0 C375 110 500 90 500 200"/>
        <path style="--i:1;--len:520" d="M625 0 C625 110 500 90 500 200"/>
        <path style="--i:0;--len:620" d="M875 0 C875 120 500 80 500 200"/>
      </svg>
      <span class="node"><img src="assets/img/logo-96.webp" width="30" height="35" alt=""></span>
    </div>
  </section>

  <!-- 4. PORTFÓLIO -->
  <section class="section" id="cases" aria-labelledby="cases-title" style="padding-top:clamp(56px,7vw,96px)">
    <div class="container">
      <div class="sec-head">
        <div><p class="eyebrow" data-reveal>Portfólio</p><h2 class="display h-section mask-group" id="cases-title"><span class="mask"><span style="--i:0">Projetos reais.</span></span><span class="mask"><span style="--i:1" class="accent">Soluções que fazem a diferença.</span></span></h2></div>
      </div>
      <div class="filters" role="group" aria-label="Filtrar projetos">
        {"".join(f'<button class="filter" type="button" data-filter="{k}" aria-pressed="{str(k == "all").lower()}">{t}</button>' for k, t in filters)}
      </div>
      <p class="sr-only" id="filter-status" aria-live="polite"></p>
      <div class="cases">
        {"".join(case_card(c, a, i) for i, c in enumerate(CASES))}
      </div>
    </div>
  </section>

  <!-- 5. INTELIGÊNCIA ARTIFICIAL -->
  <section class="section ia" id="ia" aria-labelledby="ia-title">
    <div class="container ia__grid">
      {chat_phone(a, True)}
      <div>
        <p class="eyebrow" data-reveal>Agentes de IA</p>
        <h2 class="display h-section mask-group" id="ia-title" style="margin-top:16px"><span class="mask"><span style="--i:0">Sua empresa mais inteligente.</span></span><span class="mask"><span style="--i:1" class="accent">Seu tempo mais valioso.</span></span></h2>
        <ul class="benefits">
          {"".join(f'<li class="benefit" data-reveal style="--i:{i % 2}">{ico(ic)}<span><b>{t}</b><span>{d}</span></span></li>' for i, (ic, t, d) in enumerate(benefits))}
        </ul>
        <a class="btn btn--primary btn--lg" href="{wa('Olá! Vim pelo site da RW Company e quero automatizar o atendimento da minha empresa.')}" target="_blank" rel="noopener" data-reveal>Quero automatizar minha empresa {ico('arrow', 'arrow')}</a>
      </div>
    </div>
  </section>

  <!-- 6. PROCESSO -->
  <section class="section" id="processo" aria-labelledby="proc-title">
    <div class="container">
      <div class="sec-head">
        <div><p class="eyebrow" data-reveal>Nosso processo</p><h2 class="display h-section mask-group" id="proc-title"><span class="mask"><span>Da ideia à solução.</span></span></h2></div>
        <p class="lead" data-reveal>Quatro etapas, com acompanhamento semanal depois que tudo está no ar.</p>
      </div>
      <ol class="timeline">
        <li class="timeline__rail" aria-hidden="true"><span class="timeline__fill"></span></li>
        {"".join(f'<li class="step" data-reveal><span class="step__n" aria-hidden="true">{n}</span><h3><span class="sr-only">Etapa {n}: </span>{t}</h3><p>{d}</p></li>' for n, t, d in steps)}
      </ol>
    </div>
  </section>

  <!-- 7. RESULTADOS -->
  <section class="section" id="resultados" aria-labelledby="res-title" style="padding-top:0">
    <div class="container">
      <div class="sec-head">
        <div><p class="eyebrow" data-reveal>Resultados e diferenciais</p><h2 class="display h-section mask-group" id="res-title"><span class="mask"><span>Números de verdade.</span></span></h2></div>
        <p class="lead" data-reveal>Só publicamos o que está documentado nos projetos.</p>
      </div>
      <div class="numbers">
        <div class="number" data-reveal style="--i:0"><b><span class="accent">+</span><span data-to="41">41</span>%</b><span>seguidores em 7 dias · Aurora Sobremesas</span></div>
        <div class="number" data-reveal style="--i:1"><b><span data-from="1700" data-to="2400">2.400</span></b><span>seguidores no Instagram da Aurora (eram 1.700)</span></div>
        <div class="number" data-reveal style="--i:2"><b><span data-to="24">24</span>h</b><span>de atendimento do agente de IA da Truberpell</span></div>
        <div class="number" data-reveal style="--i:3"><b><span data-to="{len(CASES)}">{len(CASES)}</span></b><span>projetos reais apresentados neste portfólio</span></div>
      </div>
      <div class="diffs">
        {"".join(f'<article class="diff" data-reveal style="--i:{i}">{ico(ic)}<h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(diffs))}
      </div>
    </div>
  </section>

  <!-- 8. CTA FINAL -->
  <section class="final" id="contato" aria-labelledby="cta-title">
    <img class="final__mark" src="assets/img/logo-480.webp" width="480" height="563" alt="" loading="lazy" decoding="async">
    <div class="container">
      <p class="eyebrow" data-reveal>Vamos conversar</p>
      <h2 class="display h-section final__title mask-group" id="cta-title"><span class="mask"><span style="--i:0">O próximo passo</span></span><span class="mask"><span style="--i:1">da sua empresa</span></span><span class="mask"><span style="--i:2" class="accent">começa com uma conversa.</span></span></h2>
      <p class="lead" data-reveal>Conte seu desafio. Vamos descobrir juntos como a tecnologia pode transformar seu negócio.</p>
      <div class="final__actions" data-reveal>
        <a class="btn btn--light btn--lg" href="{wa()}" target="_blank" rel="noopener">{ico('whatsapp')}Vamos conversar</a>
      </div>
      <div class="final__contacts" data-reveal>
        <a href="{wa()}" target="_blank" rel="noopener">{ico('whatsapp')}{PHONE_LABEL}</a>
        <a href="mailto:{EMAIL}">{ico('mail')}{EMAIL}</a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener">{ico('instagram')}@rw.companyy</a>
        <span style="display:inline-flex;align-items:center;gap:8px;min-height:44px">{ico('pin')}Londrina/PR</span>
      </div>
    </div>
  </section>
</main>
{footer(a, True)}
<dialog class="vmodal" id="vmodal" aria-label="Vídeo institucional da RW Company">
  <button class="vmodal__close" type="button" aria-label="Fechar vídeo">{ico('close')}</button>
  <video controls playsinline preload="none" data-src="assets/video/rw-reels.mp4" poster="assets/img/reels-poster.webp"></video>
</dialog>
<script src="assets/js/site.min.js" defer></script>
</body>
</html>
"""
    if PREVIEW:
        # O preview publicado recebe o esqueleto da plataforma: sai sem doctype/html/head/body.
        import re
        head_inner = re.search(r"<head>(.*?)</head>", page, re.S).group(1)
        head_inner = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>|<title>.*?</title>', "", head_inner)
        body_inner = re.search(r"<body>(.*)</body>", page, re.S).group(1)
        page = "<title>Portfólio RW Company</title>\n" + head_inner.strip() + "\n" + body_inner
    (OUT / "index.html").write_text(page, encoding="utf-8")


# ---------------------------------------------------------------- páginas de case
def build_case(i, c):
    a = "../../"
    path = f"/cases/{c['slug']}/"
    prev_c, next_c = CASES[i - 1], CASES[(i + 1) % len(CASES)]
    home = a + ("index.html" if PREVIEW else "")
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Cases", "item": DOMAIN + "/#cases"},
        {"@type": "ListItem", "position": 3, "name": c["name"], "item": DOMAIN + path}]},
        {"@context": "https://schema.org", "@type": "CreativeWork", "name": c["name"], "about": c["kicker"],
         "description": c["short"], "creator": {"@type": "Organization", "name": "RW Company", "url": DOMAIN + "/"}, "inLanguage": "pt-BR"}]
    media_html = []
    for m in c["media"]:
        kind = m[0]
        if kind == "video":
            _, base, alt = m
            media_html.append(f'<div class="device-phone"><video muted loop playsinline preload="none" data-inview poster="{a}assets/img/{base}-poster.webp" aria-label="{esc(alt)}"><source data-src="{a}assets/video/{base}.webm" type="video/webm"><source data-src="{a}assets/video/{base}.mp4" type="video/mp4"></video></div>')
        elif kind == "chat":
            media_html.append("CHAT")
        elif kind == "image":
            _, base, widths, alt = m
            media_html.append(f'<figure style="margin:0;max-width:1002px;border-radius:14px;overflow:hidden;border:1px solid var(--line-2)">{picture(base, widths, alt, "(max-width: 1100px) 92vw, 1002px", a)}</figure>')
        else:
            _, base, widths, alt = m
            media_html.append(device(kind, base, widths, alt, a, "(max-width: 1100px) 92vw, 1080px"))
    # monta blocos: telefones lado a lado, navegadores em blocos próprios
    blocks = []
    row = []
    for h in media_html:
        if h == "CHAT":
            blocks.append(f'<div class="case-media ia" style="border:0">{chat_phone(a, False)}</div>')
            continue
        if 'device-phone' in h and 'phones-duo' not in h:
            row.append(h)
        else:
            if row:
                blocks.append('<div class="case-media"><div class="media-row">' + "".join(row) + "</div></div>"); row = []
            blocks.append(f'<div class="case-media">{h}</div>')
    if row:
        blocks.append('<div class="case-media"><div class="media-row">' + "".join(row) + "</div></div>")
    note = f'<p class="note">{esc(c["note"])}</p>' if c.get("note") else ""
    tech = ('<div class="tags">' + "".join(f'<span class="tag">{esc(t)}</span>' for t in c["tech"]) + "</div>") if c.get("tech") else "<span class=\"muted\">Não divulgado</span>"
    link = f'<a href="{c["link"][1]}" target="_blank" rel="noopener">{esc(c["link"][0])} ↗</a>' if c.get("link") else esc(c["status"])
    result = (f'<div class="result-box" data-reveal><b>{esc(c["result_big"])}</b><p>{esc(c["result_text"])}</p></div>' if c.get("result_big")
              else f'<div class="result-box result-box--plain" data-reveal><p>{esc(c["result_text"])}</p></div>')
    page = head(f"{c['name']} | Case RW Company", c["short"], path, a, og_type="article", extra_ld=ld)
    page += f"""<body>
{sprite()}
{header(a, False)}
<main id="conteudo">
  <section class="case-hero">
    <div class="container">
      <nav class="crumbs" aria-label="Você está em"><a href="{home}">Início</a><span aria-hidden="true">/</span><a href="{home}#cases">Cases</a><span aria-hidden="true">/</span><span aria-current="page">{esc(c['name'])}</span></nav>
      <p class="eyebrow hero-in">{esc(c['kicker'])}</p>
      <h1 class="display mask-group"><span class="mask"><span>{esc(c['name'])}</span></span></h1>
      <p class="lead hero-in" style="--i:2">{esc(c['short'])}</p>
      <dl class="meta hero-in" style="--i:3">
        <div><dt>Cliente</dt><dd>{esc(c['client'])}</dd></div>
        <div><dt>Serviços</dt><dd>{esc(' · '.join(c['services']))}</dd></div>
        <div><dt>Tecnologias</dt><dd>{tech}</dd></div>
        <div><dt>{'Link' if c.get('link') else 'Status'}</dt><dd>{link}</dd></div>
      </dl>
    </div>
  </section>
  <div class="container">
    {"".join(blocks)}
    {note}
    <div class="case-cols">
      <h2 class="display" data-reveal>Desafio</h2>
      <div class="prose" data-reveal>{"".join(f"<p>{esc(p)}</p>" for p in c['challenge'])}</div>
    </div>
    <div class="case-cols">
      <h2 class="display" data-reveal>Solução</h2>
      <div class="prose" data-reveal>{"".join(f"<p>{esc(p)}</p>" for p in c['solution'])}<ul>{"".join(f"<li>{esc(d)}</li>" for d in c['delivered'])}</ul></div>
    </div>
    {result}
    <div class="case-cta" data-reveal>
      <h2 class="display">Quer algo assim na sua empresa?</h2>
      <a class="btn btn--primary btn--lg" href="{wa(f'Olá! Vi o case {c["name"]} no site da RW Company e quero conversar.')}" target="_blank" rel="noopener">Vamos conversar {ico('arrow', 'arrow')}</a>
    </div>
    <nav class="next-case" aria-label="Outros cases">
      <a href="{case_href(prev_c['slug'], a)}"><small>← Case anterior</small><span>{esc(prev_c['name'])}</span></a>
      <a href="{case_href(next_c['slug'], a)}"><small>Próximo case →</small><span>{esc(next_c['name'])}</span></a>
    </nav>
  </div>
</main>
{footer(a, False)}
<script src="{a}assets/js/site.min.js" defer></script>
</body>
</html>
"""
    d = OUT / "cases" / c["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(page, encoding="utf-8")


def build_meta():
    urls = ["/"] + [f"/cases/{c['slug']}/" for c in CASES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{DOMAIN}{u}</loc><changefreq>monthly</changefreq><priority>{'1.0' if u == '/' else '0.7'}</priority></url>" for u in urls]
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "RW Company", "short_name": "RW Company", "start_url": "/", "display": "browser",
        "background_color": "#07090F", "theme_color": "#07090F", "lang": "pt-BR",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "vercel.json").write_text(json.dumps({
        "cleanUrls": True, "trailingSlash": True,
        "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}, indent=2), encoding="utf-8")


def minify():
    """CSS e JS editáveis ficam em site.css / site.js; o site carrega as versões minificadas."""
    import subprocess
    a = ROOT / "site" / "assets"
    subprocess.run(["npx", "-y", "esbuild@0.24.0", str(a / "css/site.css"), "--minify", f"--outfile={a / 'css/site.min.css'}", "--log-level=warning"], check=True)
    subprocess.run(["npx", "-y", "esbuild@0.24.0", str(a / "js/site.js"), "--minify", "--target=es2017", f"--outfile={a / 'js/site.min.js'}", "--log-level=warning"], check=True)


if __name__ == "__main__":
    minify()
    SRC = ROOT / "site"
    OUT_ASSETS = SRC / "assets"
    if PREVIEW:
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.copytree(SRC / "assets", OUT / "assets")
    OUT.mkdir(exist_ok=True)
    build_home()
    for i, c in enumerate(CASES):
        build_case(i, c)
    build_meta()
    print("ok ->", OUT)
