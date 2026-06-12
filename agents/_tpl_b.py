# _tpl_b.py  —  Jinja2-шаблоны B-серии для SUMMARA
# MINDMAP, BRAINSTORM, STEPS
# Фильтр `md` регистрируется снаружи; для самотеста — простой lambda.

MINDMAP = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;700;800&family=Fredoka+One&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Baloo 2', 'Comic Sans MS', 'Trebuchet MS', cursive, sans-serif;
  background-color: #f5f5f5;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 27px, rgba(160,180,255,0.35) 28px),
    repeating-linear-gradient(90deg, transparent, transparent 27px, rgba(160,180,255,0.35) 28px);
  background-size: 28px 28px;
  min-height: 100vh;
  padding: 32px 16px 48px;
  color: #222;
}

.page {
  max-width: 820px;
  margin: 0 auto;
  background: rgba(255,255,255,0.82);
  border-radius: 18px;
  padding: 36px 40px 40px;
  box-shadow: 0 4px 32px rgba(80,80,160,0.10);
}

/* HERO TITLE */
.hero-title {
  font-family: 'Fredoka One', 'Baloo 2', cursive, sans-serif;
  font-size: 2.6rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #222;
  text-align: left;
  line-height: 1.15;
  margin-bottom: 28px;
}

/* FIELD CARDS */
.field-card {
  background: #fff;
  border-left: 6px solid #a855f7;
  border-radius: 10px;
  padding: 12px 18px;
  margin-bottom: 14px;
  box-shadow: 0 2px 8px rgba(168,85,247,0.10);
}
.field-label {
  font-weight: 800;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #a855f7;
  margin-bottom: 2px;
}
.field-value {
  font-size: 1rem;
  color: #333;
  line-height: 1.5;
}

/* TIMELINE */
.timeline {
  position: relative;
  margin: 18px 0 18px 20px;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #a855f7 0%, #ec4899 25%, #ef4444 50%, #f97316 75%, #22c55e 100%);
  border-radius: 4px;
  z-index: 0;
}
.timeline-group {
  margin-bottom: 20px;
}
.timeline-group-label {
  font-family: 'Fredoka One', 'Baloo 2', cursive, sans-serif;
  font-size: 1.5rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-left: 60px;
  margin-bottom: 6px;
}
.timeline-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 22px;
  position: relative;
}
.timeline-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Fredoka One', 'Baloo 2', cursive;
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
}
.timeline-body {
  padding-top: 6px;
  font-size: 0.97rem;
  color: #333;
  line-height: 1.55;
}

