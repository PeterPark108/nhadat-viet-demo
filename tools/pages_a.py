# Trang danh sách, chi tiết tin, dự án, tin tức, wiki
import json
from core import *
PER = 20
def listing_pages():
    made = set()
    for mode in ('ban','thue'):
        for ts in [None] + [s for s,_,_ in TYPES[mode]]:
            places = [(None,None)] + [(c,None) for c in CITIES] + [(c,d) for c in CITIES for d in CITIES[c][3] if has(mode,ts,d)]
            for c, d in places:
                res = [l for l in LISTINGS if l['mode']==mode and (ts is None or l['ts']==ts) and (c is None or l['city']==c) and (d is None or l['dist']==d)]
                res.sort(key=lambda l: (['kimcuong','vang','bac','thuong'].index(l['vip']), l['day'], l['id']))
                pages = max(1, math.ceil(len(res)/PER))
                for pnum in range(1, pages+1):
                    url = lurl(mode, ts, c, d, pnum); made.add(url)
                    listing_page(url, mode, ts, c, d, res, pnum, pages)
    return made
def listing_page(url, mode, ts, c, d, res, pnum, pages):
    verb = 'Mua bán' if mode=='ban' else 'Cho thuê'; tn = tname(mode, ts) if ts else 'nhà đất'
    where = f"{d}, {c}" if d else c
    h1 = f"{verb} {tn} {('tại ' + where) if c else 'trên toàn quốc'}"
    items = res[(pnum-1)*PER:pnum*PER]
    def body(R):
        fallback = ''
        if not res:
            sim = [l for l in LISTINGS if l['mode']==mode and (c is None or l['city']==c)][:8]
            fallback = '<div class="empty"><p>Hiện chưa có tin phù hợp trong dữ liệu mẫu.</p></div><h2 class="h2s">Tin tương tự trong khu vực</h2>' + ''.join(row(l,R) for l in sim)
        bc = [('Trang chủ','index.html'), ('Bán' if mode=='ban' else 'Cho thuê', lurl(mode) if (ts or c) else None)]
        if ts: bc.append((tn[0].upper()+tn[1:], lurl(mode, ts) if c else None))
        if c: bc.append((c, lurl(mode, ts, c) if d else None))
        if d: bc.append((d, None))
        types_opt = ''.join(f'<option value="{R}{lurl(mode,s,c,d) if (not d or has(mode,s,d)) else lurl(mode,s,c)}"{" selected" if s==ts else ""}>{"Bán" if mode=="ban" else "Thuê"} {n}</option>' for s,n,_ in TYPES[mode])
        city_opt = ''.join(f'<option value="{R}{lurl(mode,ts,cc)}"{" selected" if cc==c else ""}>{cc}</option>' for cc in CITIES)
        dist_links = ''
        if c and not d:
            ds = [(dd, len([l for l in res if l['dist']==dd])) for dd in CITIES[c][3]]
            dist_links = '<div class="chips">' + ''.join(f'<a class="chip" href="{R}{lurl(mode,ts,c,dd)}">{dd} <small>({n})</small></a>' for dd,n in ds if n) + '</div>'
        if mode=='ban': price_f = [('Dưới 1 tỷ',0,1e9),('1 - 3 tỷ',1e9,3e9),('3 - 5 tỷ',3e9,5e9),('5 - 7 tỷ',5e9,7e9),('7 - 10 tỷ',7e9,1e10),('10 - 20 tỷ',1e10,2e10),('Trên 20 tỷ',2e10,1e15)]
        else: price_f = [('Dưới 3 triệu',0,3e6),('3 - 5 triệu',3e6,5e6),('5 - 10 triệu',5e6,1e7),('10 - 20 triệu',1e7,2e7),('20 - 40 triệu',2e7,4e7),('Trên 40 triệu',4e7,1e15)]
        area_f = [('Dưới 30 m²',0,30),('30 - 50 m²',30,50),('50 - 80 m²',50,80),('80 - 100 m²',80,100),('100 - 150 m²',100,150),('150 - 300 m²',150,300),('Trên 300 m²',300,1e9)]
        mapq = f"?mode={mode}" + (f"&ts={ts}" if ts else '') + (f"&city={CITIES[c][0]}" if c else '')
        flt = lambda key, arr: ''.join(f'<li><button type="button" data-k="{key}" data-min="{int(a)}" data-max="{int(b)}" aria-pressed="false">{t}</button></li>' for t,a,b in arr)
        side = f'''<aside class="side" id="sideF" aria-label="Bộ lọc"><div class="sheet-h"><b>Bộ lọc</b><button type="button" class="hbtn" data-close-filters aria-label="Đóng bộ lọc">{ic('x')}</button></div><div class="box"><h2>Lọc theo khoảng giá</h2><ul class="flt">{flt('price',price_f)}</ul></div>
<div class="box"><h2>Lọc theo diện tích</h2><ul class="flt">{flt('area',area_f)}</ul></div>
<div class="box"><h2>{verb} {tn} theo khu vực</h2><ul class="lk">{''.join(f'<li><a href="{R}{lurl(mode,ts,cc)}">{cc}</a></li>' for cc in CITIES)}</ul></div>
<div class="box box-ad"><p><b>Nhận tin mới phù hợp</b><br>Lưu tiêu chí này để được báo khi có bất động sản mới (demo).</p><button type="button" class="btn btn-red" data-save-search>{ic('bell')}Lưu tìm kiếm</button></div><div class="sheet-f"><button type="button" class="btn" data-reset>Xóa tất cả</button><button type="button" class="btn btn-red" data-close-filters>Xem kết quả</button></div></aside>'''
        return f'''<div class="sbar"><div class="container"><form class="sbar-f" action="{R}tim-kiem.html"><label class="sr" for="kw">Từ khóa</label><span class="sbar-in">{ic('search')}<input id="kw" name="q" placeholder="Nhập địa điểm, dự án, đường phố. VD: Cầu Giấy"></span><input type="hidden" name="mode" value="{mode}"><button class="btn btn-red">Tìm kiếm</button><a class="btn btn-teal" href="{R}ban-do.html{mapq}">{ic('map')}<span>Xem bản đồ</span></a></form>
<div class="fl-row"><label class="sel"><span class="sr">Loại nhà đất</span><select data-nav><option value="{R}{lurl(mode,None,c,d)}">Tất cả loại nhà đất</option>{types_opt}</select></label>
<label class="sel"><span class="sr">Tỉnh thành</span><select data-nav><option value="{R}{lurl(mode,ts)}">Toàn quốc</option>{city_opt}</select></label>
<label class="sel"><span class="sr">Sắp xếp</span><select data-sort><option value="">Thông thường</option><option value="new">Tin mới nhất</option><option value="pa">Giá thấp đến cao</option><option value="pd">Giá cao đến thấp</option><option value="aa">Diện tích bé đến lớn</option></select></label>
<label class="tgl"><input type="checkbox" data-verified> Tin xác thực</label><button type="button" class="btn btn-sm mfbtn" data-open-filters aria-controls="sideF" aria-expanded="false">{ic('sliders')}<span>Bộ lọc</span></button></div></div></div>
<div class="container lst-wrap"><div class="lst-main">{crumbs(R, bc)}<h1>{E(h1)}</h1><p class="sub">Hiện có <b>{len(res)}</b> bất động sản (dữ liệu mẫu){f' · Trang {pnum}/{pages}' if pages>1 else ''}</p>{dist_links}
<div class="ltools"><div class="fchips" id="fchips" aria-live="polite"><span class="muted" id="fcount">{len(items)} tin trên trang này</span></div><div class="vt" role="group" aria-label="Kiểu hiển thị"><button type="button" data-view="list" aria-pressed="true">{ic('list')}<span>Danh sách</span></button><button type="button" data-view="grid" aria-pressed="false">{ic('grid')}<span>Lưới</span></button><a href="{R}ban-do.html{mapq}">{ic('map')}<span>Bản đồ</span></a></div></div>
<div class="rows" id="rows">{''.join(row(l, R) for l in items)}{fallback}</div><div class="empty empty-lg" id="noRes" hidden>{ic('search','ic-lg')}<h2>Chưa có tin khớp bộ lọc</h2><p>Thử nới khoảng giá, diện tích hoặc bỏ bớt điều kiện.</p><button type="button" class="btn" data-reset>Xóa tất cả bộ lọc</button> <button type="button" class="btn btn-red" data-save-search>{ic('bell')}Báo tôi khi có tin mới</button></div>
{pager(R, pnum, pages, lambda i: lurl(mode, ts, c, d, i))}</div>{side}</div>'''
    page(url, f"{h1}{' – Trang '+str(pnum) if pnum>1 else ''}", body, 'ban' if mode=='ban' else 'thue', desc=f"{h1}: {len(res)} tin đăng mẫu, cập nhật 10/2026.", seo=lambda R: seo_block(R, mode, ts))

