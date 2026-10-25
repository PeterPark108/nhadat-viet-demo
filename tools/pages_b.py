# Phân tích, danh bạ, trang tĩnh, trang chủ, sitemap, data.js
import json, random as _rnd
from core import *
import core

def series(key, months=24, base=None):
    r = _rnd.Random(key); b = base or {"Hà Nội":62,"TP.HCM":68,"Đà Nẵng":38,"Hải Phòng":32,"Bình Dương":28,"Khánh Hòa":36,"Đồng Nai":24,"Quảng Ninh":27}.get(key, 40)
    v=[]; x=b
    for i in range(months): x *= 1 + r.uniform(-.012, .028); v.append(round(x,1))
    return v
MONTHS = [f"T{(9+i)%12+1}/{2024+(9+i)//12}" for i in range(24)]
COLORS = ('#C4321F','#00807F','#6941C6','#B54708')
def chart(vals_list, names, h=280, unit='tr/m²', labels=MONTHS):
    W=720; P=48; mn=min(min(v) for v in vals_list)*.95; mx=max(max(v) for v in vals_list)*1.03
    X=lambda i: P + i*(W-P-16)/(len(labels)-1); Y=lambda v: h-32 - (v-mn)/(mx-mn)*(h-60)
    g=''.join(f'<line x1="{P}" x2="{W-16}" y1="{Y(mn+(mx-mn)*k/4):.1f}" y2="{Y(mn+(mx-mn)*k/4):.1f}" stroke="#EEE"/><text x="{P-6}" y="{Y(mn+(mx-mn)*k/4)+4:.1f}" text-anchor="end" font-size="11" fill="#555">{mn+(mx-mn)*k/4:.0f}</text>' for k in range(5))
    g+=''.join(f'<text x="{X(i):.1f}" y="{h-10}" text-anchor="middle" font-size="11" fill="#555">{labels[i]}</text>' for i in range(0,len(labels),4))
    lines=''
    for j,vals in enumerate(vals_list):
        lines += f'<polyline fill="none" stroke="{COLORS[j]}" stroke-width="2.5" points="{" ".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(vals))}"/>'
        lines += ''.join(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="8" fill="transparent" data-tip="{E(names[j])} · {labels[i]}: {v} {unit}"/>' for i,v in enumerate(vals))
    leg=''.join(f'<span><i style="background:{COLORS[j]}"></i>{E(n)}</span>' for j,n in enumerate(names))
    return f'<figure class="chart"><svg viewBox="0 0 {W} {h}" role="img" aria-label="Biểu đồ giá: {E(", ".join(names))}">{g}{lines}</svg><figcaption class="legend">{leg}<small>Đơn vị: {unit} · số liệu mẫu</small></figcaption><div class="tip" hidden></div></figure>'
def anav(R, cur): return '<nav class="subnav" aria-label="Phân tích đánh giá"><div class="container">' + ''.join(f'<a href="{R}{u}"{" class=on" if u==cur else ""}>{t}</a>' for t,u in [('Phân tích đánh giá','phan-tich-danh-gia.html'),('Biểu đồ giá','bieu-do-gia.html'),('Video đánh giá','video-danh-gia.html'),('Báo cáo thị trường','bao-cao-thi-truong.html'),('Góc nhìn chuyên gia','goc-nhin-chuyen-gia.html')]) + '</div></nav>'
def rcard(r, R): return f'<article class="nc"><a class="th" href="{R}phan-tich/{r["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="{img(r["img"],R)}" alt="" loading="lazy" width="400" height="260"></a><div><p class="meta">{"Biểu đồ giá" if r["kind"]=="bieu-do-gia" else "Góc nhìn chuyên gia"}</p><h3><a href="{R}phan-tich/{r["slug"]}.html">{E(r["t"])}</a></h3></div></article>'
def vcard(v, R): return f'<article class="vc"><button type="button" class="th" data-video="{E(v["t"])}" aria-label="Xem video: {E(v["t"])}"><img src="{img(v["img"],R)}" alt="" loading="lazy" width="400" height="260"><span class="play">{ic("play")}</span><span class="dur">{v["dur"]}</span></button><h3>{E(v["t"])}</h3></article>'
def rep_url(c): return 'phan-tich/' + slug(f'Biến động giá bất động sản {c} 24 tháng qua') + '.html'
def analytics_pages():
    top = list(CITIES)[:4]
    def home_(R):
        bd = ''.join(rcard(r,R) for r in REPORTS if r['kind']=='bieu-do-gia'); gn = ''.join(rcard(r,R) for r in REPORTS if r['kind']!='bieu-do-gia')
        return anav(R,'phan-tich-danh-gia.html') + f'<div class="container"><div class="hero-s"><h1>Phân tích đánh giá</h1><p>Biểu đồ giá, báo cáo và góc nhìn về thị trường (số liệu mẫu).</p></div><section><h2>Giá chào bán căn hộ trung bình 24 tháng</h2>{chart([series(c) for c in top], top)}</section><section><div class="sec-h"><h2>Biểu đồ giá theo khu vực</h2><a href="{R}bieu-do-gia.html">Xem thêm {ic("chev")}</a></div><div class="grid4">{bd}</div></section><section><div class="sec-h"><h2>Video đánh giá</h2><a href="{R}video-danh-gia.html">Xem thêm {ic("chev")}</a></div><div class="grid4">{"".join(vcard(v,R) for v in VIDEOS[:4])}</div></section><section><h2>Góc nhìn chuyên gia</h2><div class="grid3">{gn}</div></section></div>'
    page('phan-tich-danh-gia.html', 'Phân tích, đánh giá thị trường BĐS', home_, 'pt')
    def bdg(R):
        opts = ''.join(f'<option{" selected" if c=="TP.HCM" else ""}>{c}</option>' for c in CITIES)
        return anav(R,'bieu-do-gia.html') + f'<div class="container"><div class="hero-s"><h1>Biểu đồ giá bất động sản</h1><p>Lịch sử giá chào bán theo từng thị trường dựa trên dữ liệu mẫu.</p></div><div class="ctl"><label>Tỉnh thành 1 <select data-cmp="0">{opts.replace(" selected","").replace("<option>Hà Nội","<option selected>Hà Nội")}</select></label><label>Tỉnh thành 2 <select data-cmp="1">{opts}</select></label></div><div id="cmpChart">{chart([series("Hà Nội"), series("TP.HCM")], ["Hà Nội","TP.HCM"])}</div><script type="application/json" id="seriesData">{json.dumps({"labels":MONTHS,"s":{c:series(c) for c in CITIES}}, ensure_ascii=False)}</script><h2>Biểu đồ giá theo tỉnh thành</h2><div class="grid4">{"".join(rcard(r,R) for r in REPORTS if r["kind"]=="bieu-do-gia")}</div></div>'
    page('bieu-do-gia.html', 'Biểu đồ giá bất động sản theo khu vực', bdg, 'pt')
    page('video-danh-gia.html', 'Video đánh giá khu vực, dự án', lambda R: anav(R,'video-danh-gia.html') + f'<div class="container"><div class="hero-s"><h1>Video đánh giá</h1><p>Ảnh bìa minh họa; bản demo chưa có video thật.</p></div><div class="grid4">{"".join(vcard(v,R) for v in VIDEOS)}</div></div>', 'pt')
    def bc(R):
        rows = ''
        for c in CITIES:
            s = series(c)
            rows += f'<article class="rep"><span class="rep-ic">{ic("doc")}</span><div><h2>Báo cáo thị trường BĐS {c} quý 3/2026</h2><p class="muted">Giá trung bình {s[-1]} tr/m² · biến động 12 tháng {round((s[-1]/s[-13]-1)*100,1)}%</p></div><a class="btn btn-sm" href="{R}{rep_url(c)}">Xem</a></article>'
        return anav(R,'bao-cao-thi-truong.html') + f'<div class="container"><div class="hero-s"><h1>Báo cáo thị trường</h1><p>Báo cáo quý (mẫu).</p></div><div class="rep-list">{rows}</div></div>'
    page('bao-cao-thi-truong.html', 'Báo cáo thị trường', bc, 'pt')
    page('goc-nhin-chuyen-gia.html', 'Góc nhìn chuyên gia', lambda R: anav(R,'goc-nhin-chuyen-gia.html') + f'<div class="container"><div class="hero-s"><h1>Góc nhìn chuyên gia</h1></div><div class="grid3">{"".join(rcard(r,R) for r in REPORTS if r["kind"]!="bieu-do-gia")}</div></div>', 'pt')
    for r in REPORTS:
        def body(R, r=r):
            c = r['city']; s = series(c); dists = CITIES[c][3][:4]
            ser = [series(c+d, base=s[0]*_rnd.Random(d).uniform(.7,1.4)) for d in dists]
            tbl = ''.join(f'<tr><th scope="row"><a href="{R}{lurl("ban","can-ho-chung-cu",c,d) if has("ban","can-ho-chung-cu",d) else lurl("ban",None,c)}">{d}</a></th><td>{v[-1]}</td><td>{round((v[-1]/v[-13]-1)*100,1)}%</td></tr>' for d,v in zip(dists,ser))
            others = ''.join(rcard(x,R) for x in [x for x in REPORTS if x['kind']==r['kind'] and x is not r][:4])
            return anav(R, 'bieu-do-gia.html' if r['kind']=='bieu-do-gia' else 'goc-nhin-chuyen-gia.html') + f'''<div class="container art-wrap"><article class="art">{crumbs(R,[('Phân tích đánh giá','phan-tich-danh-gia.html'),(r['t'],None)])}<h1>{E(r['t'])}</h1><p class="meta">Cập nhật 10/2026 · Số liệu mẫu</p>
{chart(ser, dists)}<h2>Giá theo quận/huyện</h2><div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Khu vực</th><th scope="col">Giá TB (tr/m²)</th><th scope="col">Biến động 12 tháng</th></tr></thead><tbody>{tbl}</tbody></table></div>
<h2>Nhận định</h2>{para(len(r['t']), 'Thị trường '+c, 4)}<p class="note">Số liệu và biểu đồ là dữ liệu mẫu do NhàĐất Việt sinh ra, không phải số liệu thật.</p></article><aside class="art-side"><h2>Bài khác</h2>{others}</aside></div>'''
        page(f"phan-tich/{r['slug']}.html", r['t'], body, 'pt')

def initials(n): return ''.join(w[0] for w in n.split()[-2:])
def directory_pages():
    def tabs(R, cur): return f'<div class="seg"><a href="{R}doanh-nghiep.html"{" aria-current=page" if cur=="dn" else ""}>Doanh nghiệp</a><a href="{R}nha-moi-gioi.html"{" aria-current=page" if cur=="mg" else ""}>Cá nhân môi giới</a></div>'
    def sform(R): return f'<form class="dsearch" data-dir-filter onsubmit="return false"><b>TÌM KIẾM</b><label class="sr" for="dq">Từ khóa</label><input id="dq" placeholder="Nhập tên, khu vực"><label class="sr" for="dc">Tỉnh thành</label><select id="dc"><option value="">Tỉnh/Thành phố</option>{"".join(f"<option>{c}</option>" for c in CITIES)}</select></form>'
    def area_links(R, city):
        return ''.join(f'<li><a href="{R}{lurl(m,ts,city)}">{"Bán" if m=="ban" else "Cho thuê"} {tname(m,ts)} {city}</a></li>' for m,ts in [("ban","can-ho-chung-cu"),("ban","nha-rieng"),("thue","can-ho-chung-cu")])
    def bcard(b, R): return f'<article class="dir" data-city="{b["city"]}" data-name="{E(b["name"].lower())}"><span class="av av-xl" aria-hidden="true">{b["name"].split()[-1][0]}</span><div><h2><a href="{R}moi-gioi/{b["id"]}.html">{E(b["name"])}</a></h2><p class="muted">{ic("pin")}{b["city"]} · {b["years"]} năm kinh nghiệm</p><p class="muted">{E(b["company"])}</p><p>{ic("phone")}{b["phone"][:7]}***</p></div><div class="dir-area"><b>KHU VỰC HOẠT ĐỘNG</b><ul>{area_links(R,b["city"])}</ul></div></article>'
    def ccard(c, R): return f'<article class="dir" data-city="{c["city"]}" data-name="{E(c["name"].lower())}"><span class="logo-sq" aria-hidden="true">{initials(c["name"])}</span><div><h2><a href="{R}doanh-nghiep/{c["slug"]}.html">{E(c["name"])}</a></h2><p class="muted">{ic("pin")}{E(c["addr"])}</p><p>{ic("phone")}{c["phone"]}</p></div><div class="dir-area"><b>KHU VỰC HOẠT ĐỘNG</b><ul>{area_links(R,c["city"])}</ul></div></article>'
    def side(R):
        li = ''.join(f'<li><a href="{R}{lurl("ban",s)}">Bán {n} ({len([l for l in LISTINGS if l["ts"]==s and l["mode"]=="ban"])})</a></li>' for s,n,_ in BAN)
        li2 = ''.join(f'<li><a href="{R}{lurl("thue",s)}">Cho thuê {n} ({len([l for l in LISTINGS if l["ts"]==s and l["mode"]=="thue"])})</a></li>' for s,n,_ in THUE)
        return f'<aside class="side"><div class="box"><h2>Theo loại BĐS</h2><h3 class="h3s">Nhà đất bán</h3><ul class="lk">{li}</ul><h3 class="h3s">Nhà đất cho thuê</h3><ul class="lk">{li2}</ul></div></aside>'
    page('nha-moi-gioi.html', 'Danh bạ nhà môi giới', lambda R: f'<div class="container">{sform(R)}<div class="lst-wrap"><div class="lst-main">{crumbs(R,[("Trang chủ","index.html"),("Nhà môi giới",None)])}<h1>Danh bạ nhà môi giới</h1>{tabs(R,"mg")}<div class="dir-list">{"".join(bcard(b,R) for b in BROKERS)}</div><p class="empty" id="noRes" hidden>Không tìm thấy kết quả phù hợp.</p></div>{side(R)}</div></div>', 'db')
    page('doanh-nghiep.html', 'Danh bạ doanh nghiệp', lambda R: f'<div class="container">{sform(R)}<div class="lst-wrap"><div class="lst-main">{crumbs(R,[("Trang chủ","index.html"),("Doanh nghiệp",None)])}<h1>Danh bạ doanh nghiệp</h1>{tabs(R,"dn")}<div class="dir-list">{"".join(ccard(c,R) for c in COMPS)}</div><p class="empty" id="noRes" hidden>Không tìm thấy kết quả phù hợp.</p></div>{side(R)}</div></div>', 'db')
    for b in BROKERS:
        def body(R, b=b):
            ls = [l for l in LISTINGS if l['agent']==b['id']-1]
            return f'<div class="container">{crumbs(R,[("Nhà môi giới","nha-moi-gioi.html"),(b["name"],None)])}<div class="prof"><span class="av av-xl" aria-hidden="true">{b["name"].split()[-1][0]}</span><div><h1>{E(b["name"])}</h1><p class="muted">Môi giới tại {b["city"]} · {b["years"]} năm kinh nghiệm · {E(b["company"])} (hồ sơ mẫu)</p></div><button class="btn btn-teal" data-phone="{b["phone"]}">{ic("phone")}<span>{b["phone"][:7]}*** · Hiện số</span></button></div><h2>Tin đăng ({len(ls)})</h2><div class="rows">{"".join(row(l,R) for l in ls)}</div></div>'
        page(f"moi-gioi/{b['id']}.html", f"Môi giới {b['name']}", body, 'db')
    for c in COMPS:
        def body(R, c=c):
            pj = [p for p in PROJECTS if p['dev']==c['name']]
            staff = ''.join(f'<a class="chip" href="{R}moi-gioi/{b["id"]}.html">{E(b["name"])}</a>' for b in BROKERS if b["company"]==c["name"])
            return f'<div class="container">{crumbs(R,[("Doanh nghiệp","doanh-nghiep.html"),(c["name"],None)])}<div class="prof"><span class="logo-sq" aria-hidden="true">{initials(c["name"])}</span><div><h1>{E(c["name"])}</h1><p class="muted">{ic("pin")}{E(c["addr"])} · Thành lập {c["founded"]} (hồ sơ mẫu)</p></div><a class="btn btn-teal" href="{R}lien-he.html">{ic("mail")}Liên hệ</a></div><h2>Giới thiệu</h2>{para(c["founded"], c["name"], 2)}<h2>Dự án đã phát triển ({len(pj)})</h2><div class="grid4">{"".join(pcard(p,R) for p in pj) or "<p class=muted>Chưa có dự án trong dữ liệu mẫu.</p>"}</div><h2>Nhân sự môi giới</h2><div class="chips">{staff or "<span class=muted>Chưa có</span>"}</div></div>'
        page(f"doanh-nghiep/{c['slug']}.html", c['name'], body, 'db')

def AUTHFORM(mode, R):
    if mode == 'login':
        return f'<form class="ctf" data-auth-form="login"><label>Số điện thoại hoặc email<input name="u" required autocomplete="username"></label><label>Mật khẩu<input name="p" type="password" required minlength="6" autocomplete="current-password"></label><button class="btn btn-red btn-blk">Đăng nhập</button><p class="row-sb"><label class="tgl"><input type="checkbox"> Nhớ tài khoản</label><a href="{R}quen-mat-khau.html">Quên mật khẩu?</a></p><p class="or">Hoặc</p><button type="button" class="btn btn-blk" data-demo-toast="Demo: chưa kết nối Google">Đăng nhập với Google</button><p class="muted">Chưa là thành viên? <a href="{R}dang-ky.html" data-auth="register">Đăng ký tại đây</a></p><p class="note">Demo: không có máy chủ, tài khoản chỉ lưu trong trình duyệt.</p></form>'
    return f'<form class="ctf" data-auth-form="register"><label>Họ tên<input name="n" required autocomplete="name"></label><label>Số điện thoại hoặc email<input name="u" required autocomplete="username"></label><label>Mật khẩu (tối thiểu 6 ký tự)<input name="p" type="password" required minlength="6" autocomplete="new-password"></label><label class="tgl"><input type="checkbox" required> Tôi đồng ý với <a href="{R}dieu-khoan-thoa-thuan.html">Điều khoản thỏa thuận</a></label><button class="btn btn-red btn-blk">Tạo tài khoản</button><p class="muted">Đã có tài khoản? <a href="{R}dang-nhap.html" data-auth="login">Đăng nhập</a></p><p class="note">Demo: không có máy chủ, tài khoản chỉ lưu trong trình duyệt.</p></form>'

def DANGTIN(R):
    types_b = ''.join(f'<option value="ban:{s}">Bán {n}</option>' for s,n,_ in BAN); types_t = ''.join(f'<option value="thue:{s}">Cho thuê {n}</option>' for s,n,_ in THUE)
    cities = ''.join(f'<option>{c}</option>' for c in CITIES); dist = E(json.dumps({c:v[3] for c,v in CITIES.items()}, ensure_ascii=False))
    plans = ''.join(f'<label class="plan plan-r"><input type="radio" name="plan" value="{n}" data-price="{p}"{" checked" if i==0 else ""}><b>{n}</b><span>{p:,} đ/ngày</span></label>'.replace(',', '.') for i,(n,p) in enumerate([("Tin thường",2700),("VIP Bạc",30000),("VIP Vàng",70000),("VIP Kim Cương",280000)]))
    return f'''<div class="container post">{crumbs(R,[("Trang chủ","index.html"),("Đăng tin",None)])}<h1>Đăng tin bất động sản</h1><ol class="stepper" aria-label="Các bước"><li class="on">Thông tin BĐS</li><li>Hình ảnh & mô tả</li><li>Cấu hình tin</li><li>Xác nhận</li></ol>
<form id="postForm" novalidate data-dists="{dist}">
<fieldset class="step" data-step="0"><legend>1. Thông tin cơ bản</legend><div class="seg seg-r" role="radiogroup" aria-label="Nhu cầu"><label><input type="radio" name="mode" value="ban" checked> Bán</label><label><input type="radio" name="mode" value="thue"> Cho thuê</label></div>
<div class="grid2"><label>Loại bất động sản *<select name="type" required><option value="">Chọn loại</option>{types_b}{types_t}</select></label><label>Tỉnh/Thành phố *<select name="city" required><option value="">Chọn</option>{cities}</select></label><label>Quận/Huyện *<select name="dist" required><option value="">Chọn tỉnh trước</option></select></label><label>Đường/Phố<input name="street"></label>
<label>Diện tích (m²) *<input name="area" type="number" min="1" required inputmode="numeric"></label><label>Mức giá *<input name="price" type="number" min="0" step="any" required placeholder="Nhập số"></label><label>Đơn vị<select name="unit"><option value="tỷ">Tỷ</option><option value="triệu">Triệu</option><option value="triệu/tháng">Triệu/tháng</option><option value="thỏa thuận">Thỏa thuận</option></select></label><label>Số phòng ngủ<input name="beds" type="number" min="0"></label></div></fieldset>
<fieldset class="step" data-step="1" hidden><legend>2. Hình ảnh & mô tả</legend><label>Tiêu đề * (30–99 ký tự)<input name="title" required minlength="30" maxlength="99"></label><label>Mô tả * (tối thiểu 30 ký tự)<textarea name="desc" rows="6" required minlength="30"></textarea></label>
<label class="drop">{ic('img')}Chọn ảnh (xem trước trên máy, không tải lên)<input name="photos" type="file" accept="image/*" multiple></label><div class="thumbs" id="thumbs"></div><label>Link video YouTube (tùy chọn)<input name="video" type="url" placeholder="https://"></label></fieldset>
<fieldset class="step" data-step="2" hidden><legend>3. Cấu hình tin đăng</legend><div class="plans plans-sm">{plans}</div>
<div class="grid2"><label>Số ngày đăng<select name="days"><option>7</option><option selected>10</option><option>15</option><option>30</option></select></label><label>Ngày bắt đầu<input name="start" type="date"></label></div><p class="total">Tổng tiền (minh họa): <b id="total">27.000 đ</b></p></fieldset>
<fieldset class="step" data-step="3" hidden><legend>4. Xác nhận</legend><div id="preview" class="preview"></div><div class="grid2"><label>Tên liên hệ *<input name="cname" required autocomplete="name"></label><label>Số điện thoại *<input name="cphone" required type="tel" pattern="[0-9 +]{{9,13}}" autocomplete="tel"></label></div><p class="note">Demo: tin được lưu trong trình duyệt và hiện ở Trang cá nhân, không gửi lên máy chủ, không thanh toán.</p></fieldset>
<p class="err" id="postErr" role="alert"></p><div class="post-nav"><button type="button" class="btn" data-prev hidden>Quay lại</button><button type="button" class="btn btn-red" data-next>Tiếp tục</button><button class="btn btn-red" data-submit hidden>Đăng tin</button></div></form></div>'''

def MAPPAGE(R):
    opts = ''.join(f'<option value="{v[0]}">{c}</option>' for c,v in CITIES.items())
    return f'''<div class="map-wrap"><div class="map-side"><h1 class="map-h">Xem bản đồ</h1><form class="map-f" id="mapF"><label class="sr" for="mm">Nhu cầu</label><select id="mm" name="mode"><option value="ban">Nhà đất bán</option><option value="thue">Nhà đất cho thuê</option><option value="pj">Dự án</option></select><label class="sr" for="mc">Tỉnh thành</label><select id="mc" name="city"><option value="">Toàn quốc</option>{opts}</select></form><p class="sub" id="mapCount" aria-live="polite"></p><div id="mapList" class="map-list"></div><p class="note">Vị trí là tọa độ mẫu gần đúng theo quận. Bản đồ © OpenStreetMap.</p></div><div id="map" role="region" aria-label="Bản đồ tin đăng"></div></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script><script src="{R}js/data.js"></script><script src="{R}js/map.js" defer></script>'''

def legal(R, title, secs):
    toc = ''.join(f'<li><a href="#{a}">{b}</a></li>' for a,b in secs)
    body = ''.join(f'<h2 id="{a}">{i+1}. {b}</h2>' + para(i*5+len(title), b, 2) for i,(a,b) in enumerate(secs))
    return f'<div class="container art-wrap"><article class="art">{crumbs(R,[("Trang chủ","index.html"),(title,None)])}<h1>{title}</h1><p class="note">Văn bản mẫu cho website demo, không có giá trị pháp lý.</p><nav class="toc" aria-label="Mục lục"><b>Mục lục</b><ol>{toc}</ol></nav>{body}</article></div>'

def misc_pages():
    plans = [('Tin thường','2.700','Hiển thị dưới các tin VIP',['Hiển thị tiêu chuẩn','Tối đa 24 ảnh']),('VIP Bạc','30.000','Hiển thị trên tin thường',['Ảnh lớn hơn','Nhãn VIP Bạc','Ưu tiên tìm kiếm']),('VIP Vàng','70.000','Hiển thị trên VIP Bạc',['Hiển thị 4 ảnh','Nhãn VIP Vàng','Ưu tiên cao']),('VIP Kim Cương','280.000','Vị trí cao nhất',['Ảnh cỡ lớn nhất','Nhãn Kim Cương','Luôn ở đầu trang','Tiêu đề chữ đỏ in hoa'])]
    def bg(R):
        cards = ''.join(f'<article class="plan{" plan-hot" if i==3 else ""}"><h2>{n}</h2><p class="price"><b>{p}</b> đ/ngày</p><p class="muted">{d}</p><ul class="ticks">{"".join(f"<li>{ic(chr(99)+chr(104)+chr(101)+chr(99)+chr(107))}{x}</li>" for x in f)}</ul><a class="btn{" btn-red" if i==3 else ""} btn-blk" href="{R}dang-tin.html">Đăng tin</a></article>' for i,(n,p,d,f) in enumerate(plans))
        th = ''.join(f'<th scope="col">{n}</th>' for n,*_ in plans)
        trs = ''.join(f'<tr><th scope="row">{k}</th>' + ''.join(f'<td>{v}</td>' for v in vs) + '</tr>' for k,vs in [("Số ảnh hiển thị",["1","1","4","5"]),("Thứ tự hiển thị",["4","3","2","1"]),("Đẩy tin miễn phí",["–","–","1 lần/tuần","3 lần/tuần"]),("Thời gian tối thiểu",["10 ngày","7 ngày","7 ngày","7 ngày"])])
        mem = ''.join(f'<article class="plan"><h2>{n}</h2><p class="price"><b>{p}</b> đ/tháng</p><p class="muted">{d}</p></article>' for n,p,d in [("Cơ bản","199.000","15 tin thường + 1 VIP Bạc"),("Tiêu chuẩn","499.000","30 tin + 5 VIP Bạc + 2 VIP Vàng"),("Cao cấp","1.299.000","Không giới hạn tin thường + 10 VIP")])
        return f'<div class="container">{crumbs(R,[("Trang chủ","index.html"),("Bảng giá dịch vụ",None)])}<div class="hero-s"><h1>Bảng giá dịch vụ</h1><p>Giá minh họa cho website demo, đơn vị đồng/ngày, chưa gồm VAT.</p></div><div class="plans">{cards}</div><h2>So sánh chi tiết</h2><div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Tính năng</th>{th}</tr></thead><tbody>{trs}</tbody></table></div><h2>Gói hội viên</h2><div class="plans plans-3">{mem}</div></div>'
    page('bang-gia-dich-vu.html', 'Bảng giá dịch vụ tin đăng', bg)
    def auth(mode):
        return lambda R: f'<div class="auth-pg container"><div class="auth-art"><p class="auth-tag">Tìm nhà đất<br>Dẫn lối an cư</p><img src="{img(14,R)}" alt="" width="800" height="600"></div><div class="auth-box"><p class="muted">Xin chào bạn</p><h1>{"Đăng nhập để tiếp tục" if mode=="login" else "Đăng ký tài khoản mới"}</h1>{AUTHFORM(mode,R)}</div></div>'
    page('dang-nhap.html', 'Đăng nhập', auth('login')); page('dang-ky.html', 'Đăng ký', auth('register'))
    page('quen-mat-khau.html', 'Khôi phục mật khẩu', lambda R: f'<div class="auth-pg container"><div class="auth-box"><h1>Khôi phục mật khẩu</h1><form class="ctf" data-demo-form="Demo: không gửi email/SMS thật"><label>Email hoặc số điện thoại<input required autocomplete="username"></label><button class="btn btn-red btn-blk">Gửi mã</button></form><p><a href="{R}dang-nhap.html">Quay lại đăng nhập</a></p></div></div>')
    page('dang-tin.html', 'Đăng tin bất động sản', DANGTIN)
    page('tin-da-luu.html', 'Tin đăng đã lưu', lambda R: f'<div class="container">{crumbs(R,[("Trang chủ","index.html"),("Tin đã lưu",None)])}<h1>Tin đăng đã lưu</h1><p class="sub" id="savedCount"></p><div class="grid4" id="savedList" data-saved></div><div class="empty" id="savedEmpty" hidden><p>Bạn chưa lưu tin nào. Bấm biểu tượng trái tim trên tin đăng để lưu (lưu trong trình duyệt).</p><a class="btn btn-red" href="{R}nha-dat-ban.html">Xem tin nhà đất bán</a></div></div><script src="{R}js/data.js"></script>')
    page('trang-ca-nhan.html', 'Trang cá nhân', lambda R: f'<div class="container acc"><aside class="acc-nav"><div class="ag"><span class="av av-lg" aria-hidden="true" id="accAv">?</span><b id="accName">Khách</b></div><a href="#tin">Quản lý tin đăng</a><a href="{R}tin-da-luu.html">Tin đã lưu</a><a href="#tk">Thông tin cá nhân</a><a href="{R}bang-gia-dich-vu.html">Gói hội viên</a><button type="button" class="lnk" data-logout>Đăng xuất</button></aside><div><h1>Trang cá nhân</h1><p class="note">Demo: dữ liệu chỉ lưu trong trình duyệt của bạn (localStorage), không gửi đi đâu.</p><section id="tin"><div class="sec-h"><h2>Tin đăng của tôi</h2><a class="btn btn-red btn-sm" href="{R}dang-tin.html">Đăng tin mới</a></div><div id="myPosts" class="my-posts"></div></section><section id="tk"><h2>Thông tin cá nhân</h2><form class="ctf grid2" data-profile><label>Họ tên<input name="name" autocomplete="name"></label><label>Số điện thoại<input name="phone" type="tel" autocomplete="tel"></label><label>Email<input name="email" type="email" autocomplete="email"></label><div><button class="btn btn-red">Lưu thay đổi</button></div></form></section></div></div>')
    page('lien-he.html', 'Liên hệ', lambda R: f'<div class="container">{crumbs(R,[("Trang chủ","index.html"),("Liên hệ",None)])}<div class="two"><div><h1>Liên hệ NhàĐất Việt</h1><p>Website demo – các thông tin dưới đây là giả lập.</p><ul class="ticks"><li>{ic("pin")}Tầng 10, Tòa nhà Demo, Cầu Giấy, Hà Nội</li><li>{ic("phone")}Hotline: 1900 0000</li><li>{ic("mail")}hotro@nhadatviet.demo</li></ul><h2>Văn phòng</h2><div class="grid2"><div class="box"><b>Hà Nội</b><p class="muted">Cầu Giấy, Hà Nội</p></div><div class="box"><b>TP.HCM</b><p class="muted">Quận 1, TP.HCM</p></div></div></div><form class="ctf box" data-demo-form="Đã gửi liên hệ (demo, không gửi thật)"><h2>Gửi yêu cầu</h2><label>Họ tên<input required autocomplete="name"></label><label>Email<input required type="email" autocomplete="email"></label><label>Chủ đề<select><option>Hỗ trợ đăng tin</option><option>Báo lỗi</option><option>Hợp tác quảng cáo</option><option>Khác</option></select></label><label>Nội dung<textarea rows="5" required></textarea></label><button class="btn btn-red">Gửi</button></form></div></div>')
    stats = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in [(len(LISTINGS),"tin đăng mẫu"),(len(PROJECTS),"dự án mẫu"),(len(BROKERS),"môi giới mẫu"),(len(CITIES),"tỉnh thành")])
    page('gioi-thieu.html', 'Giới thiệu', lambda R: f'<div class="about-hero"><div class="container"><h1>Về NhàĐất Việt</h1><p>Một website demo mô phỏng nền tảng mua bán, cho thuê nhà đất – xây dựng để minh họa giao diện và trải nghiệm.</p></div></div><div class="container"><div class="stats">{stats}</div><h2>Sứ mệnh</h2>{para(1,"Nền tảng",2)}<h2 id="app">Ứng dụng di động</h2><p>Bản demo chưa có ứng dụng thật. Nút “Tải ứng dụng/Mở App” chỉ dẫn tới mục này.</p></div>')
    page('quy-che-hoat-dong.html', 'Quy chế hoạt động', lambda R: legal(R, 'Quy chế hoạt động', [('chung','Nguyên tắc chung'),('dang-tin','Quy định đăng tin'),('kiem-duyet','Kiểm duyệt nội dung'),('thanh-toan','Thanh toán dịch vụ'),('khieu-nai','Giải quyết khiếu nại'),('trach-nhiem','Trách nhiệm các bên')]))
    page('dieu-khoan-thoa-thuan.html', 'Điều khoản thỏa thuận', lambda R: legal(R, 'Điều khoản thỏa thuận', [('pham-vi','Phạm vi áp dụng'),('tai-khoan','Tài khoản người dùng'),('noi-dung','Nội dung do người dùng cung cấp'),('bao-mat','Chính sách bảo mật'),('cookie','Cookie'),('thay-doi','Thay đổi điều khoản')]))
    faqs = [('Tài khoản',[('Làm sao để đăng ký tài khoản?','Bấm “Đăng ký” ở góc phải, nhập số điện thoại/email và mật khẩu. Đây là bản demo nên tài khoản chỉ lưu trong trình duyệt.'),('Quên mật khẩu thì làm thế nào?','Dùng trang Khôi phục mật khẩu (demo).')]),('Đăng tin',[('Đăng tin có mất phí không?','Xem Bảng giá dịch vụ (giá minh họa).'),('Bao lâu tin được duyệt?','Trong bản demo, tin được lưu ngay vào Trang cá nhân của bạn.'),('Tôi có thể xóa tin không?','Có, trong Trang cá nhân > Tin đăng của tôi.')]),('Tìm kiếm',[('Làm sao lọc theo quận?','Vào trang danh sách, chọn tỉnh thành rồi chọn quận ở hàng chip phía trên.'),('Bản đồ hoạt động thế nào?','Trang Xem bản đồ dùng OpenStreetMap, vị trí tin là tọa độ mẫu gần đúng.')]),('Thanh toán',[('Có những hình thức thanh toán nào?','Bản demo không có thanh toán thật.')])]
    fq = ''.join(f'<h2>{g}</h2>' + ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q,a in qs) for g,qs in faqs)
    page('hoi-dap.html', 'Câu hỏi thường gặp', lambda R: f'<div class="container art-wrap"><article class="art">{crumbs(R,[("Trang chủ","index.html"),("Hỏi đáp",None)])}<h1>Câu hỏi thường gặp</h1><label class="sr" for="fq">Tìm câu hỏi</label><input id="fq" class="inp" placeholder="Tìm câu hỏi…" data-faq-filter>{fq}</article></div>')
    page('ban-do.html', 'Xem bản đồ bất động sản', MAPPAGE, extra_head='<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">', body_cls='map-body')
    page('tim-kiem.html', 'Kết quả tìm kiếm', lambda R: f'<div class="container">{crumbs(R,[("Trang chủ","index.html"),("Tìm kiếm",None)])}<h1 id="sqh">Kết quả tìm kiếm</h1><p class="sub" id="sqc"></p><div class="grid4" id="sres" data-search-results></div></div><script src="{R}js/data.js"></script>')
    page('404.html', 'Không tìm thấy trang', lambda R: f'<div class="container nf"><p class="nf-code">404</p><h1>Không tìm thấy trang</h1><p>Trang bạn tìm có thể đã bị xóa hoặc đường dẫn không đúng.</p><p><a class="btn btn-red" href="{R}index.html">Về trang chủ</a> <a class="btn" href="{R}nha-dat-ban.html">Xem nhà đất bán</a></p></div>')
    cr = json.load(open(os.path.join(core.OUT,'img','credits.json')))
    rows = ''.join(f'<tr><td><img src="img/{c["f"]}" alt="" width="80" height="60" loading="lazy"></td><td><a href="{E(c["src"])}" rel="noopener">{E(c["title"].replace("File:",""))}</a></td><td>{E(c["lic"])}</td></tr>' for c in cr)
    page('nguon-anh.html', 'Nguồn ảnh', lambda R: f'<div class="container"><h1>Nguồn ảnh</h1><p>Ảnh lấy từ Wikimedia Commons theo giấy phép tự do (CC/PD), đã cắt 4:3 và thu nhỏ. Không dùng ảnh của batdongsan.com.vn. Bấm vào tên tệp để xem tác giả và giấy phép đầy đủ.</p><div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Ảnh</th><th scope="col">Tác phẩm gốc</th><th scope="col">Giấy phép</th></tr></thead><tbody>{rows}</tbody></table></div></div>')

