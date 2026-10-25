# Layout, helpers, components dùng chung
import os, json, html, math
from data import *
OUT = None
E = html.escape
PAGES = []
ICON = {'search':'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>','heart':'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
'pin':'<path d="M12 22s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="10" r="2.5"/>','img':'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="m21 16-5-5-8 8"/>',
'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
'chev':'<path d="m9 18 6-6-6-6"/>','chevl':'<path d="m15 18-6-6 6-6"/>','down':'<path d="m6 9 6 6 6-6"/>','menu':'<path d="M3 6h18M3 12h18M3 18h18"/>','x':'<path d="M18 6 6 18M6 6l12 12"/>','check':'<path d="M20 6 9 17l-5-5"/>',
'share':'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>','user':'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
'map':'<path d="m9 4-6 2v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>','mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
'home':'<path d="m3 11 9-8 9 8v10H3z"/>','play':'<path d="M8 5v14l11-7z" fill="currentColor"/>','bed':'<path d="M2 18V6M2 12h20v6M22 18v-4a3 3 0 0 0-3-3H10v7"/><circle cx="6" cy="10" r="2"/>',
'bath':'<path d="M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM6 12V5a2 2 0 0 1 4 0"/>','chart':'<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>','doc':'<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
'building':'<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>','zalo':'<path d="M4 5h16v11H9l-5 4z"/>','calc':'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M8 15h2M12 15h2M8 18h2M12 18h2"/>',
'compass':'<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>'}
def ic(n, cls='ic'): return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'
def money(p, mode):
    if mode == 'thue':
        return (f"{p/1e6:.1f}".rstrip('0').rstrip('.').replace('.',',') + ' triệu/tháng') if p >= 1e6 else f"{int(p/1e3)} nghìn/tháng"
    return (f"{p/1e9:.2f}".rstrip('0').rstrip('.').replace('.',',') + ' tỷ') if p >= 1e9 else f"{int(p/1e6)} triệu"
def ppm(l): return (f"{l['price']/l['area']/1e6:.1f}".replace('.',',') + ' tr/m²') if l['mode']=='ban' else ''
def ago(d): return 'Đăng hôm nay' if d==0 else ('Đăng hôm qua' if d==1 else f'Đăng {d} ngày trước')
def img(n, R): return f"{R}img/r{n}.jpg"
def phone_of(l): return f"09{(l['id']*7919)%100000000:08d}"

def lurl(mode, ts=None, city=None, dist=None, page=1):
    base = (('ban-' if mode=='ban' else 'cho-thue-') + ts) if ts else ('nha-dat-ban' if mode=='ban' else 'nha-dat-cho-thue')
    if dist: base += '-' + dslug(dist, city)
    elif city: base += '-' + CITIES[city][0]
    return base + (f'-p{page}' if page > 1 else '') + '.html'
def detail_url(l): return f"tin/{l['id']}.html"
TYPES = {'ban':BAN, 'thue':THUE}
def tname(mode, ts): return dict((a,b) for a,b,_ in TYPES[mode])[ts]
LOGO = '<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="8" fill="#E03C31"/><path d="M8 18 17 10l9 8v8h-6v-5h-6v5H8z" fill="#fff"/></svg><span><b>NhàĐất Việt</b><small>Nền tảng BĐS (demo)</small></span>'

