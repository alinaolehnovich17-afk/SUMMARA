# _tpl_a.py — Jinja2-шаблоны для SUMMARA
# CALM_PLAN  — природно-зелёный wellness timeline (ref: primer/1.jpg)
# CORPORATE  — тёмно-синяя корпоративная сетка  (ref: primer/2.jpg)
# DOODLE     — скетч/doodle с речевыми пузырями  (ref: primer/3.jpg)

# ---------------------------------------------------------------------------
# CALM_PLAN
# ---------------------------------------------------------------------------
CALM_PLAN = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Nunito', 'Segoe UI', Arial, sans-serif;
  background: #f7f5f0;
  color: #3a3a2e;
  min-height: 100vh;
  padding: 40px 16px 60px;
}

.page {
  max-width: 820px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 32px rgba(80,90,40,0.10);
}

/* ---- HERO ---- */
.hero {
  background: #3d5a2a;
  color: #ffffff;
  padding: 48px 56px 40px;
}

.hero-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #b8cc84;
  margin-bottom: 14px;
}

.hero h1 {
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 800;
  line-height: 1.15;
  color: #f0eed8;
}

/* ---- CONTENT ---- */
.content {
  padding: 0 0 40px;
}

/* ---- TIMELINE ---- */
.timeline {
  position: relative;
  padding: 40px 48px 8px 48px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 83px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to bottom, #6a8c3a 0%, #b5c98a 100%);
  border-radius: 2px;
}

.tl-item {
  display: flex;
  gap: 24px;
  margin-bottom: 36px;
  position: relative;
}

.tl-num {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #4a7030;
  color: #fff;
  font-size: 22px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  box-shadow: 0 2px 12px rgba(74,112,48,0.35);
}

.tl-body {
  flex: 1;
  padding-top: 8px;
}

.tl-label {
  font-size: 16px;
  font-weight: 700;
  color: #3d5a2a;
  margin-bottom: 8px;
}

.tl-value {
  font-size: 14px;
  color: #555c40;
  line-height: 1.65;
}

/* ---- GROUP (ordered) as timeline steps ---- */
.tl-steps {
  list-style: none;
  counter-reset: tl-counter;
  position: relative;
  padding: 32px 48px 8px 48px;
}

.tl-steps::before {
  content: '';
  position: absolute;
  left: 83px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to bottom, #6a8c3a 0%, #b5c98a 100%);
  border-radius: 2px;
}

.tl-steps li {
  display: flex;
  gap: 24px;
  margin-bottom: 28px;
  counter-increment: tl-counter;
  position: relative;
}

.tl-steps li::before {
  content: counter(tl-counter);
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #7aaa46;
  color: #fff;
  font-size: 18px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  box-shadow: 0 2px 10px rgba(74,112,48,0.28);
}

.tl-steps li span {
  padding-top: 10px;
  font-size: 14px;
  color: #444a30;
  line-height: 1.65;
  flex: 1;
}

/* ---- GROUP (unordered) ---- */
.group-section {
  padding: 20px 48px;
}

.group-label {
  font-size: 15px;
  font-weight: 700;
  color: #3d5a2a;
  margin-bottom: 10px;
}

.bullet-list {
  list-style: none;
  padding: 0;
}

.bullet-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #444a30;
  line-height: 1.65;
}

.bullet-list li::before {
  content: '';
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #7aaa46;
  margin-top: 7px;
}

/* ---- HEADING / PARA / DIVIDER ---- */
.sec-heading {
  padding: 20px 48px 6px;
  font-size: 17px;
  font-weight: 700;
  color: #3d5a2a;
}

.para {
  padding: 8px 48px;
  font-size: 14px;
  color: #555c40;
  line-height: 1.7;
}

.divider {
  margin: 20px 48px;
  border: none;
  border-top: 1.5px solid #d4e0b8;
}

/* ---- FIELD (generic) ---- */
.field-row {
  display: flex;
  gap: 0;
  padding: 10px 48px;
}

.field-label {
  font-size: 13px;
  font-weight: 700;
  color: #7a9450;
  min-width: 140px;
  flex-shrink: 0;
  padding-top: 1px;
}

