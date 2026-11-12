import html, sys
from playwright.sync_api import sync_playwright

MAIL = '<svg viewBox="0 0 512 512" width="9" height="9"><path fill="currentColor" d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"/></svg>'
GLOBE = '<svg viewBox="0 0 512 512" width="9" height="9"><path fill="currentColor" d="M352 256c0 22.2-1.2 43.6-3.3 64H163.3c-2.2-20.4-3.3-41.8-3.3-64s1.2-43.6 3.3-64H348.7c2.2 20.4 3.3 41.8 3.3 64zm28.8-64H503.9c5.3 20.5 8.1 41.9 8.1 64s-2.8 43.5-8.1 64H380.8c2.1-20.6 3.2-42 3.2-64s-1.1-43.4-3.2-64zm112.6-32H376.7c-10-63.9-29.8-117.4-55.3-151.6c78.3 20.7 142 77.5 171.9 151.6zm-149.1 0H167.7c6.1-36.4 15.5-68.6 27-94.7c10.5-23.6 22.2-40.7 33.5-51.5C239.4 3.2 248.7 0 256 0s16.6 3.2 27.8 13.8c11.3 10.8 23 27.9 33.5 51.5c11.6 26 20.9 58.2 27 94.7zm-209 0H18.6C48.6 85.9 112.2 29.1 190.6 8.4C165.1 42.6 145.3 96.1 135.3 160zM8.1 192H131.2c-2.1 20.6-3.2 42-3.2 64s1.1 43.4 3.2 64H8.1C2.8 299.5 0 278.1 0 256s2.8-43.5 8.1-64zM194.7 446.6c-11.6-26-20.9-58.2-27-94.6H344.3c-6.1 36.4-15.5 68.6-27 94.6c-10.5 23.6-22.2 40.7-33.5 51.5C272.6 508.8 263.3 512 256 512s-16.6-3.2-27.8-13.8c-11.3-10.8-23-27.9-33.5-51.5zM135.3 352c10 63.9 29.8 117.4 55.3 151.6C112.2 482.9 48.6 426.1 18.6 352H135.3zm358.1 0c-30 74.1-93.6 130.9-171.9 151.6c25.5-34.2 45.2-87.7 55.3-151.6H493.4z"/></svg>'

CSS = r"""
@page { size: A4; margin: 15mm 17mm 18mm 17mm; }
* { box-sizing: border-box; }
html,body { margin:0; }
body { font-family: "Latin Modern Roman","LM Roman 10", %(cjk)s serif; font-size: 10.4pt; line-height: 1.36; color:#000; }
a { color:#1a1aa6; text-decoration:none; }
header { text-align:center; margin-bottom: 10pt; }
header h1 { font-size: 21pt; font-weight:700; letter-spacing:.02em; margin:0 0 6pt; %(h1extra)s }
header p { margin:1pt 0; font-size:10.4pt; }
header .sep { margin:0 5pt; }
header svg { vertical-align:-1px; margin-right:3pt; }
h2 { break-after: avoid; font-size: 10.8pt; font-weight:700; margin: 11pt 0 5pt; padding-bottom:1.5pt; border-bottom: .8pt solid #000; %(h2extra)s }
.in { padding-left: 18pt; }
.intro p { margin: 0 0 6pt; text-align: justify; }
.entry { margin: 0 0 7pt; break-inside: avoid; }
.row { display:flex; justify-content:space-between; gap:12pt; }
.row b { font-weight:700; }
.row i, .it { font-style: italic; %(itextra)s }
.row .r { white-space:nowrap; font-style:italic; %(itextra)s }
ul { margin: 2pt 0 0; padding-left: 14pt; }
li { margin: 0 0 1.5pt; text-align: justify; }
h3 { font-size: 10.8pt; font-weight:700; margin: 8pt 0 4pt; }
.paper { margin: 0 0 6pt; break-inside: avoid; }
.paper b { display:block; }
.paper small { font-size: 9.4pt; }
table { border-collapse: collapse; width:100%%; break-inside: avoid; }
td { vertical-align: top; padding: 1.5pt 0; }
td.k { white-space:nowrap; width: %(kw)s; font-weight:700; padding-right: 10pt; }
.fac td.k{width:160pt!important} .fac{font-size:9.6pt;break-inside:avoid} .refs { break-inside:avoid; display:grid; grid-template-columns: repeat(3,1fr); gap: 10pt; font-size: 9.4pt; line-height:1.3; }
.refs b { font-size: 10.4pt; }
"""