def header(R, active=''):
    def dd(key, label, href, items):
        li = ''.join(f'<li><a href="{R}{h}">{E(t)}{" <span class=new>Mới</span>" if n else ""}</a></li>' for t,h,n in items)
        on = ' on' if active==key else ''
        return f'<li class="nv{on}"><a class="nv-a" href="{R}{href}">{label}</a><button class="nv-t" aria-expanded="false" aria-label="Mở menu con {label}">{ic("down")}</button><ul class="dd">{li}</ul></li>'
    ban = [('Bán '+t, lurl('ban',s), s=='can-ho-chung-cu-mini') for s,t,_ in BAN]
    thue = [('Cho thuê '+t, lurl('thue',s), False) for s,t,_ in THUE]
    duan = [(t, f'du-an-{s}.html', False) for s,t in PROJ_TYPES]
    wiki = [(t, f'wiki/{s}.html', False) for s,t in WIKI_CATS]
    pt = [('Biểu đồ giá','bieu-do-gia.html',False),('Video đánh giá','video-danh-gia.html',False),('Báo cáo thị trường','bao-cao-thi-truong.html',False),('Góc nhìn chuyên gia','goc-nhin-chuyen-gia.html',False)]
    db = [('Nhà môi giới','nha-moi-gioi.html',False),('Doanh nghiệp','doanh-nghiep.html',False)]
    tt = [('Tin tức bất động sản','tin-tuc.html',False),('Bất động sản Hà Nội','tin-tuc-ha-noi.html',False),('Bất động sản TP.HCM','tin-tuc-tp-hcm.html',False)]
    nav = dd('ban','Nhà đất bán','nha-dat-ban.html',ban)+dd('thue','Nhà đất cho thuê','nha-dat-cho-thue.html',thue)+dd('duan','Dự án','du-an.html',duan)+dd('tin','Tin tức','tin-tuc.html',tt)+dd('wiki','Wiki BĐS','wiki.html',wiki)+dd('pt','Phân tích đánh giá','phan-tich-danh-gia.html',pt)+dd('db','Danh bạ','nha-moi-gioi.html',db)
    return f'''<a class="skip" href="#main">Bỏ qua đến nội dung</a>
<div class="appbar" id="appbar"><button class="ab-x" aria-label="Đóng" data-close-appbar>{ic('x')}</button><span class="ab-logo" aria-hidden="true">NĐ</span><span><b>Mở App để xem đầy đủ</b><br><small>So sánh giá dễ dàng</small></span><a class="btn btn-sm" href="{R}gioi-thieu.html#app">Mở App</a></div>
<header class="hdr"><div class="hdr-in">
<a class="logo" href="{R}index.html" aria-label="NhàĐất Việt – Trang chủ">{LOGO}</a>
<nav aria-label="Menu chính" class="nav-wrap" id="navWrap"><ul class="nav" id="nav">{nav}<li class="nv nv-mob"><a class="nv-a" href="{R}dang-nhap.html" data-auth="login">Đăng nhập</a></li><li class="nv nv-mob"><a class="nv-a" href="{R}dang-ky.html" data-auth="register">Đăng ký</a></li><li class="nv nv-mob"><a class="nv-a" href="{R}dang-tin.html">Đăng tin</a></li></ul></nav>
<div class="hdr-r"><a class="hbtn hide-m" href="{R}gioi-thieu.html#app">Tải ứng dụng</a><a class="hbtn" href="{R}tin-da-luu.html" aria-label="Tin đã lưu">{ic('heart')}<span class="cnt" id="favCount" hidden>0</span></a>
<span class="acct hide-m" id="acct"><a class="hbtn" href="{R}dang-nhap.html" data-auth="login">Đăng nhập</a><a class="hbtn" href="{R}dang-ky.html" data-auth="register">Đăng ký</a></span>
<a class="btn btn-post hide-m" href="{R}dang-tin.html">Đăng tin</a><button class="hbtn menu-btn" aria-label="Mở menu" aria-expanded="false" aria-controls="navWrap" data-menu>{ic('menu')}</button></div></div></header>'''