.field-value {
  font-size: 14px;
  color: #3a3a2e;
  line-height: 1.6;
  flex: 1;
}

/* ---- BADGE ---- */
.badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 24px 48px;
  border-top: 1.5px solid #e0e8cc;
  color: #9aac70;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.badge img {
  height: 28px;
  width: auto;
  border-radius: 4px;
  opacity: 0.75;
}

@media (max-width: 540px) {
  .hero { padding: 32px 24px 28px; }
  .timeline, .tl-steps, .group-section, .field-row, .sec-heading, .para, .divider {
    padding-left: 20px; padding-right: 20px;
  }
  .timeline::before, .tl-steps::before { left: 42px; }
  .badge { padding: 18px 20px; }
}
</style>
</head>
<body>
<div class="page">
  <div class="hero">
    <h1>{{ title }}</h1>
  </div>
  <div class="content">
{% for b in blocks %}
{% if b['type'] == 'field' %}
    <div class="field-row">
      <div class="field-label">{{ b['label'] | md }}</div>
      <div class="field-value">{{ b['value'] | md }}</div>
    </div>
{% elif b['type'] == 'group' and b['ordered'] %}
{% if b['label'] %}
    <div class="group-label" style="padding: 20px 48px 0;">{{ b['label'] | md }}</div>
{% endif %}
    <ol class="tl-steps">
{% for item in b['items'] %}
      <li><span>{{ item | md }}</span></li>
{% endfor %}
    </ol>
{% elif b['type'] == 'group' %}
    <div class="group-section">
{% if b['label'] %}
      <div class="group-label">{{ b['label'] | md }}</div>
{% endif %}
      <ul class="bullet-list">
{% for item in b['items'] %}
        <li><span>{{ item | md }}</span></li>
{% endfor %}
      </ul>
    </div>
{% elif b['type'] == 'heading' %}
    <div class="sec-heading">{{ b['text'] | md }}</div>
{% elif b['type'] == 'para' %}
    <div class="para">{{ b['text'] | md }}</div>
{% elif b['type'] == 'divider' %}
    <hr class="divider">
{% endif %}
{% endfor %}
  </div>
  <div class="badge">
{% if logo_b64 %}
    <img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA">
{% endif %}
    Создано в SUMMARA
  </div>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CORPORATE
# ---------------------------------------------------------------------------
CORPORATE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  background: #e8edf4;
  color: #1a2740;
  min-height: 100vh;
  padding: 48px 16px 64px;
}

.page {
  max-width: 820px;
  margin: 0 auto;
  background: #ffffff;
  box-shadow: 0 2px 24px rgba(15,30,60,0.12);
}

/* ---- HEADER ---- */
.corp-header {
  padding: 56px 56px 36px;
  border-bottom: 3px solid #1f3a5f;
}

.corp-doctype {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #4a6fa5;
  margin-bottom: 18px;
}

.corp-header h1 {
  font-family: 'Montserrat', 'Inter', sans-serif;
  font-size: clamp(28px, 4.5vw, 48px);
  font-weight: 800;
  line-height: 1.1;
  color: #1f3a5f;
  letter-spacing: -0.5px;
}

/* ---- GRID BODY ---- */
.corp-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid #c8d4e4;
}

.corp-body.single {
  grid-template-columns: 1fr;
}

/* ---- FIELD ---- */
.corp-field {
  padding: 24px 32px;
  border-bottom: 1px solid #dce5f0;
  border-right: 1px solid #dce5f0;
}

.corp-field:nth-child(2n) {
  border-right: none;
}

.corp-field-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #4a6fa5;
  margin-bottom: 6px;
}

.corp-field-value {
  font-size: 15px;
  font-weight: 500;
  color: #1a2740;
  line-height: 1.55;
}

/* ---- FULL-WIDTH WRAPPER ---- */
.corp-full {
  grid-column: 1 / -1;
  border-bottom: 1px solid #dce5f0;
}

/* ---- GROUP ---- */
.corp-group {
  padding: 28px 32px;
}