def home():
    def body(R):
        hn = [l for l in LISTINGS if l['vip'] in ('kimcuong','vang')][:8]
        locs = [('Hà Nội',14),('TP.HCM',13),('Đà Nẵng',6),('Bình Dương',12),('Hải Phòng',38),('Khánh Hòa',29)]
        types_opt = ''.join(f'<option value="{s}">{n[0].upper()+n[1:]}</option>' for s,n,_ in BAN)
        copts = ''.join(f'<option value="{v[0]}">{c}</option>' for c,v in CITIES.items())
        vids = ''.join(vcard(v,R) for v in VIDEOS)
        loc = ''.join(f'<a class="locc{" locc-big" if i==0 else ""}" href="{R}{lurl("ban",None,c)}"><img src="{img(n,R)}" alt="" loading="lazy" width="600" height="450"><span><b>{c}</b><small>{len([l for l in LISTINGS if l["city"]==c])} tin đăng</small></span></a>' for i,(c,n) in enumerate(locs))
        utils = ''.join(f'<a href="{R}{u}">{ic(i,"ic-lg")}<span>{t}</span></a>' for t,u,i in [('Xem tuổi xây nhà','wiki/phong-tuc.html','compass'),('Chi phí làm nhà','wiki/noi-ngoai-that.html','calc'),('Tính lãi suất','wiki/tai-chinh.html','chart'),('Tư vấn phong thủy','wiki/phong-tuc.html','home')])
        logos = ''.join(f'<a href="{R}doanh-nghiep/{c["slug"]}.html" class="logo-sq" aria-label="{E(c["name"])}">{initials(c["name"])}</a>' for c in COMPS[:8])
        NICE={3,4,15,16,20,23,24,26,29,31,33,34,35,37,42,43,44}
        lux = sorted([l for l in LISTINGS if l['mode']=='ban' and l['img'][0] in NICE], key=lambda l: -l['price'])[:5]
        sug = [{'t':d,'s':c,'u':R+lurl('ban',None,c,d),'k':'Khu vực'} for c in CITIES for d in CITIES[c][3] if has('ban',None,d)] + [{'t':c,'s':'Tỉnh/thành','u':R+lurl('ban',None,c),'k':'Tỉnh thành'} for c in CITIES] + [{'t':p['name'],'s':p['dist']+', '+p['city'],'u':R+'du-an/'+p['slug']+'.html','k':'Dự án'} for p in PROJECTS]
        stats = [(len(LISTINGS),'tin đăng mẫu'),(len(PROJECTS),'dự án'),(len(AGENTS),'môi giới'),(len(CITIES),'tỉnh thành')]
        luxc = ''.join(card(l,R) for l in lux)
        return f'''<section class="hero hero-lux" aria-label="Tìm kiếm"><picture class="hero-bg"><source media="(max-width:700px)" srcset="{R}img/hero-m.jpg"><img src="{R}img/hero.jpg" alt="Toàn cảnh TP.HCM lúc hoàng hôn" width="2400" height="1350" fetchpriority="high"></picture>
<div class="hero-in container"><p class="eyebrow">Nền tảng bất động sản tuyển chọn</p><h1 class="hero-h">Tìm ngôi nhà xứng tầm<br>với phong cách sống của bạn</h1><p class="hero-sub">Căn hộ, biệt thự và dự án được chọn lọc trên khắp Việt Nam. Dữ liệu minh họa.</p>
<form class="search" id="homeSearch" data-search-home action="{R}tim-kiem.html" role="search"><div class="stabs" role="tablist" aria-label="Loại giao dịch"><button type="button" role="tab" aria-selected="true" data-m="ban">Mua bán</button><button type="button" role="tab" aria-selected="false" data-m="thue">Cho thuê</button><button type="button" role="tab" aria-selected="false" data-m="duan">Dự án</button></div>
<div class="sbox"><span class="sbar-in ac">{ic('search')}<label class="sr" for="hq">Từ khóa</label><input id="hq" name="q" placeholder="Quận, dự án hoặc khu vực, ví dụ: Tây Hồ" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="acList"><ul class="ac-list" id="acList" role="listbox" hidden></ul></span><button class="btn btn-red btn-search">{ic('search')}<span>Tìm kiếm</span></button></div>
<div class="sfilters"><label class="fsel"><span>Khu vực</span><select id="hc" name="city"><option value="">Toàn quốc</option>{copts}</select></label><label class="fsel"><span>Loại hình</span><select id="ht" name="ts"><option value="">Tất cả</option>{types_opt}</select></label><label class="fsel"><span>Mức giá</span><select id="hp" name="price"><option value="">Mọi mức giá</option><option value="0-3000000000">Dưới 3 tỷ</option><option value="3000000000-7000000000">3 – 7 tỷ</option><option value="7000000000-1e15">Trên 7 tỷ</option></select></label><label class="fsel"><span>Diện tích</span><select id="ha" name="area"><option value="">Mọi diện tích</option><option value="0-50">Dưới 50 m²</option><option value="50-100">50 – 100 m²</option><option value="100-1e9">Trên 100 m²</option></select></label></div>
<p class="hot">Gợi ý: <a href="{R}{lurl('ban',None,'Hà Nội','Tây Hồ')}">Tây Hồ</a><a href="{R}{lurl('ban','nha-biet-thu-lien-ke')}">Biệt thự</a><a href="{R}{lurl('ban',None,'TP.HCM','Thủ Đức')}">Thủ Đức</a><a href="{R}du-an.html">Dự án mới</a></p></form></div>
<script type="application/json" id="acData">{json.dumps(sug, ensure_ascii=False).replace("</","<\\/")}</script></section>
<section class="trust" aria-label="Số liệu"><div class="container trust-in">{''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n,t in stats)}<div class="trust-t">{ic('shield')}<span>Thông tin minh bạch: mọi số liệu trên site là dữ liệu mẫu, có ghi rõ.</span></div></div></section>
<nav class="quick container" aria-label="Lối tắt"><a href="{R}nha-dat-ban.html">{ic('home','ic-lg')}Mua bán</a><a href="{R}nha-dat-cho-thue.html">{ic('building','ic-lg')}Cho thuê</a><a href="{R}du-an.html">{ic('pin','ic-lg')}Dự án</a><a href="{R}ban-do.html">{ic('map','ic-lg')}Bản đồ</a></nav>
<div class="container"><section class="lux-sec" aria-labelledby="luxh"><div class="sec-h"><div><p class="eyebrow">Tuyển chọn cao cấp</p><h2 id="luxh">Bất động sản giá trị nhất tuần này</h2></div><a href="{R}nha-dat-ban.html">Xem tất cả {ic('chev')}</a></div><div class="lux-grid">{luxc}</div></section>
<section><div class="sec-h"><h2>Tin tức bất động sản</h2><a href="{R}tin-tuc.html">Xem thêm {ic('chev')}</a></div><div class="news-top">{ncard(NEWS[0],R,True)}<div class="news-side">{''.join(ncard(n,R) for n in NEWS[1:5])}</div></div></section>
<section><div class="sec-h"><h2>Bất động sản dành cho bạn</h2><a href="{R}tin-da-luu.html">Tin đã lưu {ic('chev')}</a></div><div class="grid4">{''.join(card(l,R) for l in hn)}</div><p class="center"><a class="btn" href="{R}nha-dat-ban.html">Xem thêm tin {ic('down')}</a></p></section>
<section aria-labelledby="pjh"><div class="sec-h"><h2 id="pjh">Dự án bất động sản nổi bật</h2><span class="car-ctl"><button type="button" class="car-btn" data-car="pjCar" data-dir="-1" aria-label="Dự án trước">{ic('chevl')}</button><button type="button" class="car-btn" data-car="pjCar" data-dir="1" aria-label="Dự án sau">{ic('chev')}</button><a href="{R}du-an.html">Xem thêm {ic('chev')}</a></span></div><div class="carousel" id="pjCar" tabindex="0" aria-label="Danh sách dự án, cuộn ngang">{''.join(pcard(p,R) for p in PROJECTS[:12])}</div></section>
</div><section class="vstrip" aria-labelledby="vh"><div class="container"><div class="sec-h"><h2 id="vh">Video đánh giá bất động sản</h2><span class="car-ctl"><button type="button" class="car-btn" data-car="vCar" data-dir="-1" aria-label="Video trước">{ic('chevl')}</button><button type="button" class="car-btn" data-car="vCar" data-dir="1" aria-label="Video sau">{ic('chev')}</button><a href="{R}video-danh-gia.html">Xem thêm {ic('chev')}</a></span></div><div class="carousel carousel-v" id="vCar" tabindex="0" aria-label="Video, cuộn ngang">{vids}</div></div></section><div class="container">
<section><h2>Bất động sản theo địa điểm</h2><div class="locs">{loc}</div></section>
<section><h2>Hỗ trợ tiện ích</h2><div class="utils">{utils}</div></section>
<section><h2>Doanh nghiệp tiêu biểu</h2><div class="logos">{logos}</div></section></div>'''
    page('index.html', 'Mua bán, cho thuê nhà đất toàn quốc', body, desc='NhàĐất Việt – website demo mua bán, cho thuê nhà đất, dự án, tin tức.', seo=lambda R: seo_block(R,'ban',None))