def footer(R, seo=''):
    cols = [('Hướng dẫn',[('Báo giá & hỗ trợ','bang-gia-dich-vu.html'),('Câu hỏi thường gặp','hoi-dap.html'),('Góp ý báo lỗi','lien-he.html'),('Sơ đồ trang','sitemap.html')]),
            ('Quy định',[('Quy định đăng tin','quy-che-hoat-dong.html#dang-tin'),('Quy chế hoạt động','quy-che-hoat-dong.html'),('Điều khoản thỏa thuận','dieu-khoan-thoa-thuan.html'),('Chính sách bảo mật','dieu-khoan-thoa-thuan.html#bao-mat'),('Giải quyết khiếu nại','quy-che-hoat-dong.html#khieu-nai')]),
            ('Về NhàĐất Việt',[('Giới thiệu','gioi-thieu.html'),('Liên hệ','lien-he.html'),('Tin tức','tin-tuc.html'),('Wiki BĐS','wiki.html'),('Nguồn ảnh','nguon-anh.html')])]
    c = ''.join(f'<div><h3>{h}</h3><ul>' + ''.join(f'<li><a href="{R}{u}">{t}</a></li>' for t,u in l) + '</ul></div>' for h,l in cols)
    return f'''{seo}<footer class="ftr"><div class="container ftr-top"><div class="ftr-brand"><a class="logo" href="{R}index.html">{LOGO}</a>
<p>Website demo mô phỏng cấu trúc một sàn giao dịch BĐS trực tuyến. Mọi tin đăng, dự án, môi giới, doanh nghiệp và số liệu đều là <strong>dữ liệu mẫu</strong>.</p>
<p class="fc">{ic('phone')} Hotline (demo): 1900 0000</p><p class="fc">{ic('mail')} hotro@nhadatviet.demo</p></div>{c}
<form class="nl" data-demo-form="Đã đăng ký nhận bản tin (demo)"><h3>Đăng ký nhận tin</h3><label class="sr" for="nlmail">Email</label><input id="nlmail" type="email" required placeholder="Nhập email của bạn" autocomplete="email"><button class="btn btn-red">Gửi</button></form></div>
<div class="ftr-b container">© 2026 NhàĐất Việt – sản phẩm demo, không liên kết với Batdongsan.com.vn hay bất kỳ sàn BĐS nào. Ảnh: Wikimedia Commons (xem <a href="{R}nguon-anh.html">nguồn ảnh</a>).</div></footer>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>window.ROOT="{R}"</script><script src="{R}js/app.js" defer></script>'''

def page(path, title, body, active='', desc='', seo='', extra_head='', body_cls=''):
    depth = path.count('/'); R = '../' * depth
    doc = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | NhàĐất Việt</title>
<meta name="description" content="{E(desc or title)}"><link rel="icon" href="{R}img/favicon.svg"><link rel="stylesheet" href="{R}css/style.css">{extra_head}</head><body class="{body_cls}">
{header(R, active)}<main id="main">{body(R) if callable(body) else body}</main>{footer(R, seo(R) if callable(seo) else seo)}</body></html>'''
    fp = os.path.join(OUT, path); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(doc); PAGES.append(path)

def crumbs(R, items):
    li = ''.join(f'<li><a href="{R}{u}">{E(t)}</a></li>' if u else f'<li aria-current="page">{E(t)}</li>' for t,u in items)
    return f'<nav class="bc" aria-label="Breadcrumb"><ol>{li}</ol></nav>'

VIPL = {'kimcuong':'VIP Kim Cương','vang':'VIP Vàng','bac':'VIP Bạc'}
def card(l, R):
    return f'''<article class="pc"><a href="{R}{detail_url(l)}" class="th"><img src="{img(l['img'][0],R)}" alt="{E(l['title'])}" loading="lazy" width="400" height="300"><span class="cnt-img">{ic('img')}{6+l['id']%9}</span></a>
