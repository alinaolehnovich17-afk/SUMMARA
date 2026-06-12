"""
Дополнительные яркие/сочные шаблоны лэндингов (авторские, не из primer/):
- NEON  — тёмный неон-киберпанк со свечением
- JUICY — сочные тропические градиенты

Контракт блоков — см. agents/html_export.py (field/group(ordered)/heading/para/divider).
Доступ к items через b['items'] (b.items конфликтует с методом dict).
"""

# ── NEON: тёмный фон, неоновое свечение ───────────────────────────────────────
NEON = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Rajdhani', 'Segoe UI', Arial, sans-serif;
  background: #0a0718;
  background-image:
    radial-gradient(circle at 15% 10%, rgba(0,229,255,0.18), transparent 40%),
    radial-gradient(circle at 85% 20%, rgba(255,0,200,0.20), transparent 42%),
    radial-gradient(circle at 50% 100%, rgba(124,77,255,0.22), transparent 45%),
    linear-gradient(160deg, #0f0c29 0%, #1a1340 55%, #24122e 100%);
  background-attachment: fixed;
  min-height: 100vh;
  padding: 0 0 60px;
  color: #e8eaff;
}
.page { max-width: 840px; margin: 0 auto; padding: 0 18px; }

/* HERO */
.hero {
  text-align: center;
  padding: 54px 26px 40px;
  margin-bottom: 30px;
}
.hero h1 {
  font-family: 'Orbitron', 'Rajdhani', sans-serif;
  font-size: 2.5rem;
  font-weight: 900;
  line-height: 1.18;
  letter-spacing: 1px;
  color: #fff;
  text-shadow:
    0 0 8px rgba(0,229,255,0.9),
    0 0 22px rgba(0,229,255,0.6),
    0 0 40px rgba(255,0,200,0.5);
}
.hero::after {
  content: '';
  display: block;
  width: 160px; height: 4px;
  margin: 22px auto 0;
  border-radius: 4px;
  background: linear-gradient(90deg, #00e5ff, #ff00c8, #7c4dff);
  box-shadow: 0 0 14px rgba(0,229,255,0.8);
}

/* FIELD */
.field {
  background: rgba(20,16,46,0.7);
  border: 1px solid rgba(0,229,255,0.35);
  border-radius: 14px;
  padding: 16px 22px;
  margin-bottom: 14px;
  box-shadow: 0 0 18px rgba(0,229,255,0.10), inset 0 0 22px rgba(124,77,255,0.06);
  display: flex; gap: 16px; align-items: baseline;
}
.field .lbl {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  color: #00e5ff;
  text-shadow: 0 0 8px rgba(0,229,255,0.7);
  flex-shrink: 0; min-width: 110px;
}
.field .val { font-size: 1.08rem; color: #f0f2ff; line-height: 1.5; }

/* GROUP HEADING */
.ghead {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.05rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase;
  color: #ff5edb;
  text-shadow: 0 0 10px rgba(255,0,200,0.6);
  margin: 26px 0 14px;
}

/* ORDERED STEP */
.step { display: flex; gap: 18px; align-items: center; margin-bottom: 16px; }
.step .num {
  flex-shrink: 0;
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 1.3rem;
  color: #0a0718;
  background: linear-gradient(135deg, #00e5ff, #7c4dff);
  box-shadow: 0 0 16px rgba(0,229,255,0.8), 0 0 30px rgba(124,77,255,0.6);
}
.step .txt {
  flex: 1;
  background: rgba(20,16,46,0.7);
  border: 1px solid rgba(255,0,200,0.30);
  border-radius: 12px; padding: 14px 18px;
  font-size: 1.04rem; color: #f0f2ff; line-height: 1.5;
  box-shadow: 0 0 16px rgba(255,0,200,0.08);
}

/* UNORDERED GROUP */
.bgroup {
  background: rgba(20,16,46,0.6);
  border: 1px solid rgba(124,77,255,0.35);
  border-radius: 14px; padding: 16px 22px; margin-bottom: 14px;
  box-shadow: 0 0 18px rgba(124,77,255,0.10);
}
.bitem { position: relative; padding-left: 26px; margin-bottom: 8px; font-size: 1.02rem; color: #e8eaff; line-height: 1.55; }
.bitem::before {
  content: ''; position: absolute; left: 6px; top: 8px;
  width: 10px; height: 10px; border-radius: 50%;
  background: #00e5ff; box-shadow: 0 0 10px rgba(0,229,255,0.9);
}

/* HEADING / PARA / DIVIDER */
.heading {
  font-family: 'Orbitron', sans-serif; font-size: 1.25rem; font-weight: 700;
  color: #b388ff; text-shadow: 0 0 10px rgba(124,77,255,0.6);
  margin: 24px 0 12px;
}
.para { font-size: 1.02rem; line-height: 1.7; color: #cdd2f5; margin-bottom: 14px; }
.divider { height: 2px; border: none; margin: 22px 0;
  background: linear-gradient(90deg, transparent, #00e5ff, #ff00c8, transparent);
  box-shadow: 0 0 12px rgba(255,0,200,0.5); }

/* FOOTER */
.footer {
  margin-top: 40px; text-align: center; font-size: 0.82rem;
  color: #8a90c8; letter-spacing: 0.5px;
  padding-top: 20px; border-top: 1px solid rgba(124,77,255,0.25);
}
.footer img { height: 26px; vertical-align: middle; margin-right: 7px; border-radius: 6px; box-shadow: 0 0 10px rgba(0,229,255,0.5); }
.footer strong { color: #00e5ff; text-shadow: 0 0 8px rgba(0,229,255,0.6); }

@media (max-width: 600px) {
  .hero h1 { font-size: 1.8rem; }
  .field { flex-direction: column; gap: 4px; }
  .field .lbl { min-width: unset; }
  .step { flex-direction: column; align-items: flex-start; gap: 10px; }
}
</style>
</head>
<body>
<div class="page">
  <div class="hero"><h1>{{ title }}</h1></div>
  {% for b in blocks %}
    {% if b.type == 'field' %}
    <div class="field"><div class="lbl">{{ b.label | md }}</div><div class="val">{{ b.value | md }}</div></div>
    {% elif b.type == 'group' and b.ordered %}
      {% if b.label %}<div class="ghead">{{ b.label | md }}</div>{% endif %}
      {% for item in b['items'] %}
      <div class="step"><div class="num">{{ loop.index }}</div><div class="txt">{{ item | md }}</div></div>
      {% endfor %}
    {% elif b.type == 'group' and not b.ordered %}
    <div class="bgroup">
      {% if b.label %}<div class="ghead" style="margin-top:0">{{ b.label | md }}</div>{% endif %}
      {% for item in b['items'] %}<div class="bitem">{{ item | md }}</div>{% endfor %}
    </div>
    {% elif b.type == 'heading' %}
    <div class="heading">{{ b.text | md }}</div>
    {% elif b.type == 'para' %}
    <div class="para">{{ b.text | md }}</div>
    {% elif b.type == 'divider' %}
    <hr class="divider">
    {% endif %}
  {% endfor %}
  <div class="footer">
    {% if logo_b64 %}<img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA">{% endif %}
    Создано в&nbsp;<strong>SUMMARA</strong>
  </div>
</div>
</body>
</html>"""


# ── JUICY: сочные тропические градиенты ───────────────────────────────────────
JUICY = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Poppins', 'Segoe UI', Arial, sans-serif;
  background: linear-gradient(135deg, #ff6ec4 0%, #ff9a44 35%, #ffd86f 65%, #7ee8fa 100%);
  background-attachment: fixed;
  min-height: 100vh;
  padding: 0 0 60px;
  color: #2b2240;
}
.page { max-width: 840px; margin: 0 auto; padding: 0 18px; }

/* HERO */
.hero {
  text-align: center;
  padding: 50px 30px 40px;
  margin-bottom: 28px;
}
.hero h1 {
  font-family: 'Baloo 2', 'Poppins', sans-serif;
  font-size: 2.6rem; font-weight: 800; line-height: 1.15;
  color: #fff;
  text-shadow: 0 4px 0 rgba(255,90,160,0.45), 0 8px 24px rgba(120,40,90,0.35);
}
.hero::after {
  content: '🍊 🍓 🥭 🫐';
  display: block; margin-top: 14px; font-size: 1.5rem; letter-spacing: 8px;
}

/* generic card */
.card {
  background: rgba(255,255,255,0.92);
  border-radius: 22px;
  padding: 18px 24px;
  margin-bottom: 16px;
  box-shadow: 0 10px 26px rgba(180,60,120,0.22);
}

/* FIELD — colorful left accent bar, цвет циклически */
.field {
  position: relative; overflow: hidden;
  display: flex; gap: 16px; align-items: baseline;
}
.field::before {
  content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 8px;
}
.field.c0::before { background: linear-gradient(#ff5ea8, #ff2d6f); }
.field.c1::before { background: linear-gradient(#ff9a44, #ff6a00); }
.field.c2::before { background: linear-gradient(#16c79a, #00a36c); }
.field.c3::before { background: linear-gradient(#7b6cff, #4a2fe7); }
.field.c4::before { background: linear-gradient(#23bcf0, #0a8ed9); }
.field .lbl {
  font-family: 'Baloo 2', sans-serif; font-weight: 700; font-size: 0.82rem;
  text-transform: uppercase; letter-spacing: 0.6px; color: #d62f7a;
  flex-shrink: 0; min-width: 104px; padding-left: 8px;
}
.field.c1 .lbl { color: #e06000; }
.field.c2 .lbl { color: #008a5c; }
.field.c3 .lbl { color: #5a3fe0; }
.field.c4 .lbl { color: #0a82c4; }
.field .val { font-size: 1.06rem; color: #34243f; line-height: 1.5; }

/* GROUP HEADING */
.ghead {
  font-family: 'Baloo 2', sans-serif; font-size: 1.3rem; font-weight: 800;
  color: #fff; text-shadow: 0 3px 0 rgba(220,47,122,0.4);
  margin: 26px 0 14px;
}

/* ORDERED STEP — juicy gradient badges */
.step {
  background: rgba(255,255,255,0.94);
  border-radius: 20px; padding: 16px 22px; margin-bottom: 14px;
  box-shadow: 0 8px 22px rgba(180,60,120,0.20);
  display: flex; gap: 18px; align-items: center;
}
.step .num {
  flex-shrink: 0; width: 58px; height: 58px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Baloo 2', sans-serif; font-weight: 800; font-size: 1.5rem; color: #fff;
  box-shadow: 0 6px 16px rgba(0,0,0,0.18);
}
.step.c0 .num { background: linear-gradient(135deg, #ff7eb3, #ff2d6f); }
.step.c1 .num { background: linear-gradient(135deg, #ffb347, #ff6a00); }
.step.c2 .num { background: linear-gradient(135deg, #43e97b, #11998e); }
.step.c3 .num { background: linear-gradient(135deg, #a18cd1, #5a2ff0); }
.step.c4 .num { background: linear-gradient(135deg, #4facfe, #0a8ed9); }
.step .txt { flex: 1; font-size: 1.05rem; color: #34243f; line-height: 1.5; }

/* UNORDERED GROUP */
.bitem { position: relative; padding-left: 26px; margin-bottom: 8px; font-size: 1.02rem; color: #34243f; line-height: 1.55; }
.bitem::before {
  content: ''; position: absolute; left: 4px; top: 7px;
  width: 12px; height: 12px; border-radius: 50%;
  background: linear-gradient(135deg, #ff5ea8, #ff9a44);
}

/* HEADING / PARA / DIVIDER */
.heading { font-family: 'Baloo 2', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff; text-shadow: 0 3px 0 rgba(220,47,122,0.4); margin: 24px 0 12px; }
.para { font-size: 1.02rem; line-height: 1.7; color: #3a2c46; }
.divider { height: 6px; border: none; border-radius: 6px; margin: 22px 0;
  background: linear-gradient(90deg, #ff5ea8, #ff9a44, #ffd86f, #43e97b, #4facfe); }

/* FOOTER */
.footer {
  margin-top: 38px; text-align: center; font-size: 0.84rem;
  color: #fff; padding: 16px; background: rgba(255,255,255,0.20);
  border-radius: 18px; backdrop-filter: blur(4px);
}
.footer img { height: 28px; vertical-align: middle; margin-right: 7px; border-radius: 7px; }
.footer strong { color: #fff; }

@media (max-width: 600px) {
  .hero h1 { font-size: 1.9rem; }
  .field, .step { flex-direction: column; gap: 6px; align-items: flex-start; }
  .field .lbl { min-width: unset; }
}
</style>
</head>
<body>
<div class="page">
  <div class="hero"><h1>{{ title }}</h1></div>
  {% set ns = namespace(fi=0, si=0) %}
  {% for b in blocks %}
    {% if b.type == 'field' %}
    <div class="card field c{{ ns.fi % 5 }}"><div class="lbl">{{ b.label | md }}</div><div class="val">{{ b.value | md }}</div></div>
    {% set ns.fi = ns.fi + 1 %}
    {% elif b.type == 'group' and b.ordered %}
      {% if b.label %}<div class="ghead">{{ b.label | md }}</div>{% endif %}
      {% for item in b['items'] %}
      <div class="step c{{ (loop.index0) % 5 }}"><div class="num">{{ loop.index }}</div><div class="txt">{{ item | md }}</div></div>
      {% endfor %}
    {% elif b.type == 'group' and not b.ordered %}
    <div class="card">
      {% if b.label %}<div class="ghead" style="color:#d62f7a;text-shadow:none;margin-top:0">{{ b.label | md }}</div>{% endif %}
      {% for item in b['items'] %}<div class="bitem">{{ item | md }}</div>{% endfor %}
    </div>
    {% elif b.type == 'heading' %}
    <div class="heading">{{ b.text | md }}</div>
    {% elif b.type == 'para' %}
    <div class="card para">{{ b.text | md }}</div>
    {% elif b.type == 'divider' %}
    <hr class="divider">
    {% endif %}
  {% endfor %}
  <div class="footer">
    {% if logo_b64 %}<img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="SUMMARA">{% endif %}
    Создано в&nbsp;<strong>SUMMARA</strong>
  </div>
</div>
</body>
</html>"""