.corp-group-label {
  font-family: 'Montserrat', 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #1f3a5f;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #1f3a5f;
  display: inline-block;
}

.corp-ol {
  list-style: none;
  counter-reset: corp-counter;
  padding: 0;
}

.corp-ol li {
  counter-increment: corp-counter;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #2a3a54;
  line-height: 1.6;
}

.corp-ol li::before {
  content: counter(corp-counter, decimal-leading-zero);
  flex-shrink: 0;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #ffffff;
  background: #1f3a5f;
  width: 28px;
  height: 28px;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1px;
}

.corp-ul {
  list-style: none;
  padding: 0;
}

.corp-ul li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #2a3a54;
  line-height: 1.6;
}

.corp-ul li::before {
  content: '';
  flex-shrink: 0;
  width: 5px;
  height: 5px;
  background: #1f3a5f;
  margin-top: 8px;
  border-radius: 1px;
}

/* ---- HEADING / PARA / DIVIDER ---- */
.corp-heading {
  grid-column: 1 / -1;
  padding: 20px 32px 8px;
  border-bottom: 1px solid #dce5f0;
  font-family: 'Montserrat', 'Inter', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1f3a5f;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.corp-para {
  grid-column: 1 / -1;
  padding: 12px 32px;
  border-bottom: 1px solid #dce5f0;
  font-size: 14px;
  color: #3a4d6a;
  line-height: 1.7;
}

.corp-divider {
  grid-column: 1 / -1;
  border: none;
  border-top: 2px solid #1f3a5f;
  margin: 0;
}

/* ---- FOOTER / BADGE ---- */
.corp-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 32px;
  border-top: 3px solid #1f3a5f;
  background: #f5f7fb;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #4a6fa5;
}

.corp-footer img {
  height: 22px;
  width: auto;
  border-radius: 3px;
  opacity: 0.7;
}

@media (max-width: 560px) {
  .corp-header { padding: 32px 20px 24px; }
  .corp-body { grid-template-columns: 1fr; }
  .corp-field { border-right: none; }
  .corp-group, .corp-field { padding: 18px 20px; }
  .corp-heading, .corp-para { padding-left: 20px; padding-right: 20px; }
  .corp-footer { padding: 14px 20px; }
}
</style>
</head>
<body>
<div class="page">
  <div class="corp-header">
    <h1>{{ title }}</h1>
  </div>
  <div class="corp-body">
{% for b in blocks %}
{% if b['type'] == 'field' %}
    <div class="corp-field">
      <div class="corp-field-label">{{ b['label'] | md }}</div>
      <div class="corp-field-value">{{ b['value'] | md }}</div>
    </div>
{% elif b['type'] == 'group' %}
    <div class="corp-full">
      <div class="corp-group">
{% if b['label'] %}
        <div class="corp-group-label">{{ b['label'] | md }}</div>
{% endif %}
{% if b['ordered'] %}
        <ol class="corp-ol">
{% for item in b['items'] %}
          <li>{{ item | md }}</li>
{% endfor %}
        </ol>
{% else %}
        <ul class="corp-ul">
{% for item in b['items'] %}
          <li>{{ item | md }}</li>
{% endfor %}
        </ul>
{% endif %}
      </div>
    </div>
{% elif b['type'] == 'heading' %}
    <div class="corp-heading">{{ b['text'] | md }}</div>
{% elif b['type'] == 'para' %}
    <div class="corp-para">{{ b['text'] | md }}</div>
{% elif b['type'] == 'divider' %}
    <hr class="corp-divider">
{% endif %}
{% endfor %}
  </div>
  <div class="corp-footer">
{% if logo_b64 %}
    <img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA">
{% endif %}
    Создано в SUMMARA
  </div>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# DOODLE
# ---------------------------------------------------------------------------
DOODLE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=Comfortaa:wght@400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Comfortaa', 'Segoe UI', Arial, sans-serif;
  background: #e8e6e0;
  color: #2a2a2a;
  min-height: 100vh;
  padding: 40px 16px 60px;
}