<div class="pc-b"><h3><a href="{R}{detail_url(l)}">{E(l['title'])}</a></h3><p class="pr"><b>{money(l['price'],l['mode'])}</b> · <b>{l['area']} m²</b></p><p class="loc">{ic('pin')}{E(l['dist'])}, {E(l['city'])}</p>
<div class="pc-f"><span>{ago(l['day'])}</span><button class="heart" data-fav="{l['id']}" aria-pressed="false" aria-label="Lưu tin">{ic('heart')}</button></div></div></article>'''
def row(l, R):
    big = l['vip'] in ('kimcuong','vang')
    imgs = ''.join(f'<img src="{img(n,R)}" alt="" loading="lazy" width="300" height="225">' for n in l['img'][1:4]) if big else ''
    a = AGENTS[l['agent']]; ph = phone_of(l)
    feats = (f'<span class="ft">{l["beds"]} {ic("bed")}</span><span class="ft">{l["baths"]} {ic("bath")}</span>') if l['beds'] else ''
    vip = f'<span class="vip v-{l["vip"]}">{VIPL[l["vip"]]}</span>' if l['vip'] in VIPL else ''
    ver = f'<span class="ver">{ic("check")}Xác thực</span> ' if l['verified'] else ''
    return f'''<article class="lr{' lr-big' if big else ''}" data-price="{int(l['price'])}" data-area="{l['area']}" data-day="{l['day']}" data-ver="{1 if l['verified'] else 0}" data-mode="{l['mode']}"><a class="lr-media" href="{R}{detail_url(l)}" tabindex="-1" aria-hidden="true">{vip}<img class="lr-main" src="{img(l['img'][0],R)}" alt="" loading="lazy" width="600" height="450"><span class="lr-sub">{imgs}</span><span class="cnt-img">{ic('img')}{6+l['id']%9}</span></a>
<div class="lr-b"><h3><a href="{R}{detail_url(l)}">{ver}{E(l['title'])}</a></h3>
<p class="pr"><b>{money(l['price'],l['mode'])}</b> · <b>{l['area']} m²</b>{' · <span class=muted>'+ppm(l)+'</span>' if l['mode']=='ban' else ''} {feats}<span class="loc">{ic('pin')}{E(l['dist'])}, {E(l['city'])}</span></p>
<p class="desc">{E(l['title'])}. Vị trí gần đường {E(l['street'])}, {E(l['dist'])}, thuận tiện di chuyển. Diện tích {l['area']} m², hướng {l['dir']}, pháp lý: {E(l['legal'].lower())}, nội thất {l['furn'].lower()}.</p>
<div class="lr-f"><span class="ag"><span class="av" aria-hidden="true">{a.split()[-1][0]}</span><span>{E(a)}<br><small>{ago(l['day'])}</small></span></span><span class="lr-act"><button class="btn btn-teal btn-sm" data-phone="{ph}">{ic('phone')}<span>{ph[:7]} *** · Hiện số</span></button><button class="heart" data-fav="{l['id']}" aria-pressed="false" aria-label="Lưu tin">{ic('heart')}</button></span></div></div></article>'''
def pcard(p, R):
    return f'''<article class="pj"><a href="{R}du-an/{p['slug']}.html" class="th"><img src="{img(p['img'][0],R)}" alt="{E(p['name'])}" loading="lazy" width="400" height="300"><span class="st st-{p['id']%3}">{p['status']}</span></a>