def esc(s): return s

def build(d, lang):
    cjk = '"Noto Serif CJK TC",' if lang=='zh' else '"Noto Serif CJK TC",'
    css = CSS % dict(cjk=cjk,
        h1extra = 'letter-spacing:.25em;' if lang=='zh' else 'text-transform:uppercase;',
        h2extra = 'letter-spacing:.12em;' if lang=='zh' else 'text-transform:uppercase; letter-spacing:.01em;',
        itextra = 'font-style:normal;' if lang=='zh' else '',
        kw = '100pt' if lang=='zh' else '74pt')
    if lang=='zh':
        css += 'body{font-family:"Noto Serif CJK TC",serif}' + 'body{font-size:9.9pt;line-height:1.42} .entry{margin-bottom:5pt} h2{margin:9pt 0 4pt} .intro p{margin-bottom:4pt} li{margin-bottom:1pt} h3{margin:6pt 0 3pt}'
    if lang=='en':
        css += '.intro p, li{text-align:left} ' + 'body{font-size:10pt;line-height:1.32} .entry{margin-bottom:5.5pt} h2{margin:9pt 0 4pt} .intro p{margin-bottom:4.5pt} li{margin-bottom:1pt}'
    o = [f'<!DOCTYPE html><html lang="{ "zh-Hant" if lang=="zh" else "en"}"><head><meta charset="utf-8"><style>{css}</style></head><body>']
    o.append(f'<header><h1>{d["name"]}</h1><p>{d["affil"]}</p>'
             f'<p><a href="mailto:r14341044@ntu.edu.tw">{MAIL}r14341044@ntu.edu.tw</a><span class="sep">⋄</span>'
             f'<a href="https://kane-yc-chen.github.io">{GLOBE}kane-yc-chen.github.io</a></p></header>')
    for sec in d['sections']:
        o.append(f'<h2>{sec["h"]}</h2>')
        kind = sec['kind']
        if kind=='intro':
            o.append('<div class="in intro">' + ''.join(f'<p>{p}</p>' for p in sec['ps']) + '</div>')
        elif kind=='entries':
            o.append('<div class="in">')
            for e in sec['items']:
                o.append('<div class="entry">')
                o.append(f'<div class="row"><b>{e["org"]}</b><span class="r">{e.get("right","")}</span></div>')
                for role in e.get('roles',[]):
                    if role['t'] or role.get('d'):
                        o.append(f'<div class="row"><i>{role["t"]}</i><span class="r">{role.get("d","")}</span></div>')
                    if role.get('b'):
                        o.append('<ul>' + ''.join(f'<li>{x}</li>' for x in role['b']) + '</ul>')
                if e.get('sub'):
                    o.append(f'<div>{e["sub"]}</div>')
                if e.get('b'):
                    o.append('<ul>' + ''.join(f'<li>{x}</li>' for x in e['b']) + '</ul>')
                o.append('</div>')
            o.append('</div>')
        elif kind=='research':
            o.append('<div class="in">')
            for g in sec['groups']:
                o.append(f'<h3>{g["h"]}</h3><ul>')
                for p in g['items']:
                    o.append(f'<li class="paper"><b>{p["t"]}</b><small>{p["s"]}</small></li>')
                o.append('</ul>')
            o.append('</div>')
        elif kind=='table':
            o.append('<div class="in"><table>' + ''.join(f'<tr><td class="k">{k}</td><td>{v}</td></tr>' for k,v in sec['rows']) + '</table></div>')
        elif kind=='faculty':
            o.append('<div class="in"><table class="fac">' + ''.join(f'<tr><td class="k">{k}</td><td>{v}</td></tr>' for k,v in sec['rows']) + '</table></div>')
        elif kind=='refs':
            o.append('<div class="in refs">' + ''.join('<div>' + '<br>'.join(r) + '</div>' for r in sec['items']) + '</div>')
    o.append('</body></html>')
    return ''.join(o)