.page {
  max-width: 820px;
  margin: 0 auto;
  background: #f2f0eb;
  border-radius: 8px;
  position: relative;
  padding: 0 0 40px;
}

/* ---- DOODLE STAR DECORATIONS ---- */
.page::before,
.page::after {
  font-family: sans-serif;
  position: absolute;
  font-size: 28px;
  color: #2a2a2a;
  pointer-events: none;
}

.page::before {
  content: '✳';
  top: 28px;
  left: 28px;
  opacity: 0.6;
}

.page::after {
  content: '✳';
  top: 28px;
  right: 28px;
  opacity: 0.6;
  font-size: 20px;
}

/* ---- HERO ---- */
.doodle-hero {
  text-align: center;
  padding: 60px 48px 32px;
  position: relative;
}

.doodle-hero h1 {
  font-family: 'Caveat', cursive, sans-serif;
  font-size: clamp(32px, 6vw, 58px);
  font-weight: 700;
  color: #1e1e1e;
  line-height: 1.2;
  position: relative;
  display: inline-block;
}

.doodle-hero h1::after {
  content: '';
  display: block;
  width: 60%;
  height: 3px;
  background: #2a2a2a;
  margin: 10px auto 0;
  border-radius: 2px;
}

.doodle-doctype {
  font-family: 'Caveat', cursive;
  font-size: 15px;
  color: #888;
  margin-top: 10px;
  text-align: center;
}

/* ---- CONTENT ---- */
.doodle-content {
  padding: 8px 40px;
}

/* ---- FIELD as speech bubble ---- */
.bubble-wrap {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.bubble-wrap.right {
  align-items: flex-end;
}

.bubble {
  position: relative;
  background: #ffffff;
  border: 2.5px solid #2a2a2a;
  border-radius: 22px 22px 22px 4px;
  padding: 14px 20px;
  max-width: 88%;
  box-shadow: 3px 3px 0 #c8c5be;
}

.bubble.right {
  border-radius: 22px 22px 4px 22px;
  box-shadow: -3px 3px 0 #c8c5be;
}

.bubble-label {
  font-family: 'Caveat', cursive;
  font-size: 13px;
  font-weight: 600;
  color: #888;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.bubble-value {
  font-family: 'Comfortaa', sans-serif;
  font-size: 14px;
  color: #1e1e1e;
  line-height: 1.6;
}

/* ---- GROUP (ordered) as numbered doodle steps ---- */
.doodle-steps {
  margin: 16px 0;
}

.doodle-step-label {
  font-family: 'Caveat', cursive;
  font-size: 20px;
  font-weight: 700;
  color: #2a2a2a;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.doodle-step-label::before {
  content: '';
  display: inline-block;
  width: 24px;
  height: 3px;
  background: #f5b800;
  border-radius: 2px;
}

.doodle-step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.step-num-bubble {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  background: #f5b800;
  border: 2.5px solid #2a2a2a;
  border-radius: 50% 50% 50% 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Caveat', cursive;
  font-size: 24px;
  font-weight: 700;
  color: #1e1e1e;
  box-shadow: 2px 2px 0 #c8a000;
}

.step-text-bubble {
  flex: 1;
  background: #ffffff;
  border: 2px solid #2a2a2a;
  border-radius: 16px 16px 16px 4px;
  padding: 12px 16px;
  font-family: 'Comfortaa', sans-serif;
  font-size: 14px;
  color: #1e1e1e;
  line-height: 1.6;
  box-shadow: 2px 2px 0 #c8c5be;
  margin-top: 4px;
}

/* arrow connector */
.step-arrow {
  text-align: center;
  font-size: 20px;
  color: #aaa;
  margin: -8px 0 -8px 24px;
  line-height: 1;
}

/* ---- GROUP (unordered) ---- */
.doodle-ul-section {
  margin: 16px 0;
}

.doodle-ul-label {
  font-family: 'Caveat', cursive;
  font-size: 20px;
  font-weight: 700;
  color: #2a2a2a;
  margin-bottom: 10px;
}

.doodle-ul {
  list-style: none;
  padding: 0;
}

.doodle-ul li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
  font-family: 'Comfortaa', sans-serif;
  font-size: 14px;
  color: #1e1e1e;
  line-height: 1.6;
}