def detail_pages():
    for l in LISTINGS:
        def body(R, l=l):
            a = AGENTS[l['agent']]; ph = phone_of(l)
            sim = [x for x in LISTINGS if x['mode']==l['mode'] and x['ts']==l['ts'] and x['id']!=l['id']][:4]
            near = [x for x in LISTINGS if x['dist']==l['dist'] and x['id']!=l['id']][:4]
            g = f'<div class="gal" data-gallery><button class="gal-main" data-open="0" aria-label="Xem ảnh lớn"><img src="{img(l["img"][0],R)}" alt="{E(l["title"])}" width="800" height="600"><span class="cnt-img">{ic("img")}{len(l["img"])}</span></button>' + ''.join(f'<button class="gal-t" data-open="{i}" aria-label="Xem ảnh {i+1}"><img src="{img(n,R)}" alt="" loading="lazy" width="200" height="150"></button>' for i,n in enumerate(l['img'][1:5],1)) + '</div>'
            g += '<script type="application/json" data-gallery-src>' + json.dumps([img(n,R) for n in l['img']]) + '</script>'
            specs = [('Diện tích', f"{l['area']} m²"), ('Mức giá', money(l['price'],l['mode'])), ('Hướng nhà', l['dir']), ('Pháp lý', l['legal']), ('Nội thất', l['furn'])]
            if l['beds']: specs += [('Số phòng ngủ', f"{l['beds']} phòng"), ('Số toilet', f"{l['baths']} phòng")]
            if l['floors']: specs.append(('Số tầng', f"{l['floors']} tầng"))
            sp = ''.join(f'<div class="spec"><span>{k}</span><b>{v}</b></div>' for k,v in specs)
            bc = [('Trang chủ','index.html'),('Bán' if l['mode']=='ban' else 'Cho thuê', lurl(l['mode'])),(l['city'], lurl(l['mode'],l['ts'],l['city'])),(l['dist'], lurl(l['mode'],l['ts'],l['city'],l['dist'])),(l['tn'][0].upper()+l['tn'][1:], lurl(l['mode'],l['ts']))]
            loan = ('<section><h2>Ước tính khoản vay</h2><form class="loan" data-loan data-price="'+str(int(l['price']))+'"><label>Tỷ lệ vay (%)<input type="number" name="r" value="70" min="0" max="90"></label><label>Thời hạn (năm)<input type="number" name="y" value="20" min="1" max="35"></label><label>Lãi suất (%/năm)<input type="number" name="i" value="8.5" step="0.1" min="0"></label><output class="loan-out"></output></form></section>') if l['mode']=='ban' else ''
            return f'''<div class="container det">{crumbs(R,bc)}<div class="det-grid"><div>{g}
<h1>{E(l['title'])}</h1><p class="loc">{ic('pin')}{E(l['street'])}, {E(l['dist'])}, {E(l['city'])} · <a href="{R}ban-do.html?id={l['id']}">Xem bản đồ</a></p>
<div class="kpis"><div><span>Mức giá</span><b class="red">{money(l['price'],l['mode'])}</b></div>{f'<div><span>Đơn giá</span><b>{ppm(l)}</b></div>' if l['mode']=='ban' else ''}<div><span>Diện tích</span><b>{l['area']} m²</b></div>{f'<div><span>Phòng ngủ</span><b>{l["beds"]} PN</b></div>' if l['beds'] else ''}<div><span>Pháp lý</span><b>{E(l['legal'])}</b></div>
<div class="kpi-act"><button class="hbtn" data-share aria-label="Chia sẻ liên kết">{ic('share')}</button><button class="hbtn" data-print aria-label="In trang">{ic('print')}</button><button class="qbtn" data-compare='{cmpdata(l,R)}' aria-pressed="false" aria-label="Thêm vào so sánh">{ic('scale')}</button><button class="heart" data-fav="{l['id']}" aria-pressed="false" aria-label="Lưu tin">{ic('heart')}</button></div></div>
<section><h2>Thông tin mô tả</h2>{para(l['id'], l['tn'][0].upper()+l['tn'][1:]+' tại '+l['dist'], 3)}<p>Liên hệ {E(a)} để được tư vấn và xem nhà (thông tin demo).</p></section>
<section><h2>Đặc điểm bất động sản</h2><div class="specs">{sp}</div></section>
<section><h2>Xem trên bản đồ</h2><a class="mapprev" href="{R}ban-do.html?id={l['id']}">{ic('map')}<span>Mở bản đồ khu vực {E(l['dist'])}</span></a></section>{loan}
<div class="meta-row"><span>Ngày đăng: {max(1,26-l['day'])}/10/2026</span><span>Loại tin: {VIPL.get(l['vip'],'Tin thường')}</span><span>Mã tin: ND{100000+l['id']}</span></div>
<section><h2>Bất động sản dành cho bạn</h2><div class="grid4">{''.join(card(x,R) for x in sim)}</div></section>
<section><h2>Tin đăng cùng khu vực</h2><div class="grid4">{''.join(card(x,R) for x in near)}</div></section></div>
<aside class="ct"><div class="ct-card"><div class="ag"><span class="av av-lg" aria-hidden="true">{a.split()[-1][0]}</span><span><small>Được đăng bởi</small><br><a href="{R}moi-gioi/{l['agent']+1}.html"><b>{E(a)}</b></a><br><small>Môi giới (demo)</small></span></div>
<p class="ct-price"><b>{money(l['price'],l['mode'])}</b>{f'<small>{ppm(l)}</small>' if l['mode']=='ban' else ''}</p><button class="btn btn-teal btn-blk" data-phone="{ph}">{ic('phone')}<span>{ph[:7]} *** · Hiện số</span></button><a class="btn btn-blk" href="{R}lien-he.html">{ic('zalo')}Chat qua Zalo</a><a class="btn btn-blk" href="#ctf">{ic('mail')}Gửi email</a>
<form id="ctf" class="ctf" data-demo-form="Đã gửi yêu cầu liên hệ (demo, không gửi đi thật)"><label>Họ tên<input required autocomplete="name" data-msg="Vui lòng nhập họ tên"></label><label>Số điện thoại<input required type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9 +]{{9,13}}" data-msg="Số điện thoại gồm 9–13 chữ số"></label><label>Nội dung<textarea rows="3">Tôi quan tâm tin ND{100000+l['id']}.</textarea></label><button class="btn btn-red btn-blk">Gửi yêu cầu</button></form><p class="ct-note">{ic('shield')}Không chuyển cọc trước khi xem nhà và kiểm tra pháp lý.</p></div></aside></div></div>
<nav class="mbar" aria-label="Liên hệ nhanh"><a class="btn btn-teal" href="tel:{ph}">{ic('phone')}Gọi</a><a class="btn" href="{R}lien-he.html">{ic('zalo')}Zalo</a><a class="btn btn-red" href="#ctf">{ic('mail')}Nhắn tin</a></nav>'''
        page(detail_url(l), l['title'], body, 'ban' if l['mode']=='ban' else 'thue', desc=f"{l['title']} – {l['dist']}, {l['city']}")