/* circle colours cycling */
.tl-c0 { background: #a855f7; }
.tl-c1 { background: #ec4899; }
.tl-c2 { background: #ef4444; }
.tl-c3 { background: #f97316; }
.tl-c4 { background: #22c55e; }
.tl-c5 { background: #3b82f6; }
.tl-c6 { background: #eab308; }
.tl-c7 { background: #06b6d4; }

/* group heading colours */
.gc0 { color: #a855f7; }
.gc1 { color: #ec4899; }
.gc2 { color: #ef4444; }
.gc3 { color: #f97316; }
.gc4 { color: #22c55e; }
.gc5 { color: #3b82f6; }
.gc6 { color: #eab308; }
.gc7 { color: #06b6d4; }

/* HEADING block */
.section-heading {
  font-family: 'Fredoka One', 'Baloo 2', cursive, sans-serif;
  font-size: 1.35rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #a855f7;
  margin: 22px 0 8px;
  letter-spacing: 0.5px;
}

/* PARA block */
.para-block {
  font-size: 0.97rem;
  color: #444;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* bullet list */
.bullet-group {
  margin: 10px 0 10px 60px;
}
.bullet-group-label {
  font-family: 'Fredoka One', 'Baloo 2', cursive, sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #ec4899;
  margin-bottom: 6px;
}
.bullet-item {
  font-size: 0.96rem;
  color: #333;
  line-height: 1.5;
  padding-left: 18px;
  position: relative;
  margin-bottom: 5px;
}
.bullet-item::before {
  content: '✦';
  position: absolute;
  left: 0;
  color: #ec4899;
  font-size: 0.75rem;
  top: 2px;
}

/* DIVIDER */
.divider {
  border: none;
  height: 3px;
  background: linear-gradient(90deg, #a855f7, #ec4899, #f97316, #22c55e);
  border-radius: 3px;
  margin: 20px 0;
}

/* FOOTER */
.footer {
  margin-top: 36px;
  padding-top: 18px;
  border-top: 2px dashed #d0d0e0;
  text-align: center;
  font-size: 0.78rem;
  color: #888;
  font-family: 'Baloo 2', sans-serif;
}
.footer img {
  height: 28px;
  vertical-align: middle;
  margin-right: 6px;
  border-radius: 6px;
}

@media (max-width: 600px) {
  .page { padding: 20px 14px 28px; }
  .hero-title { font-size: 1.8rem; }
  .timeline { margin-left: 0; }
  .bullet-group { margin-left: 10px; }
}
</style>
</head>
<body>
<div class="page">

  <div class="hero-title">{{ title }}</div>

  {% set ns = namespace(tl_idx=0, g_idx=0) %}
  {% for b in blocks %}

    {% if b.type == 'field' %}
    <div class="field-card">
      <div class="field-label">{{ b.label | md }}</div>
      <div class="field-value">{{ b.value | md }}</div>
    </div>

    {% elif b.type == 'group' and b.ordered %}
    <div class="timeline timeline-group">
      {% if b.label %}
      <div class="timeline-group-label gc{{ ns.g_idx % 8 }}">{{ b.label | md }}</div>
      {% set ns.g_idx = ns.g_idx + 1 %}
      {% endif %}
      {% for item in b['items'] %}
      <div class="timeline-item">
        <div class="timeline-circle tl-c{{ ns.tl_idx % 8 }}">{{ loop.index }}</div>
        <div class="timeline-body">{{ item | md }}</div>
      </div>
      {% set ns.tl_idx = ns.tl_idx + 1 %}
      {% endfor %}
    </div>

    {% elif b.type == 'group' and not b.ordered %}
    <div class="bullet-group">
      {% if b.label %}
      <div class="bullet-group-label">{{ b.label | md }}</div>
      {% endif %}
      {% for item in b['items'] %}
      <div class="bullet-item">{{ item | md }}</div>
      {% endfor %}
    </div>

    {% elif b.type == 'heading' %}
    <div class="section-heading">{{ b.text | md }}</div>

    {% elif b.type == 'para' %}
    <div class="para-block">{{ b.text | md }}</div>

    {% elif b.type == 'divider' %}
    <hr class="divider">

    {% endif %}
  {% endfor %}

  <div class="footer">
    {% if logo_b64 %}<img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA logo">{% endif %}
    Создано в&nbsp;<strong>SUMMARA</strong>
  </div>

</div>
</body>
</html>"""


BRAINSTORM = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Baloo+2:wght@400;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Baloo 2', 'Comic Sans MS', cursive, sans-serif;
  background-color: #f0f0f8;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 27px, rgba(120,140,220,0.28) 28px),
    repeating-linear-gradient(90deg, transparent, transparent 27px, rgba(120,140,220,0.28) 28px);
  background-size: 28px 28px;
  min-height: 100vh;
  padding: 32px 16px 48px;
  color: #111;
}

.page {
  max-width: 820px;
  margin: 0 auto;
  background: rgba(255,255,255,0.78);
  border-radius: 20px;
  padding: 36px 40px 44px;
  box-shadow: 0 4px 36px rgba(60,60,140,0.12);
}

/* HERO */
.hero-title {
  font-family: 'Caveat', 'Comic Sans MS', cursive;
  font-size: 2.8rem;
  font-weight: 700;
  color: #111;
  line-height: 1.1;
  margin-bottom: 8px;
}
.hero-sub {
  font-family: 'Caveat', 'Comic Sans MS', cursive;
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 28px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

/* FIELD CARDS */
.field-card {
  background: #fff;
  border: 3px solid #8b5cf6;
  border-radius: 12px;
  padding: 12px 18px;
  margin-bottom: 14px;
  box-shadow: 3px 3px 0 #8b5cf6;
}
.field-label {
  font-family: 'Caveat', cursive;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #8b5cf6;
  margin-bottom: 2px;
}
.field-value {
  font-size: 1rem;
  color: #222;
  line-height: 1.5;
}

/* PAINT-STROKE TIMELINE */
.stroke-timeline {
  position: relative;
  margin: 18px 0 18px 16px;
}
.stroke-timeline::before {
  content: '';
  position: absolute;
  left: 22px;
  top: 0;
  bottom: 0;
  width: 5px;
  background: linear-gradient(180deg, #8b5cf6 0%, #ec4899 25%, #ef4444 50%, #f97316 75%, #22c55e 100%);
  border-radius: 5px;
  z-index: 0;
}
.stroke-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 26px;
  position: relative;
}
.stroke-circle {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Caveat', cursive;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  box-shadow: 0 3px 10px rgba(0,0,0,0.22);
}
.stroke-content {
  flex: 1;
}
/* paint stroke effect */
.stroke-blob {
  position: relative;
  padding: 14px 20px 14px 18px;
  border-radius: 8px 30px 12px 26px / 26px 12px 30px 8px;
  color: #fff;
  font-size: 0.96rem;
  line-height: 1.5;
  box-shadow: 2px 4px 0 rgba(0,0,0,0.18);
  min-height: 52px;
}
.stroke-title {
  font-family: 'Caveat', cursive;
  font-size: 1.4rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}
.stroke-text {
  font-family: 'Baloo 2', cursive, sans-serif;
  font-size: 0.92rem;
  opacity: 0.95;
}

/* stroke palette */
.sc0 { background: #8b5cf6; }  /* purple */
.sc1 { background: #ec4899; }  /* pink */
.sc2 { background: #ef4444; }  /* red */
.sc3 { background: #f97316; }  /* orange */
.sc4 { background: #22c55e; }  /* green */
.sc5 { background: #3b82f6; }  /* blue */
.sc6 { background: #eab308; }  /* yellow, text dark */
.sc7 { background: #06b6d4; }  /* cyan */
.sc6 .stroke-title, .sc6 .stroke-text { color: #222; }

/* circle colours matching */
.cc0 { background: #8b5cf6; }
.cc1 { background: #ec4899; }
.cc2 { background: #ef4444; }
.cc3 { background: #f97316; }
.cc4 { background: #22c55e; }
.cc5 { background: #3b82f6; }
.cc6 { background: #eab308; }
.cc7 { background: #06b6d4; }

/* bullet group */
.bullet-group {
  margin: 10px 0 14px 12px;
}
.bullet-group-label {
  font-family: 'Caveat', cursive;
  font-size: 1.35rem;
  font-weight: 700;
  color: #ec4899;
  margin-bottom: 6px;
  text-transform: uppercase;
}
.bullet-item {
  font-size: 0.96rem;
  color: #222;
  line-height: 1.55;
  padding-left: 20px;
  position: relative;
  margin-bottom: 5px;
}
.bullet-item::before {
  content: '★';
  position: absolute;
  left: 0;
  color: #f97316;
  font-size: 0.8rem;
  top: 2px;
}

/* HEADING */
.section-heading {
  font-family: 'Caveat', cursive;
  font-size: 1.6rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #8b5cf6;
  margin: 22px 0 8px;
  letter-spacing: 1px;
}

/* PARA */
.para-block {
  font-size: 0.97rem;
  color: #333;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* DIVIDER */
.divider {
  border: none;
  height: 4px;
  background: repeating-linear-gradient(90deg, #8b5cf6 0px, #8b5cf6 12px, transparent 12px, transparent 18px, #ec4899 18px, #ec4899 30px, transparent 30px, transparent 36px);
  border-radius: 4px;
  margin: 20px 0;
}

/* FOOTER */
.footer {
  margin-top: 36px;
  padding-top: 18px;
  border-top: 3px dashed #d0c0e8;
  text-align: center;
  font-size: 0.8rem;
  color: #888;
  font-family: 'Baloo 2', sans-serif;
}
.footer img {
  height: 28px;
  vertical-align: middle;
  margin-right: 6px;
  border-radius: 6px;
}

@media (max-width: 600px) {
  .page { padding: 18px 12px 28px; }
  .hero-title { font-size: 2rem; }
  .stroke-timeline { margin-left: 0; }
  .bullet-group { margin-left: 0; }
}
</style>
</head>
<body>
<div class="page">

  <div class="hero-title">{{ title }}</div>

  {% set ns = namespace(s_idx=0, g_idx=0) %}
  {% for b in blocks %}

    {% if b.type == 'field' %}
    <div class="field-card">
      <div class="field-label">{{ b.label | md }}</div>
      <div class="field-value">{{ b.value | md }}</div>
    </div>

    {% elif b.type == 'group' and b.ordered %}
    <div class="stroke-timeline">
      {% if b.label %}
      <div class="section-heading">{{ b.label | md }}</div>
      {% endif %}
      {% for item in b['items'] %}
      <div class="stroke-item">
        <div class="stroke-circle cc{{ ns.s_idx % 8 }}">{{ loop.index }}</div>
        <div class="stroke-content">
          <div class="stroke-blob sc{{ ns.s_idx % 8 }}">
            <div class="stroke-text">{{ item | md }}</div>
          </div>
        </div>
      </div>
      {% set ns.s_idx = ns.s_idx + 1 %}
      {% endfor %}
    </div>

    {% elif b.type == 'group' and not b.ordered %}
    <div class="bullet-group">
      {% if b.label %}
      <div class="bullet-group-label">{{ b.label | md }}</div>
      {% endif %}
      {% for item in b['items'] %}
      <div class="bullet-item">{{ item | md }}</div>
      {% endfor %}
    </div>

    {% elif b.type == 'heading' %}
    <div class="section-heading">{{ b.text | md }}</div>

    {% elif b.type == 'para' %}
    <div class="para-block">{{ b.text | md }}</div>

    {% elif b.type == 'divider' %}
    <hr class="divider">

    {% endif %}
  {% endfor %}

  <div class="footer">
    {% if logo_b64 %}<img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA logo">{% endif %}
    Создано в&nbsp;<strong>SUMMARA</strong>
  </div>

</div>
</body>
</html>"""


STEPS = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Montserrat:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
  background: #b8d9ea;
  min-height: 100vh;
  padding: 0 0 56px;
  color: #333;
}

/* cloud blobs scattered in background */
body::before, body::after {
  content: '';
  position: fixed;
  border-radius: 50%;
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
}
body::before {
  width: 380px; height: 220px;
  background: #fff;
  top: 80px; left: -80px;
  border-radius: 50% 60% 70% 40% / 60% 50% 50% 60%;
}
body::after {
  width: 320px; height: 180px;
  background: #fff;
  bottom: 120px; right: -60px;
  border-radius: 60% 40% 50% 70% / 50% 60% 40% 50%;
}

.page {
  position: relative;
  z-index: 1;
  max-width: 820px;
  margin: 0 auto;
  padding: 0 16px;
}

/* HERO */
.hero {
  background: #fff;
  border-radius: 0 0 40px 40px;
  padding: 36px 40px 32px;
  text-align: center;
  margin-bottom: 32px;
  box-shadow: 0 4px 20px rgba(60,120,180,0.12);
}
.hero-title {
  font-family: 'Montserrat', 'Nunito', Arial, sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  color: #2c3e6b;
  line-height: 1.2;
  margin-bottom: 0;
}

/* CLOUD SEPARATOR */
.cloud-sep {
  text-align: center;
  margin: 6px 0 18px;
  font-size: 1.8rem;
  opacity: 0.55;
  letter-spacing: 4px;
}

/* FIELD CARDS — yellow cards */
.field-card {
  background: #f9e468;
  border-radius: 16px;
  padding: 16px 22px;
  margin-bottom: 14px;
  box-shadow: 0 3px 12px rgba(200,160,0,0.15);
  display: flex;
  gap: 12px;
  align-items: baseline;
}
.field-label {
  font-family: 'Montserrat', Arial, sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7a6000;
  flex-shrink: 0;
  min-width: 90px;
}
.field-value {
  font-size: 1rem;
  color: #3a3000;
  line-height: 1.5;
}

/* STEP CARD */
.step-card {
  background: #e8eef8;
  border-radius: 20px;
  padding: 20px 26px 20px 22px;
  margin-bottom: 18px;
  box-shadow: 0 3px 14px rgba(60,100,180,0.11);
  display: flex;
  gap: 20px;
  align-items: flex-start;
  position: relative;
}
.step-badge {
  background: #f4a7b5;
  border-radius: 50%;
  width: 68px;
  height: 68px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(220,80,120,0.22);
  font-family: 'Montserrat', Arial, sans-serif;
}
.step-badge-label {
  font-size: 0.6rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #a0003a;
  line-height: 1;
}
.step-badge-num {
  font-size: 1.7rem;
  font-weight: 900;
  color: #a0003a;
  line-height: 1;
}
.step-body {
  flex: 1;
  padding-top: 6px;
}
.step-text {
  font-size: 1rem;
  color: #2d3a5a;
  line-height: 1.6;
}

/* GROUP HEADER */
.group-heading {
  font-family: 'Montserrat', Arial, sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #2c3e6b;
  margin: 18px 0 10px;
  padding-left: 4px;
  border-left: 4px solid #f4a7b5;
  padding-left: 10px;
}

/* bullet group */
.bullet-group {
  background: #e8eef8;
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 14px;
  box-shadow: 0 2px 10px rgba(60,100,180,0.08);
}
.bullet-group-label {
  font-family: 'Montserrat', Arial, sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #2c3e6b;
  margin-bottom: 8px;
}
.bullet-item {
  font-size: 0.97rem;
  color: #2d3a5a;
  line-height: 1.55;
  padding-left: 22px;
  position: relative;
  margin-bottom: 5px;
}
.bullet-item::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f4a7b5;
}

/* HEADING block */
.section-heading {
  font-family: 'Montserrat', Arial, sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e6b;
  margin: 22px 0 10px;
}

/* PARA block */
.para-block {
  font-size: 0.97rem;
  color: #3a4560;
  line-height: 1.65;
  margin-bottom: 14px;
  background: rgba(255,255,255,0.60);
  border-radius: 12px;
  padding: 12px 18px;
}

/* cloud-shaped divider */
.divider {
  border: none;
  text-align: center;
  margin: 18px 0;
  height: 20px;
  background: none;
  position: relative;
}
.divider::before {
  content: '☁ ☁ ☁';
  font-size: 1.4rem;
  color: rgba(255,255,255,0.9);
  letter-spacing: 8px;
}

/* FOOTER */
.footer {
  margin-top: 40px;
  padding: 20px;
  background: rgba(255,255,255,0.55);
  border-radius: 16px;
  text-align: center;
  font-size: 0.8rem;
  color: #5570a0;
  font-family: 'Nunito', sans-serif;
  box-shadow: 0 2px 10px rgba(60,100,180,0.08);
}
.footer img {
  height: 28px;
  vertical-align: middle;
  margin-right: 6px;
  border-radius: 6px;
}

@media (max-width: 600px) {
  .hero { padding: 24px 18px 22px; border-radius: 0 0 24px 24px; }
  .hero-title { font-size: 1.6rem; }
  .step-card { flex-direction: column; gap: 12px; }
  .step-badge { width: 56px; height: 56px; }
  .field-card { flex-direction: column; gap: 4px; }
  .field-label { min-width: unset; }
}
</style>
</head>
<body>
<div class="page">

  <div class="hero">
    <h1 class="hero-title">{{ title }}</h1>
  </div>

  {% set ns = namespace(step_idx=0) %}
  {% for b in blocks %}

    {% if b.type == 'field' %}
    <div class="field-card">
      <div class="field-label">{{ b.label | md }}</div>
      <div class="field-value">{{ b.value | md }}</div>
    </div>

    {% elif b.type == 'group' and b.ordered %}
    {% if b.label %}
    <div class="group-heading">{{ b.label | md }}</div>
    {% endif %}
    {% for item in b['items'] %}
    <div class="step-card">
      <div class="step-badge">
        <span class="step-badge-label">ШАГ</span>
        <span class="step-badge-num">{{ loop.index }}</span>
      </div>
      <div class="step-body">
        <div class="step-text">{{ item | md }}</div>
      </div>
    </div>
    {% set ns.step_idx = ns.step_idx + 1 %}
    {% endfor %}

    {% elif b.type == 'group' and not b.ordered %}
    <div class="bullet-group">
      {% if b.label %}
      <div class="bullet-group-label">{{ b.label | md }}</div>
      {% endif %}
      {% for item in b['items'] %}
      <div class="bullet-item">{{ item | md }}</div>
      {% endfor %}
    </div>

    {% elif b.type == 'heading' %}
    <div class="section-heading">{{ b.text | md }}</div>

    {% elif b.type == 'para' %}
    <div class="para-block">{{ b.text | md }}</div>

    {% elif b.type == 'divider' %}
    <div class="divider"></div>

    {% endif %}
  {% endfor %}

  <div class="footer">
    {% if logo_b64 %}<img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA logo">{% endif %}
    Создано в&nbsp;<strong>SUMMARA</strong>
  </div>

</div>
</body>
</html>"""