# ---------------- ENGLISH ----------------
EN = dict(name='Yu-Cheng (Kane) Chen',
 affil='Graduate Institute of National Development <span class="sep">⋄</span> National Taiwan University',
 sections=[
 dict(h='Introduction', kind='intro', ps=[
  'I am a master’s student at the Graduate Institute of National Development, National Taiwan University. I am interested in how public institutions govern emerging technologies and how citizens take part in decisions about them. Drawing on deliberative democracy, my thesis will examine how members of the public, selected through sampling and brought together in a citizen deliberation, reason through the ethical and governance questions raised by prenatal and neonatal genetic testing in the era of next-generation sequencing.',
  'Beyond the thesis, I study the organizational forms through which the state acts. A National Science and Technology Council (NSTC) project compares institutional change and controversy in administrative corporations and government-endowed foundations. Two commissioned studies, one on whether the Center for Occupational Accident Prevention and Rehabilitation should become an administrative corporation and one on personnel and pay systems for the National Institute of Traditional Chinese Medicine, show how such bodies take shape in practice. I also contribute to an NSTC project on energy security and regional cooperation under geopolitical risk, and I use quantitative text analysis to compare how the Japanese and South Korean legislatures debate climate loss and damage.']),
 dict(h='Education', kind='entries', items=[
  dict(org='National Taiwan University', right='Sep 2025 – Present', sub='Master of Arts in National Development; GPA by semester: 4.00–4.10 (out of 4.30)<br>Thesis (planned): <i>The Right to Know and the Right Not to Know: Citizen Deliberation on Prenatal and Neonatal Genetic Testing in the Era of Next-Generation Sequencing</i><br>Advisor: Prof. Tze-Luen Lin; Co-advisor: Prof. Kuo-Hui Chang'),
  dict(org='University of Taipei', right='Sep 2024 – Jun 2025', sub='Pre-master’s student (accelerated B.A.–M.P.A. track), Master of Public Administration Program, Department of Social and Public Affairs'),
  dict(org='Jinan University, Guangzhou, China', right='Aug 2024 – Jan 2025', sub='Exchange Student, International Politics'),
  dict(org='University of Taipei', right='Sep 2021 – Jun 2025', sub='Bachelor of Arts in Social and Public Affairs; GPA by semester: 4.00–4.18 (out of 4.30)'),
 ]),
  dict(h='Research Experience', kind='entries', items=[
  dict(org='National Taiwan University', right='Taipei, Taiwan', roles=[dict(t='Graduate Research Assistant to Prof. Tze-Luen Lin', d='Jan 2026 – Present', b=[
   'NSTC project, <i>Energy Security, Key Energy Resource Risks, and Regional Cooperation Strategies under Geopolitics</i>.',
   'Joint study by National Taiwan University Hospital and National Taiwan University, <i>Exploring Parental Decision-Making and Ethical Issues in Prenatal and Neonatal Genetic Testing in the Next-Generation Sequencing Era</i> (from Feb 2026).'])]),
  dict(org='University of Taipei', right='Taipei, Taiwan', roles=[dict(t='Graduate Research Assistant to Assoc. Prof. Tien-Shen Li', d='Sep 2026 – Present', b=[
   'NSTC project, <i>Institutional Nodes and the Logic of Controversy Generation: A Comparative Analysis of Institutional Change in Quasi-Governmental Organizations, Focusing on Administrative Corporations and Government-Endowed Foundations</i> (from Oct 2026).',
   'Commissioned project, <i>Establishment of Personnel and Compensation Systems for the National Institute of Traditional Chinese Medicine</i>, an administrative corporation (from Oct 2026).'])]),
  dict(org='Taiwan Occupational Hygiene Association', right='Taipei, Taiwan', roles=[dict(t='Research Assistant to Adjunct Asst. Prof. Hui-Chen Tseng', d='Jan 2026 – Present', b=[
   'Commissioned study under the 2026 Program for Improving Medical Care, Rehabilitation and Return-to-Work Services for Occupationally Injured Workers, assessing whether the Center for Occupational Accident Prevention and Rehabilitation should become an administrative corporation.'])]),
  dict(org='University of Taipei', right='Taipei, Taiwan', roles=[
   dict(t='Undergraduate Research Assistant to Assoc. Prof. Tien-Shen Li', d='Sep 2023 – Jul 2024', b=[
    '<i>Planning the Transformation of Taipei City Hospital’s Management System</i> (planning study).',
    'USR Hub project, <i>Urban Regeneration Master Plan: A Community Revitalization Experiment with Local Participation</i> (Sep – Dec 2023).']),
   dict(t='Telephone Interviewer, then Administrative Assistant and Supervisor, Public Opinion and Policy Research Center', d='Sep 2021 – Aug 2023', b=[
    'Survey projects under the center’s director, Assoc. Prof. Tzu-Ping Liu, including an evaluation of pandemic relief measures for enterprises and workers by the Workforce Development Agency, Ministry of Labor; a public service satisfaction survey for the National Health Insurance Administration, Ministry of Health and Welfare; and a study of knowledge transfer and human factors in AI decision-making.']),
   ]),
 ]),
 dict(h='Internships', kind='entries', items=[
  dict(org='Public Affairs Intern, Department of Civil Affairs, Taipei City Government', right='Feb 2024 – Jun 2024', roles=[dict(t='', b=[
   'Internship project: citizen-facing services at Taipei’s household registration offices and the emotional labor of front-line staff, with the Wenshan and Datong District offices as case studies.'])]),
  dict(org='Public Affairs Intern, Environmental Jurists Association', right='Jul 2023 – Dec 2023', roles=[dict(t='', b=[
   'Internship project: the evolution of hillside development and building-control zones in Taipei, and how hillside housing relates to urban renewal and the reconstruction of old, structurally unsafe buildings.'])]),
 ]),
 dict(h='Service', kind='table', rows=[
  ('2022 – 2024','Student Representative, University and College Affairs Meetings, University of Taipei'),
  ('2022 – 2024','President (16th and 17th terms), Social and Public Affairs Student Association; Student Representative, Department Affairs Meeting'),
  ('2022 – 2023','Member, Student Appeals Review Committee, University of Taipei'),
  ('2022','Director of Cultural Affairs (9th term), University of Taipei Student Association'),
  ('2022','Chair (8th term), Election and Recall Affairs Committee, Student Association'),
 ]),
 dict(h='Skills', kind='table', rows=[
  ('Methods','Deliberative analysis, qualitative content analysis, comparative institutional analysis, cross-national case studies, survey research, quantitative text analysis, focus groups, tabletop exercise design'),
  ('Software','R, SPSS'),
 ]),
 dict(h='Advisors and Supervisors', kind='faculty', rows=[
  ('Prof. Tze-Luen Lin','<i>Advisor.</i> Department of Political Science; Director, Center for Public Policy and Law, National Taiwan University'),
  ('Prof. Kuo-Hui Chang','<i>Co-advisor.</i> Director, Graduate Institute of National Development, National Taiwan University'),
  ('Assoc. Prof. Tien-Shen Li','<i>Research supervisor.</i> Department of Public Affairs; Director, General Education Center, University of Taipei'),
  ('Adjunct Asst. Prof. Hui-Chen Tseng','<i>Research supervisor.</i> Department of Business Administration, Chung Yuan Christian University'),
  ('Assoc. Prof. Tzu-Ping Liu','<i>Center director.</i> Department of Public Affairs; Director, Public Opinion and Policy Research Center, University of Taipei'),
 ]),
])