def project_pages():
    def lst(R, items, h1, bc):
        rows = ''.join(f"""<article class="pjr"><a href="{R}du-an/{p['slug']}.html" tabindex="-1" aria-hidden="true"><img src="{img(p['img'][0],R)}" alt="" loading="lazy" width="400" height="300"></a><div><span class="st st-{p['id']%3}">{p['status']}</span><h2><a href="{R}du-an/{p['slug']}.html">{E(p['name'])}</a></h2><p class="pr">{p['price']} triệu/m² · {p['ha']} ha · {p['units']} căn</p><p class="loc">{ic('pin')}{E(p['dist'])}, {E(p['city'])}</p><p class="muted">{E(p['pt'][1])} · Chủ đầu tư: {E(p['dev'])}</p></div></article>""" for p in items)
        if not rows: rows = f'<p class="empty">Chưa có dự án thuộc loại hình này trong dữ liệu mẫu. Xem <a href="{R}du-an.html">tất cả dự án</a>.</p>'
        return f'''<div class="container">{crumbs(R,bc)}<div class="sec-h"><h1>{E(h1)}</h1><a class="btn btn-teal" href="{R}ban-do.html?mode=pj">{ic('map')}<span>Xem bản đồ</span></a></div><p class="sub">Có {len(items)} dự án (dữ liệu mẫu)</p><div class="chips">{''.join(f'<a class="chip" href="{R}du-an-{s}.html">{t}</a>' for s,t in PROJ_TYPES)}</div><div class="pj-list">{rows}</div></div>'''
    page('du-an.html', 'Dự án bất động sản mới nhất 2026', lambda R: lst(R, PROJECTS, 'Dự án bất động sản trên toàn quốc', [('Trang chủ','index.html'),('Dự án',None)]), 'duan')
    for s, t in PROJ_TYPES:
        items = [p for p in PROJECTS if p['pt'][0]==s]
        page(f'du-an-{s}.html', f'Dự án {t}', lambda R, items=items, t=t: lst(R, items, f'Dự án {t}', [('Trang chủ','index.html'),('Dự án','du-an.html'),(t,None)]), 'duan')
    for p in PROJECTS:
        def body(R, p=p):
            sale = [l for l in LISTINGS if l['city']==p['city'] and l['ts'] in ('can-ho-chung-cu','nha-biet-thu-lien-ke','dat-nen-du-an','shophouse-nha-pho-thuong-mai')][:4]
            rel = [x for x in PROJECTS if x['city']==p['city'] and x['id']!=p['id']][:4]
            tabs = [('tong-quan','Tổng quan'),('mat-bang','Mặt bằng'),('vi-tri','Vị trí'),('tien-ich','Tiện ích'),('ban-cho-thue','Bán & cho thuê'),('hoi-dap','Hỏi đáp')]
            gal = f'<div class="pgal"><img class="pg-main" src="{img(p["img"][0],R)}" alt="{E(p["name"])}" width="800" height="600">' + ''.join(f'<img src="{img(n,R)}" alt="" loading="lazy" width="400" height="300">' for n in p['img'][1:5]) + f'<span class="st st-{p["id"]%3}">{p["status"]}</span></div>'
            info = [('Diện tích', f"{p['ha']} ha"),('Quy mô', f"{p['units']} căn"),('Loại hình', p['pt'][1]),('Giá tham khảo', f"{p['price']} triệu/m²"),('Bàn giao dự kiến', f"Quý {1+p['id']%4}/{p['year']}"),('Chủ đầu tư', p['dev'])]
            dev = [c for c in COMPS if c['name']==p['dev']][0]
            plan = ''.join(f'<rect x="{20+i*95}" y="{30+(i%2)*20}" width="80" height="{120-(i%3)*15}" rx="4" fill="#fff" stroke="#009BA1"/><text x="{60+i*95}" y="100" text-anchor="middle" font-size="13" fill="#2C2C2C">Tòa {chr(65+i)}</text>' for i in range(6))
            faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in [('Dự án đã có sổ chưa?','Thông tin mẫu: dự án đang hoàn thiện thủ tục cấp sổ theo tiến độ bàn giao.'),('Chính sách thanh toán thế nào?','Thanh toán theo tiến độ, hỗ trợ vay tối đa 70% giá trị căn hộ (demo).'),('Phí quản lý bao nhiêu?','Dự kiến 12.000–18.000 đ/m²/tháng (demo).')])
            return f'''<div class="container det">{crumbs(R,[('Dự án','du-an.html'),(p['pt'][1],f"du-an-{p['pt'][0]}.html"),(p['name'],None)])}<div class="pj-head"><div><h1>{E(p['name'])}</h1><p class="loc">{ic('pin')}{E(p['dist'])}, {E(p['city'])}. <a href="{R}ban-do.html?pj={p['id']}">Xem bản đồ</a></p></div><button class="hbtn" data-share>{ic('share')}Chia sẻ</button></div>{gal}
<nav class="ptabs" aria-label="Mục dự án">{''.join(f'<a href="#{a}">{b}</a>' for a,b in tabs)}</nav><div class="det-grid"><div>
<section id="tong-quan"><h2>Tổng quan dự án</h2><div class="specs">{''.join(f'<div class="spec"><span>{k}</span><b>{E(str(v))}</b></div>' for k,v in info)}</div>{para(p['id']*3, 'Dự án '+p['name'], 3)}<p>Chủ đầu tư: <a href="{R}doanh-nghiep/{dev['slug']}.html">{E(dev['name'])}</a></p></section>
<section id="mat-bang"><h2>Mặt bằng dự án</h2><svg class="plan" viewBox="0 0 600 260" role="img" aria-label="Sơ đồ mặt bằng minh họa"><rect x="5" y="5" width="590" height="250" rx="8" fill="#F2F7F7" stroke="#B9D9DA"/>{plan}<rect x="20" y="190" width="560" height="45" rx="4" fill="#DFF0E3"/><text x="300" y="217" text-anchor="middle" font-size="13" fill="#2C2C2C">Công viên nội khu · Hồ bơi · Sân thể thao</text></svg><p class="muted">Sơ đồ minh họa, không phải mặt bằng thật.</p></section>
<section id="vi-tri"><h2>Vị trí</h2><p>Dự án nằm tại {E(p['dist'])}, {E(p['city'])}, kết nối thuận tiện tới trung tâm, trường học, bệnh viện và trung tâm thương mại.</p><a class="mapprev" href="{R}ban-do.html?pj={p['id']}">{ic('map')}<span>Mở bản đồ vị trí dự án</span></a></section>
<section id="tien-ich"><h2>Tiện ích</h2><ul class="ticks">{''.join(f'<li>{ic("check")}{t}</li>' for t in ['Hồ bơi tràn bờ','Gym & yoga','Vườn nướng BBQ','Trường mầm non nội khu','Siêu thị tiện lợi','Bảo vệ 24/7','Hầm để xe 2 tầng','Sân chơi trẻ em'])}</ul></section>
<section id="ban-cho-thue"><h2>Tin bán & cho thuê quanh dự án</h2><div class="grid4">{''.join(card(l,R) for l in sale)}</div></section>
<section id="hoi-dap"><h2>Câu hỏi thường gặp</h2>{faq}</section>
<section><h2>Dự án khác tại {E(p['city'])}</h2><div class="grid4">{''.join(pcard(x,R) for x in rel)}</div></section></div>
<aside class="ct"><div class="ct-card"><h2>Liên hệ tư vấn miễn phí</h2><p class="muted">Để lại thông tin để nhận tư vấn và cập nhật mới nhất của dự án (demo).</p><form class="ctf" data-demo-form="Đã ghi nhận yêu cầu tư vấn (demo)"><label>Họ tên<input required autocomplete="name"></label><label>Số điện thoại<input required type="tel" autocomplete="tel"></label><button class="btn btn-teal btn-blk">{ic('mail')}Liên hệ lại tôi</button></form></div></aside></div></div>'''
        page(f"du-an/{p['slug']}.html", f"Dự án {p['name']} – {p['dist']}, {p['city']}", body, 'duan')