<div class="pc-b"><h3><a href="{R}du-an/{p['slug']}.html">{E(p['name'])}</a></h3><p class="pr">{p['price']} triệu/m² · {p['ha']} ha</p><p class="loc">{ic('pin')}{E(p['dist'])}, {E(p['city'])}</p></div></article>'''
def ncard(n, R, big=False):
    return f'<article class="nc{" nc-big" if big else ""}"><a href="{R}tin-tuc/{n["slug"]}.html" class="th" tabindex="-1" aria-hidden="true"><img src="{img(n["img"],R)}" alt="" loading="lazy" width="400" height="260"></a><div><p class="meta">{n["date"]} · {E(n["cat"])}</p><h3><a href="{R}tin-tuc/{n["slug"]}.html">{E(n["t"])}</a></h3></div></article>'
def pager(R, cur, total, fn):
    if total <= 1: return ''
    s = '<nav class="pg" aria-label="Phân trang">'
    if cur > 1: s += f'<a href="{R}{fn(cur-1)}" aria-label="Trang trước">{ic("chevl")}</a>'
    for i in range(1, total+1): s += f'<a href="{R}{fn(i)}"{" aria-current=page class=on" if i==cur else ""}>{i}</a>'
    if cur < total: s += f'<a href="{R}{fn(cur+1)}" aria-label="Trang sau">{ic("chev")}</a>'
    return s + '</nav>'
def para(seed, topic, n=5):
    import random as _r; r = _r.Random(seed)
    S = [f"{topic} đang nhận được nhiều sự quan tâm từ người mua ở thực lẫn nhà đầu tư trong năm 2026.","Theo dữ liệu mẫu của NhàĐất Việt, lượng tin đăng tăng khoảng {0}% so với cùng kỳ, trong khi mặt bằng giá chào bán đi ngang hoặc tăng nhẹ.".format(r.randint(4,18)),
         "Người mua nên kiểm tra kỹ pháp lý, tiến độ và uy tín chủ đầu tư hoặc chủ nhà trước khi đặt cọc.","Hạ tầng giao thông như các tuyến vành đai, metro và cầu mới là động lực chính giúp khu vực ven trung tâm thu hút cư dân.",
         "Các chuyên gia khuyến nghị dùng đòn bẩy tài chính ở mức an toàn, tổng khoản trả nợ hàng tháng không nên vượt quá 40% thu nhập.","Ở phân khúc cho thuê, nhu cầu tập trung vào căn hộ 1–2 phòng ngủ gần khu văn phòng, trường đại học và khu công nghiệp.",
         "Nguồn cung mới chủ yếu đến từ các dự án quy mô lớn ở khu vực phía Đông và phía Tây của đô thị.","Khoảng chênh giữa giá chào bán và giá giao dịch thực tế thường dao động 5–10%, người mua có thể thương lượng.",
         "Bên cạnh giá, các yếu tố như tiện ích nội khu, chất lượng quản lý vận hành và cộng đồng cư dân ngày càng được coi trọng.","Thị trường được dự báo phân hóa: sản phẩm có pháp lý rõ ràng, giá hợp lý sẽ hấp thụ tốt, còn sản phẩm đầu cơ sẽ chậm thanh khoản."]
    r.shuffle(S); return ''.join(f'<p>{x}</p>' for x in [' '.join(S[i:i+2]) for i in range(0, min(n,5)*2, 2)])
def has(mode, ts, d): return any(l for l in LISTINGS if l['mode']==mode and (ts is None or l['ts']==ts) and l['dist']==d)
def seo_block(R, mode, ts):
    t = tname(mode, ts) if ts else 'nhà đất'; verb = 'Mua bán' if mode=='ban' else 'Cho thuê'
    cities = ''.join(f'<li><a href="{R}{lurl(mode,ts,c)}">{verb} {t} {c}</a></li>' for c in CITIES)
    dists = ''.join(f'<li><a href="{R}{lurl(mode,ts,c,d)}">{verb} {t} {d}</a></li>' for c in ('Hà Nội','TP.HCM') for d in CITIES[c][3] if has(mode,ts,d))
    other = ''.join(f'<li><a href="{R}{lurl(mode,s)}">{"Bán" if mode=="ban" else "Cho thuê"} {n}</a></li>' for s,n,_ in TYPES[mode])
    return f'<section class="seo" aria-label="Liên kết theo khu vực"><div class="container seo-in"><div><h2>{verb} {t} theo tỉnh thành</h2><ul>{cities}</ul></div><div><h2>{verb} {t} theo quận huyện</h2><ul>{dists}</ul></div><div><h2>{verb} theo loại hình</h2><ul>{other}</ul></div></div></section>'