ZH = dict(name='陳佑丞',
 affil='國立臺灣大學 國家發展研究所 碩士班 <span class="sep">⋄</span> Yu-Cheng (Kane) Chen',
 sections=[
 dict(h='簡介', kind='intro', ps=[
  '我是國立臺灣大學國家發展研究所碩士生，關心公共制度如何治理新興科技，以及公民如何參與這些決策。我的碩士論文預計從審議民主的角度出發，分析經抽樣選出的一般民眾在公民審議中，如何思辨次世代定序時代產前與新生兒基因檢測所牽動的倫理與治理問題。',
  '論文之外，我也研究國家透過哪些組織形式行動。國科會計畫比較行政法人與政府捐助財團法人的制度變遷與爭議生成；職災預防及重建中心轉型評估、國家中醫研究院人事薪資制度建構兩項委託研究，則讓我從實務端理解這類組織如何被設計。此外，我參與地緣政治下能源安全與區域合作的國科會研究，並以計量文本分析比較日本與韓國國會如何討論氣候「損失與損害」。']),
 dict(h='學歷', kind='entries', items=[
  dict(org='國立臺灣大學　國家發展研究所　碩士班', right='2025.09 – 迄今', sub='學期 GPA 4.00–4.10／4.3<br>碩士論文（預計）：知與不知的權利：次世代定序時代產前與新生兒基因檢測的公民審議經驗<br>指導教授：林子倫 教授；共同指導教授：張國暉 教授'),
  dict(org='臺北市立大學　社會暨公共事務學系　公共事務碩士班（預研生）', right='2024.09 – 2025.06'),
  dict(org='暨南大學（中國廣州）　國際政治　交換學生', right='2024.08 – 2025.01'),
  dict(org='臺北市立大學　社會暨公共事務學系　學士', right='2021.09 – 2025.06', sub='學期 GPA 4.00–4.18／4.3'),
 ]),
  dict(h='研究經歷', kind='entries', items=[
  dict(org='國立臺灣大學', right='臺北', roles=[dict(t='碩士生兼任研究助理（林子倫 教授）', d='2026.01 – 迄今', b=[
   '國科會計畫「地緣政治下的能源安全、關鍵能資源風險及區域合作策略之研析」。',
   '臺大醫院與臺灣大學合作計畫「探索次世代定序時代產前和新生兒基因檢測的父母決策和倫理問題」（2026.02 起）。'])]),
  dict(org='臺北市立大學', right='臺北', roles=[dict(t='碩士生兼任研究助理（李天申 副教授）', d='2026.09 – 迄今', b=[
   '國科會計畫「制度節點與爭議的生成邏輯：準政府組織制度變遷過程的比較分析－以行政法人與政府捐助之財團法人為例」（2026.10 起）。',
   '「行政法人國家中醫研究院人事及薪資建構委託辦理計畫」（2026.10 起）。'])]),
  dict(org='台灣職業衛生學會', right='臺北', roles=[dict(t='研究助理（曾慧珍 兼任助理教授，中原大學企業管理學系）', d='2026.01 – 迄今', b=[
   '「115 年度職災勞工傷病診治及重建復工服務精進計畫－職災預防及重建中心轉型為行政法人之可行性評估」。'])]),
  dict(org='臺北市立大學', right='臺北', roles=[
   dict(t='大學生兼任研究助理（李天申 副教授）', d='2023.09 – 2024.07', b=[
    '「臺北市立聯合醫院經營體制轉型方案探討規劃案」（2023.12 – 2024.07）。',
    '112 年度 USR Hub 計畫「都市再生總體計畫：在地參與的社區活化實驗」（2023.09 – 2023.12）。']),
   dict(t='民意與政策研究中心　兼任行政助理及督導（中心主任：劉自平 副教授）', d='2022.09 – 2023.08', b=[
    '參與勞動部勞動力發展署協助受疫情影響企業及勞工之紓困措施成效分析、衛生福利部中央健康保險署公共服務滿意度調查，以及人工智慧決策過程中的知識移轉與人為因素研究。']),
   dict(t='民意與政策研究中心　電話訪員', d='2021.09 – 2022.08')]),
 ]),
 dict(h='實習經歷', kind='entries', items=[
  dict(org='臺北市政府民政局', right='2024.02 – 2024.06', roles=[dict(t='公共事務實習', b=[
   '調查分析臺北市戶政事務所便民服務措施與服務人員之情緒勞務，以文山區、大同區戶政事務所為研究對象。'])]),
  dict(org='環境法律人協會', right='2023.07 – 2023.12', roles=[dict(t='公共事務實習', b=[
   '研究臺北市山坡地開發與建築管制區域之演變，以及山坡地住宅開發與都市更新、危老重建之關係。'])]),
 ]),
 dict(h='公共服務', kind='table', rows=[
  ('2022 – 2024','臺北市立大學校務會議學生代表'),
  ('2022 – 2024','臺北市立大學人文藝術學院院務會議學生代表'),
  ('2022 – 2024','社會暨公共事務學系系學會第 16、17 屆會長；系務會議學生代表'),
  ('2022 – 2023','臺北市立大學學生申訴評議委員會委員'),
  ('2022','臺北市立大學學生會第 9 屆文化部部長'),
  ('2022','臺北市立大學學生會第 8 屆選舉及罷免事務委員會主任委員'),
 ]),
 dict(h='技能', kind='table', rows=[
  ('研究方法','審議民主分析、質性內容分析、比較制度分析、跨國個案研究、調查研究、計量文本分析、焦點團體座談、桌上推演設計'),
  ('統計軟體','R、SPSS'),
 ]),
 dict(h='相關師長', kind='table', rows=[
  ('林子倫 教授','指導教授｜國立臺灣大學政治學系、公共事務研究所暨國際政治經濟學院專任教授，兼公共政策與法律研究中心主任'),
  ('張國暉 教授','共同指導教授｜國立臺灣大學國家發展研究所專任教授兼所長'),
  ('李天申 副教授','計畫主持人｜臺北市立大學公共事務學系專任副教授兼通識教育中心主任'),
  ('曾慧珍 兼任助理教授','計畫主持人｜中原大學企業管理學系兼任助理教授'),
  ('劉自平 副教授','中心主任｜臺北市立大學公共事務學系專任副教授兼民意與政策研究中心主任'),
 ]),
])