def news_pages():
    def lst(R, items, h1):
        return f'<div class="container">{crumbs(R,[("Trang chủ","index.html"),("Tin tức",None)])}<h1>{h1}</h1><nav class="chips" aria-label="Chuyên mục"><a class="chip" href="{R}tin-tuc.html">Tất cả</a><a class="chip" href="{R}tin-tuc-ha-noi.html">BĐS Hà Nội</a><a class="chip" href="{R}tin-tuc-tp-hcm.html">BĐS TP.HCM</a></nav><div class="news-top">{ncard(items[0],R,True)}<div class="news-side">{"".join(ncard(n,R) for n in items[1:5])}</div></div><div class="grid3">{"".join(ncard(n,R) for n in items[5:])}</div></div>'
    page('tin-tuc.html', 'Tin tức bất động sản', lambda R: lst(R, NEWS, 'Tin tức bất động sản'), 'tin')
    page('tin-tuc-ha-noi.html', 'Tin tức bất động sản Hà Nội', lambda R: lst(R, [n for n in NEWS if n['city']=='Hà Nội'], 'Bất động sản Hà Nội'), 'tin')
    page('tin-tuc-tp-hcm.html', 'Tin tức bất động sản TP.HCM', lambda R: lst(R, [n for n in NEWS if n['city']=='TP.HCM'], 'Bất động sản TP.HCM'), 'tin')
    for n in NEWS:
        def body(R, n=n):
            rel = [x for x in NEWS if x['id']!=n['id'] and x['cat']==n['cat']][:4]
            return f'''<div class="container art-wrap"><article class="art">{crumbs(R,[('Tin tức','tin-tuc.html'),(n['cat'],None)])}<h1>{E(n['t'])}</h1><p class="meta">{n['date']} · Tác giả: {E(n['author'])} · {E(n['cat'])}</p>
<p class="lead">{E(n['t'])}. Bài viết mẫu tổng hợp diễn biến thị trường {E(n['city'])} trong tháng 10/2026.</p><figure><img src="{img(n['img'],R)}" alt="Ảnh minh họa" width="800" height="600"><figcaption>Ảnh minh họa (Wikimedia Commons).</figcaption></figure>
<h2>Diễn biến chính</h2>{para(n['id']*7, 'Thị trường '+n['city'], 3)}<h2>Góc nhìn chuyên gia</h2>{para(n['id']*11, 'Phân khúc nhà ở', 2)}<blockquote>“Người mua nên ưu tiên sản phẩm có pháp lý rõ ràng và khả năng trả nợ bền vững.” – chuyên gia (nhân vật minh họa)</blockquote><h2>Khuyến nghị</h2>{para(n['id']*13, 'Người mua để ở', 2)}
<div class="share-row"><button class="btn btn-sm" data-share>{ic('share')}Chia sẻ</button></div><p class="note">Nội dung do NhàĐất Việt soạn làm dữ liệu mẫu, không phải tin thật.</p></article><aside class="art-side"><h2>Bài viết liên quan</h2>{''.join(ncard(x,R) for x in rel)}<a class="btn btn-blk" href="{R}tin-tuc.html">Xem tất cả tin tức</a></aside></div>'''
        page(f"tin-tuc/{n['slug']}.html", n['t'], body, 'tin')