.doodle-ul li::before {
  content: '★';
  color: #f5b800;
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}

/* ---- HEADING / PARA ---- */
.doodle-heading {
  font-family: 'Caveat', cursive;
  font-size: 24px;
  font-weight: 700;
  color: #1e1e1e;
  margin: 24px 0 8px;
  position: relative;
  display: inline-block;
}

.doodle-heading::after {
  content: '';
  display: block;
  width: 100%;
  height: 2.5px;
  background: #f5b800;
  border-radius: 2px;
  margin-top: 3px;
}

.doodle-para {
  font-family: 'Comfortaa', sans-serif;
  font-size: 14px;
  color: #3a3a3a;
  line-height: 1.75;
  margin: 10px 0;
  text-align: center;
  padding: 0 16px;
}

/* ---- DIVIDER ---- */
.doodle-divider {
  border: none;
  border-top: 2.5px dashed #c8c5be;
  margin: 24px 0;
}

/* ---- BADGE ---- */
.doodle-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 32px 40px 0;
  padding: 14px 24px;
  background: #ffffff;
  border: 2px solid #2a2a2a;
  border-radius: 12px;
  box-shadow: 3px 3px 0 #c8c5be;
  font-family: 'Caveat', cursive;
  font-size: 16px;
  color: #555;
}

.doodle-badge img {
  height: 26px;
  width: auto;
  border-radius: 4px;
}

/* ---- DECORATIVE STAR (inline) ---- */
.star-deco {
  display: inline-block;
  color: #f5b800;
  font-size: 18px;
  margin: 0 4px;
  vertical-align: middle;
}

@media (max-width: 540px) {
  .doodle-hero { padding: 48px 20px 24px; }
  .doodle-content { padding: 8px 16px; }
  .doodle-badge { margin: 24px 16px 0; }
  .page::before, .page::after { font-size: 20px; top: 16px; left: 14px; right: 14px; }
}
</style>
</head>
<body>
<div class="page">
  <div class="doodle-hero">
    <h1>{{ title }}</h1>
  </div>
  <div class="doodle-content">
{% for b in blocks %}
{% if b['type'] == 'field' %}
    <div class="bubble-wrap{% if loop.index is even %} right{% endif %}">
      <div class="bubble{% if loop.index is even %} right{% endif %}">
        <div class="bubble-label">{{ b['label'] | md }}</div>
        <div class="bubble-value">{{ b['value'] | md }}</div>
      </div>
    </div>
{% elif b['type'] == 'group' and b['ordered'] %}
    <div class="doodle-steps">
{% if b['label'] %}
      <div class="doodle-step-label">{{ b['label'] | md }}</div>
{% endif %}
{% for item in b['items'] %}
      <div class="doodle-step-item">
        <div class="step-num-bubble">{{ loop.index }}</div>
        <div class="step-text-bubble">{{ item | md }}</div>
      </div>
{% if not loop.last %}
      <div class="step-arrow">↓</div>
{% endif %}
{% endfor %}
    </div>
{% elif b['type'] == 'group' %}
    <div class="doodle-ul-section">
{% if b['label'] %}
      <div class="doodle-ul-label">{{ b['label'] | md }}</div>
{% endif %}
      <ul class="doodle-ul">
{% for item in b['items'] %}
        <li>{{ item | md }}</li>
{% endfor %}
      </ul>
    </div>
{% elif b['type'] == 'heading' %}
    <div class="doodle-heading">{{ b['text'] | md }}</div>
{% elif b['type'] == 'para' %}
    <div class="doodle-para">{{ b['text'] | md }}</div>
{% elif b['type'] == 'divider' %}
    <hr class="doodle-divider">
{% endif %}
{% endfor %}
  </div>
  <div class="doodle-badge">
{% if logo_b64 %}
    <img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA">
{% endif %}
    <span class="star-deco">✳</span> Создано в SUMMARA <span class="star-deco">✳</span>
  </div>
</div>
</body>
</html>"""
