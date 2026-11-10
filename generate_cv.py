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
<title>Currículo - Cauã Gustavo da Silva Bernardino</title>
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
    font-size: 9pt;
    line-height: 1.42;
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
    padding: 12mm 14mm 12mm 14mm;
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
    height: 6px;
    background: linear-gradient(90deg, #0284c7, #38bdf8, #6366f1);
  }}

  /* HEADER PAGE 1 */
  .header-p1 {{
    text-align: center;
    padding-bottom: 12px;
    margin-bottom: 12px;
    border-bottom: 1.5px solid #e2e8f0;
  }}
  .avatar {{
    width: 82px;
    height: 82px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #0284c7;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.22);
    display: inline-block;
    margin-bottom: 6px;
  }}
  .name {{
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 2.2px;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 3px;
  }}
  .role {{
    font-size: 9.8pt;
    font-weight: 700;
    color: #0284c7;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 5px;
  }}
  .quote {{
    font-size: 8.2pt;
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
    padding-bottom: 10px;
    margin-bottom: 14px;
    border-bottom: 1.5px solid #e2e8f0;
  }}
  .header-p2-name {{
    font-size: 11pt;
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
    font-size: 7.8pt;
    color: #64748b;
    text-align: right;
  }}

  /* TWO-COLUMN LAYOUT */
  .layout {{
    display: flex;
    gap: 18px;
    height: calc(100% - 150px);
  }}
  .layout-p2 {{
    display: flex;
    gap: 18px;
    height: calc(100% - 40px);
  }}

  /* LEFT SIDEBAR (31%) */
  .sidebar {{
    width: 31%;
    border-right: 1.5px solid #e2e8f0;
    padding-right: 14px;
    display: flex;
    flex-direction: column;
    gap: 11px;
  }}

  /* RIGHT MAIN (69%) */
  .main {{
    width: 69%;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  /* SECTION TITLE */
  .section-title {{
    font-size: 9.2pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding-bottom: 3px;
    border-bottom: 2px solid #0284c7;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .section-title-icon {{
    color: #0284c7;
    font-size: 9pt;
  }}

  /* CONTACT LIST */
  .contact-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 8pt;
  }}
  .contact-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    color: #334155;
    word-break: break-all;
  }}
  .contact-item a {{
    color: #0284c7;
    text-decoration: none;
    font-weight: 600;
  }}
  .c-icon {{
    font-size: 8.5pt;
    color: #0284c7;
    flex-shrink: 0;
  }}

  /* SUMMARY */
  .summary-text {{
    font-size: 8.1pt;
    color: #334155;
    line-height: 1.4;
    text-align: justify;
  }}

  /* SKILL GROUPS */
  .skill-group {{
    margin-bottom: 6px;
  }}
  .skill-group-title {{
    font-size: 8pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 3px;
  }}
  .skill-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 3.5px;
  }}
  .skill-tag {{
    font-size: 7.2pt;
    padding: 1.5px 6px;
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
    margin-bottom: 9px;
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
    margin-bottom: 1.5px;
  }}
  .job-title {{
    font-size: 9.3pt;
    font-weight: 800;
    color: #0f172a;
  }}
  .job-date {{
    font-size: 7.5pt;
    font-weight: 700;
    color: #0284c7;
    background: #e0f2fe;
    padding: 1px 6px;
    border-radius: 999px;
    white-space: nowrap;
  }}
  .job-company {{
    font-size: 8.3pt;
    font-weight: 600;
    color: #475569;
    margin-bottom: 3px;
  }}
  .job-company span {{
    color: #64748b;
    font-weight: 400;
  }}
  .job-bullets {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 3px;
    font-size: 8.1pt;
    color: #334155;
  }}
  .job-bullets li {{
    position: relative;
    padding-left: 10px;
    line-height: 1.38;
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
    gap: 7px;
  }}
  .proj-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6.5px 9px;
  }}
  .proj-title {{
    font-size: 8.6pt;
    font-weight: 800;
    color: #0f172a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
  }}
  .proj-status {{
    font-size: 6.5pt;
    font-weight: 700;
    color: #047857;
    background: #d1fae5;
    padding: 1px 5px;
    border-radius: 3px;
    text-transform: uppercase;
  }}
  .proj-desc {{
    font-size: 7.8pt;
    color: #475569;
    line-height: 1.35;
    margin-bottom: 3px;
  }}
  .proj-techs {{
    font-size: 7.2pt;
    color: #0284c7;
    font-weight: 600;
  }}

  /* CERTIFICATIONS LIST */
  .cert-list {{
    display: flex;
    flex-direction: column;
    gap: 5.5px;
  }}
  .cert-item {{
    font-size: 7.9pt;
  }}
  .cert-name {{
    font-weight: 700;
    color: #0f172a;
    line-height: 1.25;
  }}
  .cert-org {{
    color: #0284c7;
    font-weight: 600;
    font-size: 7.4pt;
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
      <div class="role">Engenheiro de Software | Full Stack & Inteligência Artificial</div>
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
          <div class="section-title">
            <span class="section-title-icon">📍</span> Contato
          </div>
          <ul class="contact-list">
            <li class="contact-item">
              <span class="c-icon">📞</span>
              <span><strong>+55 (27) 99781-7164</strong></span>
            </li>
            <li class="contact-item">
              <span class="c-icon">✉️</span>
              <span><strong>cauag1834@gmail.com</strong></span>
            </li>
            <li class="contact-item">
              <span class="c-icon">📌</span>
              <span>Espírito Santo, Brasil</span>
            </li>
            <li class="contact-item">
              <span class="c-icon">🔗</span>
              <span><a href="https://www.linkedin.com/in/cau%C3%A3-gustavo-da-silva-bernardino-455005304/" target="_blank">linkedin.com/in/caua-gustavo</a></span>
            </li>
            <li class="contact-item">
              <span class="c-icon">🐙</span>
              <span><a href="https://github.com/cauag1834-maker" target="_blank">github.com/cauag1834-maker</a></span>
            </li>
            <li class="contact-item">
              <span class="c-icon">🌐</span>
              <span><a href="https://workflow.app.br" target="_blank">Portfólio & Plataformas no Ar</a></span>
            </li>
          </ul>
        </div>

        <!-- RESUMO PROFISSIONAL -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">💼</span> Perfil Profissional
          </div>
          <p class="summary-text">
            Desenvolvedor Full Stack de 21 anos com perfil orientado a <strong>Engenharia da Computação</strong>, <strong>Organização Empresarial</strong> e <strong>Otimização de Processos Comerciais</strong>.
          </p>
          <p class="summary-text" style="margin-top: 5px;">
            Especialista na concepção e sustentação de microsserviços, ecossistemas SaaS multi-tenant, gateways de mensageria em Cloud VPS e soluções avançadas com <strong>Inteligência Artificial (Google Gemini)</strong>. Diferencial reconhecido em liderar diagnósticos operacionais e transformar fluxos manuais em faturamento e escala real.
          </p>
        </div>

        <!-- COMPETÊNCIAS TÉCNICAS -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">🛠️</span> Habilidades Técnicas
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Linguagens & Frontend</div>
            <div class="skill-tags">
              <span class="skill-tag accent">TypeScript</span>
              <span class="skill-tag accent">JavaScript ES6+</span>
              <span class="skill-tag accent">Next.js 14</span>
              <span class="skill-tag">React 18</span>
              <span class="skill-tag">Tailwind CSS</span>
              <span class="skill-tag">C++</span>
              <span class="skill-tag">HTML5 / CSS3</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Inteligência Artificial & LLMs</div>
            <div class="skill-tags">
              <span class="skill-tag accent">Google Gemini API</span>
              <span class="skill-tag accent">Prompt Engineering</span>
              <span class="skill-tag">NLP / Sentimento</span>
              <span class="skill-tag">Agentes Autônomos</span>
              <span class="skill-tag">n8n Workflows</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Cloud, DevOps & Infra</div>
            <div class="skill-tags">
              <span class="skill-tag accent">Hostinger VPS</span>
              <span class="skill-tag accent">Linux (Ubuntu)</span>
              <span class="skill-tag accent">Docker Containers</span>
              <span class="skill-tag">WhatsApp API (WAHA)</span>
              <span class="skill-tag">Vercel Edge</span>
              <span class="skill-tag">Cloudflare SSL/DNS</span>
              <span class="skill-tag">Wireshark</span>
            </div>
          </div>

          <div class="skill-group">
            <div class="skill-group-title">Bancos de Dados & Back</div>
            <div class="skill-tags">
              <span class="skill-tag accent">PostgreSQL</span>
              <span class="skill-tag accent">Supabase RLS</span>
              <span class="skill-tag">Deno Edge</span>
              <span class="skill-tag">Node.js</span>
              <span class="skill-tag">Webhooks Idempotentes</span>
              <span class="skill-tag">RESTful APIs</span>
            </div>
          </div>
        </div>

      </div>

      <!-- RIGHT MAIN (EXPERIÊNCIA) -->
      <div class="main">

        <div>
          <div class="section-title">
            <span class="section-title-icon">💼</span> Trajetória Profissional
          </div>

          <!-- GOOGLE AMBASSADOR -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Google Student Ambassador</div>
              <div class="job-date">Ago. 2026 – Presente</div>
            </div>
            <div class="job-company">Google for Education & Amplifica <span>· Remoto / Nacional</span></div>
            <ul class="job-bullets">
              <li>Selecionado nacionalmente para representar e disseminar soluções de <strong>Inteligência Artificial Generativa (Google Gemini)</strong> e ferramentas educacionais de ponta.</li>
              <li>Condução de workshops e dinâmicas sobre aplicação de IA para produtividade, engenharia e resolução de desafios acadêmicos e corporativos.</li>
            </ul>
          </div>

          <!-- WORKFLOW BUSINESS -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Suporte Técnico & Analista de Integração</div>
              <div class="job-date">Jun. 2025 – Presente</div>
            </div>
            <div class="job-company">Workflow Business <span>· Tempo Integral · Vitória/ES (Remoto)</span></div>
            <ul class="job-bullets">
              <li>Desenvolvimento e sustentação de <strong>integrações de APIs de alto volume em TypeScript e JavaScript</strong>, conectando CRM a formulários nativos do Meta Lead Ads com transbordo no WhatsApp em &lt; 3 segundos.</li>
              <li>Engenharia de integração com gateways e plataformas de infoproduto (<strong>Hubla e Hotmart</strong>), automatizando recuperação de carrinhos abandonados e entrega imediata de credenciais de acesso via bot.</li>
              <li>Administração e hardening de <strong>infraestrutura própria de mensageria em VPS Linux (Hostinger)</strong>, operando cluster Docker com API não oficial de WhatsApp com alta tolerância a falhas.</li>
              <li>Suporte técnico especializado de 3º nível para contas corporativas, resolvendo gargalos de latência e otimizando pipelines de webhooks.</li>
            </ul>
          </div>

          <!-- OK BANK -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Correspondente Bancário & Operações Comerciais</div>
              <div class="job-date">Set. 2024 – Fev. 2025</div>
            </div>
            <div class="job-company">OK BANK <span>· Estágio · 6 meses</span></div>
            <ul class="job-bullets">
              <li>Atuação direta na esteira de concessão e validação de crédito, análise documental minuciosa e relacionamento de negócios com clientes.</li>
              <li>Mapeamento e otimização dos fluxos de onboarding de clientes, reduzindo o tempo médio de resposta e triagem comercial.</li>
            </ul>
          </div>

          <!-- PME MÁQUINAS -->
          <div class="timeline-item">
            <div class="job-header">
              <div class="job-title">Assistente Administrativo & Processos</div>
              <div class="job-date">Ago. 2023 – Dez. 2024</div>
            </div>
            <div class="job-company">PME Máquinas e Equipamentos <span>· Estágio · 1 ano 5 meses</span></div>
            <ul class="job-bullets">
              <li>Reestruturação de processos operacionais e controles administrativos internos, organizando inventário e dados logísticos.</li>
              <li>Padronização de rotinas de atendimento que integraram o time comercial e administrativo com maior agilidade.</li>
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
        <div class="header-p2-role">Engenharia de Software · IA & Organização Empresarial</div>
      </div>
      <div class="header-p2-contact">
        +55 (27) 99781-7164 · cauag1834@gmail.com<br>
        Espírito Santo, Brasil · github.com/cauag1834-maker
      </div>
    </div>

    <!-- LAYOUT PAGE 2 -->
    <div class="layout-p2">

      <!-- LEFT SIDEBAR -->
      <div class="sidebar">

        <!-- FORMAÇÃO ACADÊMICA -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">🎓</span> Formação
          </div>
          
          <div style="margin-bottom: 7px;">
            <div style="font-weight: 800; font-size: 8.5pt; color: #0f172a;">Engenharia da Computação / Tecnologia</div>
            <div style="font-size: 7.8pt; color: #0284c7; font-weight: 600;">Graduação em Andamento</div>
            <div style="font-size: 7.5pt; color: #64748b;">Espírito Santo, Brasil</div>
            <p style="font-size: 7.5pt; color: #475569; margin-top: 2px;">
              Foco em Arquitetura de Software, Sistemas Distribuídos, Algoritmos e Inteligência Artificial.
            </p>
          </div>

          <div>
            <div style="font-weight: 800; font-size: 8.5pt; color: #0f172a;">Iniciação Científica — FAPES</div>
            <div style="font-size: 7.8pt; color: #0284c7; font-weight: 600;">EMESCAM & Governo do ES</div>
            <p style="font-size: 7.5pt; color: #475569; margin-top: 2px;">
              Pesquisa financiada pela FAPES sobre análise de dados sociais e combate a preconceitos no ambiente escolar público capixaba.
            </p>
          </div>
        </div>

        <!-- CERTIFICAÇÕES & RECONHECIMENTOS -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">🏆</span> Certificações
          </div>

          <div class="cert-list">
            <div class="cert-item">
              <div class="cert-name">Google Student Ambassador 2026</div>
              <div class="cert-org">Google for Education / Amplifica</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Formação Técnica em PLC</div>
              <div class="cert-org">Vale S.A. (Controladores Industriais)</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Cerimônia de Certificados Vale</div>
              <div class="cert-org">Reconhecimento Oficial Multinacional Vale</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Imersão Técnica IA na Prática (IAP)</div>
              <div class="cert-org">Treinamento em LLMs & Agentes IA</div>
            </div>

            <div class="cert-item">
              <div class="cert-name">Defesa WhatsApp Multi-tenant</div>
              <div class="cert-org">Apresentação Acadêmica de Sistemas</div>
            </div>
          </div>
        </div>

        <!-- DIFERENCIAL DE GESTÃO -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">⚙️</span> Gestão & Metodologia
          </div>
          <div style="font-size: 7.8pt; color: #334155; line-height: 1.4;">
            <div>• <strong>Organização Empresarial:</strong> Mapeamento e eliminação de gargalos em equipes.</div>
            <div>• <strong>Processos Comerciais:</strong> Estruturação de funis de vendas e atendimento ágil.</div>
            <div>• <strong>Pego, Otimizo e Transformo:</strong> Execução rápida com equipe técnica dedicada.</div>
          </div>
        </div>

        <!-- IDIOMAS -->
        <div>
          <div class="section-title">
            <span class="section-title-icon">🌐</span> Idiomas
          </div>
          <div style="font-size: 8pt; color: #334155; line-height: 1.45;">
            <div><strong>Português:</strong> Nativo</div>
            <div><strong>Inglês:</strong> Técnico Profissional (Leitura fluente de documentações, APIs e arquiteturas)</div>
          </div>
        </div>

      </div>

      <!-- RIGHT MAIN (PROJETOS DETALHADOS) -->
      <div class="main">

        <div>
          <div class="section-title">
            <span class="section-title-icon">🚀</span> Projetos de Engenharia & IA em Produção
          </div>

          <div class="proj-list">

            <!-- 1. UVV EAD -->
            <div class="proj-card">
              <div class="proj-title">
                <span>1. Sistema EAD — Universidade Vila Velha (UVV)</span>
                <span class="proj-status">EM PRODUÇÃO ATIVA 🚀</span>
              </div>
              <div class="proj-desc">
                Nova plataforma de Ensino a Distância desenvolvida sob medida e implantada para os alunos da UVV, alinhada diretamente com a diretoria acadêmica da instituição para otimizar os fluxos de aprendizagem e retenção estudantil.
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
                Ecossistema de inteligência política e social com IA de análise de sentimento, CRM georreferenciado e santinhos digitais. Validado nas Eleições 2026 (Prefeito Arnaldinho Borgo) e em negociação executiva com a diretoria da <strong>TV Gazeta</strong> (Afiliada Globo) para monitoramento de redes.
              </div>
              <div class="proj-techs">Next.js 14 · Supabase RLS · Vercel Edge · IA Sentimento · Docker</div>
            </div>

            <!-- 3. MEDSYSTEM -->
            <div class="proj-card">
              <div class="proj-title">
                <span>3. MedSystem — Prontuário IA & Prescrição Memed</span>
                <span class="proj-status">HOMOLOGAÇÃO CLÍNICA</span>
              </div>
              <div class="proj-desc">
                Prontuário com IA por voz via Google Gemini (transcrição clínica em 30s para o padrão SOAP com CID-10), Prescrição Digital oficial Memed Sinapse (ICP-Brasil) e split automático de repasse para carteira de 400+ médicos.
              </div>
              <div class="proj-techs">Google Gemini 1.5 · Memed SDK · Split Pix/Cartão · Painel TV</div>
            </div>

            <!-- 4. WORKUT -->
            <div class="proj-card">
              <div class="proj-title">
                <span>4. Workut — SaaS Gestão de Beleza & Estética</span>
                <span class="proj-status">PRODUÇÃO & EXPANSÃO VE</span>
              </div>
              <div class="proj-desc">
                Plataforma com agenda multi-profissional sem conflitos, PDV, frente de caixa cego e Clube VIP de assinaturas. Em produção real (Dom Cabral Barbearia) e em expansão internacional para a Venezuela com a Aura Cosméticos.
              </div>
              <div class="proj-techs">Next.js 14 · Supabase · InfinitePay/Stripe · Apps Mobile</div>
            </div>

            <!-- 5. VETIO 2.0 -->
            <div class="proj-card">
              <div class="proj-title">
                <span>5. Vetio 2.0 — Saúde Pet & Smart Tags QR/NFC</span>
                <span class="proj-status">PRODUÇÃO ATIVA</span>
              </div>
              <div class="proj-desc">
                Prontuário veterinário com controle vacinal FEFO por lote e inovadoras Smart Tags QR/NFC com resgate SOS geolocalizado para cães e gatos em operação clínica ativa (FF Pet Center).
              </div>
              <div class="proj-techs">Smart Tags NFC/QR · GPS Consentido · PostgreSQL · Next.js</div>
            </div>

            <!-- 6. CLOUD VPS HOSTINGER -->
            <div class="proj-card">
              <div class="proj-title">
                <span>6. Infraestrutura Cloud VPS Hostinger & Gateway WhatsApp</span>
                <span class="proj-status">DEVOPS DEDICADO</span>
              </div>
              <div class="proj-desc">
                Servidor Linux dedicado gerenciado pessoalmente, operando cluster Docker com API não oficial de WhatsApp. Atua como o backend central de mensageria em tempo real e webhooks para todo o ecossistema.
              </div>
              <div class="proj-techs">Hostinger VPS · Linux Ubuntu · Docker · WAHA HTTP API · SSL/DNS</div>
            </div>

            <!-- 7. LANDING PAGES -->
            <div class="proj-card">
              <div class="proj-title">
                <span>7. Landing Pages de Alta Conversão & Design Web</span>
                <span class="proj-status">ALTA PERFORMANCE</span>
              </div>
              <div class="proj-desc">
                Páginas ultra-otimizadas para tráfego pago (Meta Ads, Google Ads), nota 95+ no PageSpeed (&lt; 1.5s), design Dark Glassmorphism e integração de leads direto para o WhatsApp em menos de 3s.
              </div>
              <div class="proj-techs">Web Vitals 95+ · Webhooks Meta Ads · Funil AIDA · Stripe/Hubla</div>
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

temp_profile = Path(tempfile.gettempdir()) / "chrome_cv_export_v2"
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