def sitemap():
    groups = {}
    for p in PAGES:
        k = p.split('/')[0] if '/' in p else ('Danh sách nhà đất' if p.startswith(('ban-','cho-thue-','nha-dat-')) else ('Danh mục dự án' if p.startswith('du-an-') else 'Trang khác'))
        groups.setdefault(k, []).append(p)
    def body(R):
        s = ''.join(f'<details><summary>{k} ({len(v)})</summary><ul class="cols">' + ''.join(f'<li><a href="{R}{u}">{u}</a></li>' for u in sorted(v)) + '</ul></details>' for k,v in sorted(groups.items()))
        return f'<div class="container"><h1>Sơ đồ trang ({len(PAGES)+1} trang HTML)</h1>{s}</div>'
    page('sitemap.html', 'Sơ đồ trang', body)

def data_js(listing_urls):
    L = [dict(id=l['id'], m=l['mode'], ts=l['ts'], tn=l['tn'], c=l['city'], cs=CITIES[l['city']][0], d=l['dist'], t=l['title'], p=l['price'], a=l['area'], b=l['beds'], img=l['img'][0], lat=l['lat'], lng=l['lng'], v=l['vip'], day=l['day']) for l in LISTINGS]
    P = [dict(id=p['id'], n=p['name'], s=p['slug'], c=p['city'], cs=CITIES[p['city']][0], d=p['dist'], img=p['img'][0], lat=round(p['lat'],5), lng=round(p['lng'],5), st=p['status'], pr=p['price']) for p in PROJECTS]
    D = {d: [dslug(d,c), c, CITIES[c][0]] for c in CITIES for d in CITIES[c][3]}
    W = [dict(t=w['t'], u=f"wiki/{w['cat']}/{w['slug']}.html") for w in WIKI] + [dict(t=n['t'], u=f"tin-tuc/{n['slug']}.html") for n in NEWS]
    js = '// DỮ LIỆU MẪU (DEMO) – sinh bởi tools/build.py, không phải tin thật\n'
    js += 'window.ND={L:' + json.dumps(L, ensure_ascii=False, separators=(',',':')) + ',P:' + json.dumps(P, ensure_ascii=False, separators=(',',':')) + ',D:' + json.dumps(D, ensure_ascii=False) + ',C:' + json.dumps({c:[v[0],v[1],v[2]] for c,v in CITIES.items()}, ensure_ascii=False) + ',A:' + json.dumps(W, ensure_ascii=False) + ',U:' + json.dumps(sorted(listing_urls)) + '};\n'
    open(os.path.join(core.OUT,'js','data.js'),'w').write(js)