def wnav(R, cur=None): return '<nav class="subnav" aria-label="Wiki BĐS"><div class="container">' + f'<a href="{R}wiki.html"{" class=on" if cur is None else ""}>Tất cả</a>' + ''.join(f'<a href="{R}wiki/{s}.html"{" class=on" if s==cur else ""}>{t}</a>' for s,t in WIKI_CATS) + '</div></nav>'
def wcard(w, R): return f'<article class="nc"><a class="th" href="{R}wiki/{w["cat"]}/{w["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="{img(w["img"],R)}" alt="" loading="lazy" width="400" height="260"></a><div><p class="meta">{w["catn"]} · {w["date"]}</p><h3><a href="{R}wiki/{w["cat"]}/{w["slug"]}.html">{E(w["t"])}</a></h3></div></article>'
def wiki_pages():
    def home_(R):
        secs = ''.join(f'<section><div class="sec-h"><h2>{t}</h2><a href="{R}wiki/{s}.html">Xem thêm {ic("chev")}</a></div><div class="grid4">{"".join(wcard(w,R) for w in WIKI if w["cat"]==s)}</div></section>' for s,t in WIKI_CATS)
        return wnav(R) + f'<div class="container"><div class="hero-s"><h1>Wiki BĐS</h1><p>Cẩm nang mua bán, đầu tư, thuê và cho thuê bất động sản (nội dung mẫu).</p><form class="sbar-f sbar-c" action="{R}tim-kiem.html"><label class="sr" for="wq">Tìm bài viết</label><span class="sbar-in">{ic("search")}<input id="wq" name="q" placeholder="Tìm kiến thức BĐS"></span><input type="hidden" name="scope" value="wiki"><button class="btn btn-red">Tìm</button></form></div>{secs}</div>'
    page('wiki.html', 'Wiki BĐS – Cẩm nang mua bán, đầu tư, thuê nhà', home_, 'wiki')
    for s, t in WIKI_CATS:
        items = [w for w in WIKI if w['cat']==s]
        page(f'wiki/{s}.html', f'{t} – Wiki BĐS', lambda R, s=s, t=t, items=items: wnav(R, s) + f'<div class="container">{crumbs(R,[("Wiki BĐS","wiki.html"),(t,None)])}<h1>{t}</h1><div class="grid3">{"".join(wcard(w,R) for w in items)}</div></div>', 'wiki')
        for w in items:
            def body(R, w=w, items=items):
                toc = ['Khái niệm', 'Những điều cần lưu ý', 'Các bước thực hiện', 'Câu hỏi thường gặp']
                return wnav(R, w['cat']) + f'''<div class="container art-wrap"><article class="art">{crumbs(R,[('Wiki BĐS','wiki.html'),(w['catn'],f"wiki/{w['cat']}.html"),(w['t'],None)])}<h1>{E(w['t'])}</h1><p class="meta">{w['date']} · {w['catn']}</p>
<nav class="toc" aria-label="Mục lục"><b>Mục lục</b><ol>{''.join(f'<li><a href="#m{i}">{x}</a></li>' for i,x in enumerate(toc))}</ol></nav><figure><img src="{img(w['img'],R)}" alt="Ảnh minh họa" width="800" height="600"></figure>
{''.join(f'<h2 id="m{i}">{x}</h2>' + para(w['id']*17+i, w['t'], 2) for i,x in enumerate(toc[:3]))}<ol class="steps">{''.join(f'<li>{x}</li>' for x in ['Xác định nhu cầu và ngân sách','Khảo sát khu vực, so sánh giá','Kiểm tra pháp lý, quy hoạch','Đàm phán, đặt cọc có hợp đồng','Công chứng, sang tên, nộp thuế phí'])}</ol>
<h2 id="m3">Câu hỏi thường gặp</h2><details><summary>Bài viết này có giá trị pháp lý không?</summary><p>Không. Đây là nội dung mẫu, hãy tham khảo luật sư hoặc cơ quan có thẩm quyền.</p></details></article>
<aside class="art-side"><h2>Cùng chuyên mục</h2>{''.join(wcard(x,R) for x in items if x['id']!=w['id'])}</aside></div>'''
            page(f"wiki/{w['cat']}/{w['slug']}.html", w['t'], body, 'wiki')
