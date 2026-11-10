import os
import base64
import subprocess
import tempfile
from pathlib import Path
import pypdf

# Load profile image as base64
img_path = Path("assets/profile.jpg")
if img_path.exists():
    with open(img_path, "rb") as f:
        img_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
else:
    img_b64 = ""

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Currículo: Cauã Gustavo da Silva Bernardino</title>
<style>
  @page {{
    size: A4;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #f1f5f9;
    font-size: 8.8pt;
    line-height: 1.4;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* PAGE CONTAINER */
  .page {{
    width: 210mm;
    min-height: 297mm;
    height: 297mm;
    margin: 0 auto;
    background: #ffffff;
    padding: 11mm 13mm 11mm 13mm;
    position: relative;
    page-break-after: always;
    box-sizing: border-box;
    overflow: hidden;
  }}

  /* TOP DECORATIVE ACCENT */
  .top-bar {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #0284c7, #38bdf8, #0369a1);
  }}

  /* HEADER PAGE 1 */
  .header-p1 {{
    text-align: center;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1.5px solid #e2e8f0;
  }}
  .avatar {{
    width: 78px;
    height: 78px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #0284c7;
    box-shadow: 0 4px 10px rgba(2, 132, 199, 0.2);
    display: inline-block;
    margin-bottom: 5px;
  }}
  .name {{
    font-size: 16.5pt;
    font-weight: 800;
    letter-spacing: 2px;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 2px;
  }}
  .role {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #0284c7;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .quote {{
    font-size: 8pt;
    font-style: italic;
    color: #475569;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.35;
  }}

  /* HEADER PAGE 2 (COMPACT) */
  .header-p2 {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    margin-bottom: 11px;
    border-bottom: 1.5px solid #e2e8f0;
  }}
  .header-p2-name {{
    font-size: 10.8pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  .header-p2-role {{
    font-size: 8.2pt;
    font-weight: 700;
    color: #0284c7;
  }}
  .header-p2-contact {{
    font-size: 7.6pt;
    color: #64748b;
    text-align: right;
    line-height: 1.35;
  }}

  /* TWO-COLUMN LAYOUT */
  .layout {{
    display: flex;
    gap: 16px;
    height: calc(100% - 146px);
  }}
  .layout-p2 {{
    display: flex;
    gap: 16px;
    height: calc(100% - 42px);
  }}

  /* LEFT SIDEBAR (32%) */
  .sidebar {{
    width: 32%;
    border-right: 1.5px solid #e2e8f0;
    padding-right: 13px;
    display: flex;
    flex-direction: column;
    gap: 9px;
  }}

  /* RIGHT MAIN (68%) */
  .main {{
    width: 68%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  /* SECTION TITLE (NO EMOJIS, CLEAN & PROFESSIONAL) */
  .section-title {{
    font-size: 8.8pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding-bottom: 3px;
    border-bottom: 2px solid #0284c7;
    margin-bottom: 5px;
  }}

  /* CONTACT LIST */
  .contact-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 3.5px;
    font-size: 7.8pt;
  }}
  .contact-item {{
    display: flex;
    flex-direction: column;
    gap: 1px;
    color: #334155;
    word-break: break-all;
  }}
  .c-label {{
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #0284c7;
    letter-spacing: 0.5px;
  }}
  .c-val {{
    font-size: 7.8pt;
    color: #334155;
  }}
  .contact-item a {{
    color: #0284c7;
    text-decoration: none;
    font-weight: 600;
  }}

  /* SUMMARY */
  .summary-text {{
    font-size: 7.9pt;
    color: #334155;
    line-height: 1.38;
    text-align: justify;
  }}

  /* SKILL GROUPS */
  .skill-group {{
    margin-bottom: 5px;
  }}
  .skill-group-title {{
    font-size: 7.8pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2.5px;
  }}
  .skill-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
  }}
  .skill-tag {{
    font-size: 7pt;
    padding: 1px 5px;
    background: #f1f5f9;
    color: #334155;
    border-radius: 3px;
    font-weight: 600;
    border: 1px solid #e2e8f0;
  }}
  .skill-tag.accent {{
    background: #e0f2fe;
    color: #0369a1;
    border-color: #bae6fd;
  }}

  /* TIMELINE JOBS */
  .timeline-item {{
    margin-bottom: 8px;
    padding-left: 9px;
    border-left: 2px solid #cbd5e1;
    position: relative;
  }}
  .timeline-item:last-child {{
    margin-bottom: 0;
  }}
  .job-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1px;
  }}
  .job-title {{
    font-size: 9pt;
    font-weight: 800;
    color: #0f172a;
  }}
  .job-date {{
    font-size: 7.3pt;
    font-weight: 700;
    color: #0284c7;
    background: #e0f2fe;
    padding: 1px 6px;
    border-radius: 999px;
    white-space: nowrap;
  }}
  .job-company {{
    font-size: 8.1pt;
    font-weight: 600;
    color: #475569;
    margin-bottom: 2.5px;
  }}
  .job-company span {{
    color: #64748b;
    font-weight: 400;
  }}
  .job-bullets {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 2.5px;
    font-size: 7.9pt;
    color: #334155;
  }}
  .job-bullets li {{
    position: relative;
    padding-left: 9px;
    line-height: 1.35;
  }}
  .job-bullets li::before {{
    content: "•";
    color: #0284c7;
    font-weight: bold;
    position: absolute;
    left: 0;
  }}

  /* PROJECT CARDS */
  .proj-list {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .proj-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 5.5px 8.5px;
  }}
  .proj-title {{
    font-size: 8.4pt;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
  }}
  .proj-status {{
    font-size: 6.3pt;
    font-weight: 700;
    color: #0369a1;
    background: #e0f2fe;
    padding: 1px 5px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .proj-desc {{
    font-size: 7.6pt;
    color: #475569;
    line-height: 1.32;
    margin-bottom: 2.5px;
  }}
  .proj-techs {{
    font-size: 7pt;
    color: #0284c7;
    font-weight: 600;
  }}

  /* CERTIFICATIONS LIST */
  .cert-list {{
    display: flex;
    flex-direction: column;
    gap: 4.5px;
  }}
  .cert-item {{
    font-size: 7.7pt;
  }}
  .cert-name {{
    font-weight: 700;
    color: #0f172a;
    line-height: 1.25;
  }}
  .cert-org {{
    color: #0284c7;
    font-weight: 600;
    font-size: 7.2pt;
  }}
</style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="page">
    <div class="top-bar"></div>

    <!-- HEADER -->
    <div class="header-p1">
      <img src="{img_b64}" alt="Cauã Gustavo da Silva Bernardino" class="avatar" />
      <h1 class="name">Cauã Gustavo da Silva Bernardino</h1>
      <div class="role">Estudante de Engenharia da Computação · 6º Período (Faculdade Multivix Vitória)</div>
      <p class="quote">
        "Onde há processos a serem otimizados, eu e minha equipe entramos, organizamos a operação e transformamos tecnologia em realidade e resultado comercial."
      </p>
    </div>

    <!-- LAYOUT PAGE 1 -->
    <div class="layout">

      <!-- LEFT SIDEBAR -->
      <div class="sidebar">

        <!-- CONTATO -->
        <div>
          <div class="section-title">Contato</div>
          <ul class="contact-list">
            <li class="contact-item">
              <span class="c-label">Telefone / WhatsApp</span>
              <span class="c-val"><strong>+55 (27) 99781-7164</strong></span>
            </li>
            <li class="contact-item">
              <span class="c-label">E-mail</span>
              <span class="c-val"><strong>cauag1834@gmail.com</strong></span>
            </li>
            <li class="contact-item">
              <span class="c-label">Localização</span>
              <span class="c-val">Vitória/ES | Bairro Nova Palestina (CEP: 29032-364)</span>
            </li>
            <li class="contact-item">
              <span class="c-label">LinkedIn</span>
              <span class="c-val"><a href="https://www.linkedin.com/in/cau%C3%A3-gustavo-da-silva-bernardino-455005304/" target="_blank">linkedin.com/in/caua-gustavo</a></span>
            </li>
            <li class="contact-item">
              <span class="c-label">GitHub</span>
              <span class="c-val"><a href="https://github.com/cauag1834-maker" target="_blank">github.com/cauag1834-maker</a></span>
            </li>
            <li class="contact-item">
              <span class="c-label">Portfólio & Plataformas</span>
              <span class="c-val"><a href="https://workflow.app.br" target="_blank">workflow.app.br / meu-perfil-caua-g</a></span>
            </li>
          </ul>
        </div>

        <!-- PERFIL PROFISSIONAL -->
        <div>
          <div class="section-title">Perfil Profissional</div>
          <p class="summary-text">
            Graduando em <strong>Engenharia da Computação (6º período) na Multivix Vitória</strong>, com sólida atuação prática em <strong>Organização Empresarial</strong>, <strong>Otimização de Processos Comerciais</strong> e <strong>Desenvolvimento Full Stack / Integração de APIs</strong>.
          </p>
          <p class="summary-text" style="margin-top: 4px;">
            Experiência em ecossistemas SaaS multi-tenant, gateways de mensageria com automação de WhatsApp, funções serverless com <strong>Supabase (Edge Functions)</strong> e inteligência artificial aplicada aos negócios (<strong>Google Gemini</strong>). Capacidade comprovada em alinhar visão de engenharia à entrega de resultados comerciais.
          </p>
        </div>

        <!-- COMPETÊNCIAS TÉCNICAS -->
        <div>
          <div class="section-title">Habilidades Técnicas</div>

          <div class="skill-group">
            <div class="skill-group-title">Linguagens & Frameworks</div>
            <div class="skill-tags">
              <span class="skill-tag accent">TypeScript</span>
              <span class="skill-tag accent">JavaScript ES6+</span>
              <span class="skill-tag accent">Next.js 14</span>
              <span class="skill-tag">FlutterFlow</span>
              <span class="skill-tag">React</span>
              <span class="skill-tag">Node.js</span>
              <span class="skill-tag">C++</span>
              <span class="skill-tag">HTML5 / CSS3</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">APIs, Supabase & Back-end</div>
            <div class="skill-tags">
              <span class="skill-tag accent">Supabase (Edge Functions)</span>
              <span class="skill-tag accent">PostgreSQL / RLS</span>
              <span class="skill-tag accent">APIs RESTful</span>
              <span class="skill-tag">Webhooks Idempotentes</span>
              <span class="skill-tag">WhatsApp API (WAHA)</span>
              <span class="skill-tag">Hubla & Hotmart</span>
              <span class="skill-tag">URA de Atendimento</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Inteligência Artificial & Dados</div>
            <div class="skill-tags">
              <span class="skill-tag accent">Google Gemini API</span>
              <span class="skill-tag accent">Prompt Engineering</span>
              <span class="skill-tag">Power BI</span>
              <span class="skill-tag">Excel Avançado</span>
              <span class="skill-tag">Validação / Filtro de Leads</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Cloud, Infra & Hardware</div>
            <div class="skill-tags">
              <span class="skill-tag accent">Hostinger VPS (Linux)</span>
              <span class="skill-tag accent">Docker Containers</span>
              <span class="skill-tag">Montagem & Suporte de Hardware</span>
              <span class="skill-tag">Redes & Protocolos</span>
              <span class="skill-tag">Vercel & Cloudflare</span>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT MAIN (EXPERIÊNCIA) -->
      <div class="main">

        <div>
          <div class="section-title">Experiência Profissional</div>

          <!-- GOOGLE AMBASSADOR -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Google Student Ambassador</div>
              <div class="job-date">Ago. 2026 a Presente</div>
            </div>
            <div class="job-company">Google for Education & Amplifica <span>· Remoto / Nacional</span></div>
            <ul class="job-bullets">
              <li>Selecionado nacionalmente para representar e disseminar soluções de <strong>Inteligência Artificial Generativa (Google Gemini)</strong> e ecossistema Google Workspace.</li>
              <li>Condução de workshops acadêmicos e treinamentos práticos sobre aplicação de LLMs e ferramentas de automação na rotina educacional e corporativa.</li>
            </ul>
          </div>

          <!-- WORKFLOW APP / BUSINESS -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Suporte Técnico & Analista de Integração / Atendimento Multicanal</div>
              <div class="job-date">Jun. 2025 a Presente</div>
            </div>
            <div class="job-company">Workflow App / Business <span>· Vitória/ES (Remoto / Presencial)</span></div>
            <ul class="job-bullets">
              <li>Desenvolvimento e implementação de <strong>integrações de APIs em JavaScript e TypeScript</strong>, conectando o sistema central a CRMs, WordPress, URA de atendimento e plataformas de clínicas.</li>
              <li>Estruturação e automação de microsserviços no <strong>Supabase</strong>, criando <strong>Edge Functions serverless</strong>, regras de autenticação e rotinas com banco de dados.</li>
              <li>Integração completa de checkout e webhook com <strong>Hubla</strong>: disparo automático de mensagens no WhatsApp para recuperação de carrinho abandonado e envio imediato de acessos pós-pagamento.</li>
              <li>Desenvolvimento de sistema interno para teste e filtragem de contatos WhatsApp: higienização de listas ativas/inativas para download e disparos com alta entregabilidade.</li>
              <li>Atuação inicial no suporte multicanal a usuários com transição e ascensão direta para engenharia e automações de fluxos.</li>
            </ul>
          </div>

          <!-- POLÍCIA MILITAR (PROJETO ACADÊMICO VET) -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Desenvolvedor de Software (FlutterFlow) · Projeto Acadêmico</div>
              <div class="job-date">Projeto Prático</div>
            </div>
            <div class="job-company">Polícia Militar / Atividade Prática Acadêmica <span>· Vitória/ES</span></div>
            <ul class="job-bullets">
              <li>Desenvolvimento de aplicação Web voltada ao setor veterinário da corporação policial utilizando <strong>FlutterFlow</strong> e banco de dados integrado.</li>
              <li>Implementação de rotinas de cálculo automático de doses de vacinas/medicamentos e geração/armazenamento de relatórios veterinários operacionais.</li>
            </ul>
          </div>

          <!-- OK BANK -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Correspondente Bancário & Vendas</div>
              <div class="job-date">Set. 2024 a Fev. 2025</div>
            </div>
            <div class="job-company">OK BANK <span>· 6 meses</span></div>
            <ul class="job-bullets">
              <li>Atuação comercial focada em superação de metas, prospecção ativa e atendimento ao cliente com excelência.</li>
              <li><strong>Reconhecido como um dos melhores vendedores da empresa</strong>, com destaque registrado e publicado oficialmente no LinkedIn do OK Bank.</li>
            </ul>
          </div>

          <!-- PME MÁQUINAS -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Assistente Administrativo</div>
              <div class="job-date">Ago. 2023 a Dez. 2024</div>
            </div>
            <div class="job-company">PME Máquinas e Equipamentos <span>· 1 ano e 5 meses</span></div>
            <ul class="job-bullets">
              <li>Elaboração de orçamentos técnicos, controle rigoroso de horas de maquinário e organização de relatórios de viagem e folha de ponto.</li>
              <li>Reestruturação de processos administrativos internos, garantindo cumprimento de prazos e organização de dados logísticos.</li>
            </ul>
          </div>

        </div>

      </div>

    </div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page">
    <div class="top-bar"></div>

    <!-- HEADER COMPACT PAGE 2 -->
    <div class="header-p2">
      <div>
        <div class="header-p2-name">Cauã Gustavo da Silva Bernardino</div>
        <div class="header-p2-role">Engenharia da Computação (6º Período · Multivix Vitória) · Full Stack & IA</div>
      </div>
      <div class="header-p2-contact">
        +55 (27) 99781-7164 · cauag1834@gmail.com<br>
        Vitória/ES | Bairro Nova Palestina · github.com/cauag1834-maker
      </div>
    </div>

    <!-- LAYOUT PAGE 2 -->
    <div class="layout-p2">

      <!-- LEFT SIDEBAR -->
      <div class="sidebar">

        <!-- FORMAÇÃO ACADÊMICA -->
        <div>
          <div class="section-title">Formação Acadêmica</div>
          
          <div style="margin-bottom: 6px;">
            <div style="font-weight: 800; font-size: 8.3pt; color: #0f172a;">Engenharia da Computação (Bacharelado)</div>
            <div style="font-size: 7.7pt; color: #0284c7; font-weight: 700;">Faculdade Multivix Vitória · 6º Período</div>
            <div style="font-size: 7.3pt; color: #64748b;">Vitória/ES · Graduação em andamento</div>
            <p style="font-size: 7.3pt; color: #475569; margin-top: 1.5px;">
              Foco em Arquitetura de Computadores, Sistemas Distribuídos, Algoritmos, Redes e IA.
            </p>
          </div>

          <div style="margin-bottom: 6px;">
            <div style="font-weight: 800; font-size: 8.3pt; color: #0f172a;">Iniciação Científica: FAPES & EMESCAM</div>
            <div style="font-size: 7.7pt; color: #0284c7; font-weight: 600;">Governo do Estado do ES & EMESCAM</div>
            <p style="font-size: 7.3pt; color: #475569; margin-top: 1.5px;">
              Pesquisa acadêmica sobre combate ao preconceito nas escolas públicas e elaboração de cartilha educativa.
            </p>
          </div>

          <div>
            <div style="font-weight: 800; font-size: 8.3pt; color: #0f172a;">Ensino Médio Completo</div>
            <div style="font-size: 7.5pt; color: #475569;">EEEFM Elza Lemos de Andreatta</div>
          </div>
        </div>

        <!-- CURSOS & CERTIFICAÇÕES -->
        <div>
          <div class="section-title">Cursos & Certificações</div>

          <div class="cert-list">
            <div class="cert-item">
              <div class="cert-name">Google Student Ambassador 2026</div>
              <div class="cert-org">Google for Education / Amplifica</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Automação com Controladores (PLCs)</div>
              <div class="cert-org">Projeto Vale nas Escolas · Multinacional Vale S.A.</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Informática Avançada & Hardware</div>
              <div class="cert-org">Power BI, Excel, Montagem e Manutenção</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Assistente Administrativo (Teórico e Prático)</div>
              <div class="cert-org">Gestão de Processos e Rotinas Empresariais</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Imersão IA na Prática (IAP)</div>
              <div class="cert-org">Aplicações com LLMs e Agentes Autônomos</div>
            </div>
          </div>
        </div>

        <!-- DIFERENCIAL DE GESTÃO -->
        <div>
          <div class="section-title">Organização Empresarial & Gestão</div>
          <div style="font-size: 7.6pt; color: #334155; line-height: 1.38;">
            <div>• <strong>Diagnóstico de Gargalos:</strong> Identificação rápida de falhas operacionais e comerciais.</div>
            <div>• <strong>Estruturação de Processos:</strong> Padronização de rotinas para ganho de escala.</div>
            <div>• <strong>Pego, Otimizo e Transformo:</strong> Execução técnica alinhada a metas de faturamento.</div>
          </div>
        </div>

        <!-- IDIOMAS -->
        <div>
          <div class="section-title">Idiomas</div>
          <div style="font-size: 7.7pt; color: #334155; line-height: 1.4;">
            <div><strong>Português:</strong> Nativo</div>
            <div><strong>Inglês:</strong> Técnico (Leitura de documentações, APIs e arquiteturas)</div>
          </div>
        </div>

      </div>

      <!-- RIGHT MAIN (PROJETOS DETALHADOS) -->
      <div class="main">

        <div>
          <div class="section-title">Projetos de Engenharia & Software em Destaque</div>

          <div class="proj-list">

            <!-- 1. UVV EAD -->
            <div class="proj-card">
              <div class="proj-title">
                <span>1. Sistema EAD: Universidade Vila Velha (UVV)</span>
                <span class="proj-status">EM PRODUÇÃO</span>
              </div>
              <div class="proj-desc">
                Nova plataforma de Ensino a Distância desenvolvida sob medida e implantada para os alunos da UVV, conduzida em alinhamento estratégico com a diretoria acadêmica para modernização de acesso e retenção estudantil.
              </div>
              <div class="proj-techs">Full Stack · Next.js · PostgreSQL · Supabase · UX Mobile-first</div>
            </div>

            <!-- 2. PUBLIVIEW360 -->
            <div class="proj-card">
              <div class="proj-title">
                <span>2. PubliView360 & PubliOnline (Comunicação 360)</span>
                <span class="proj-status">PRODUÇÃO & MÍDIA</span>
              </div>
              <div class="proj-desc">
                Ecossistema de inteligência política e monitoramento com IA de análise de sentimento e CRM georreferenciado. Validado nas Eleições 2026 e em negociação executiva com a diretoria da <strong>TV Gazeta</strong> (Afiliada Globo) para monitoramento de redes.
              </div>
              <div class="proj-techs">Next.js 14 · Supabase RLS · Vercel Edge · IA Sentimento · Docker</div>
            </div>

            <!-- 3. WORKFLOW APP & AUTOMAÇÕES WHATSAPP -->
            <div class="proj-card">
              <div class="proj-title">
                <span>3. Gateway de Mensageria & Integrações de Vendas</span>
                <span class="proj-status">PRODUÇÃO ATIVA</span>
              </div>
              <div class="proj-desc">
                Infraestrutura com VPS Hostinger dedicada rodando cluster Docker com API de WhatsApp, disparo em massa inteligente, recuperação de checkout Hubla e ferramenta de validação/higienização de listas ativas.
              </div>
              <div class="proj-techs">Hostinger VPS · Linux Ubuntu · Docker · Node.js · Hubla · WAHA API</div>
            </div>

            <!-- 4. MEDSYSTEM -->
            <div class="proj-card">
              <div class="proj-title">
                <span>4. MedSystem: Prontuário IA & Prescrição Memed</span>
                <span class="proj-status">HOMOLOGAÇÃO</span>
              </div>
              <div class="proj-desc">
                Prontuário com IA por voz via Google Gemini (transcrição clínica em 30s no padrão SOAP/CID-10), Prescrição Digital oficial Memed (ICP-Brasil) e split automático financeiro para mais de 400 médicos.
              </div>
              <div class="proj-techs">Google Gemini · Memed SDK · Split Pix/Cartão · Supabase</div>
            </div>

            <!-- 5. WORKUT -->
            <div class="proj-card">
              <div class="proj-title">
                <span>5. Workut: SaaS de Gestão para Estética & Beleza</span>
                <span class="proj-status">PRODUÇÃO & EXPANSÃO</span>
              </div>
              <div class="proj-desc">
                SaaS completo de gestão com agendamento online sem conflito, PDV integrado, clube de assinaturas e operação real (Dom Cabral Barbearia) e expansão internacional com Aura Cosméticos (Venezuela).
              </div>
              <div class="proj-techs">Next.js 14 · Supabase · Pagamentos Integrados · Mobile Web</div>
            </div>

            <!-- 6. VETIO & PROJETOS VETERINÁRIOS -->
            <div class="proj-card">
              <div class="proj-title">
                <span>6. Vetio 2.0 & Aplicações Veterinárias (Pet / PM)</span>
                <span class="proj-status">PRODUÇÃO ATIVA</span>
              </div>
              <div class="proj-desc">
                Sistemas para saúde animal com controle vacinal FEFO por lote, relatórios médicos e Smart Tags QR/NFC com resgate SOS geolocalizado em clínicas reais e projeto acadêmico para o setor da PM.
              </div>
              <div class="proj-techs">Smart Tags NFC/QR · FlutterFlow · Next.js · PostgreSQL</div>
            </div>

            <!-- 7. LOVEMEMORY & LANDING PAGES -->
            <div class="proj-card">
              <div class="proj-title">
                <span>7. LoveMemory & Criação de Landing Pages de Alta Conversão</span>
                <span class="proj-status">ALTA CONVERSÃO</span>
              </div>
              <div class="proj-desc">
                Plataforma web de memórias afetivas interativas (lovememory.space) e desenvolvimento de landing pages ultra-rápidas (PageSpeed 95+, &lt;1.5s), com transbordo imediato para WhatsApp e campanhas de tráfego pago.
              </div>
              <div class="proj-techs">PageSpeed 95+ · Webhooks Meta Ads · Funil de Vendas · Stripe</div>
            </div>

          </div>
        </div>

      </div>

    </div>
  </div>

</body>
</html>
"""

with open("curriculo-caua-gustavo.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("curriculo-caua-gustavo.html created successfully!")

# Render to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf_out = Path("curriculo-caua-gustavo.pdf").resolve()
html_uri = Path("curriculo-caua-gustavo.html").resolve().as_uri()

temp_profile = Path(tempfile.gettempdir()) / f"chrome_cv_export_{os.getpid()}"
temp_profile.mkdir(parents=True, exist_ok=True)

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--user-data-dir={temp_profile}",
    f"--print-to-pdf={pdf_out}",
    html_uri
]

print("Running Chrome to generate PDF...")
res = subprocess.run(cmd, capture_output=True, text=True)
if pdf_out.exists():
    size = pdf_out.stat().st_size
    reader = pypdf.PdfReader(str(pdf_out))
    pages = len(reader.pages)
    print(f"SUCCESS: PDF generated! Size: {size} bytes | Pages: {pages}")
else:
    print("FAILED:", res.stderr)