HEAD_EN = '<div style="width:100%;text-align:right;padding-right:17mm;font-family:\'Latin Modern Roman\';font-size:7.5pt;color:#555;font-style:italic;">For reference only &middot; Comparative Legislative Politics in East Asia (Fall 2026), Graduate Institute of National Development, National Taiwan University</div>'
HEAD_ZH = '<div style="width:100%;text-align:right;padding-right:17mm;font-family:\'Noto Serif CJK TC\';font-size:7.5pt;color:#555;">僅供參考｜國立臺灣大學國家發展研究所 115-1「東亞比較立法政治專題」課程使用</div>'
FOOT_EN = '<div style="width:100%;text-align:center;font-family:\'Latin Modern Roman\';font-size:7.5pt;color:#555;line-height:1.35;">For reference only in the course <i>Comparative Legislative Politics in East Asia</i> (Fall 2026), Graduate Institute of National Development, National Taiwan University.<br><span style="font-size:9pt;color:#000">Last updated: November 12, 2026 &middot; Page <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>'
FOOT_ZH = '<div style="width:100%;text-align:center;font-family:\'Noto Serif CJK TC\';font-size:7.5pt;color:#555;line-height:1.4;">本履歷目前僅供國立臺灣大學國家發展研究所 115-1「東亞比較立法政治專題」（Comparative Legislative Politics in East Asia）課程參考使用。<br><span style="font-size:9pt;color:#000">最後更新：2026.11.12・第 <span class="pageNumber"></span> 頁，共 <span class="totalPages"></span> 頁</span></div>'

out = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, d, foot, fn, head in [('en',EN,FOOT_EN,'CV_YuChengChen_en.pdf',HEAD_EN),('zh',ZH,FOOT_ZH,'CV_陳佑丞_zh.pdf',HEAD_ZH)]:
        h = build(d, lang)
        open(f'/tmp/cv/{lang}.html','w',encoding='utf-8').write(h)
        pg = b.new_page()
        pg.goto(f'file:///tmp/cv/{lang}.html'); pg.wait_for_timeout(500)
        pg.pdf(path=f'{out}/{fn}', format='A4', display_header_footer=True, header_template=head, footer_template=foot,
               margin=dict(top='15mm',bottom='19mm',left='17mm',right='17mm'), print_background=True)
    b.close()
