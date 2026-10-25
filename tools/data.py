# Dữ liệu mẫu (DEMO) cho NhàĐất Việt — sinh tất định, không phải tin thật
import random, unicodedata, re
R = random.Random(2026)
def slug(s):
    s = s.replace('đ','d').replace('Đ','D')
    s = unicodedata.normalize('NFD', s); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

CITIES = {  # tên: (slug, lat, lng, [quận...])
 "Hà Nội": ("ha-noi",21.028,105.834,["Cầu Giấy","Đống Đa","Tây Hồ","Thanh Xuân","Nam Từ Liêm","Long Biên","Hoàng Mai","Hà Đông","Gia Lâm"]),
 "TP.HCM": ("tp-hcm",10.776,106.700,["Quận 1","Quận 7","Thủ Đức","Bình Thạnh","Phú Nhuận","Gò Vấp","Tân Bình","Bình Chánh"]),
 "Đà Nẵng": ("da-nang",16.054,108.202,["Hải Châu","Sơn Trà","Ngũ Hành Sơn","Thanh Khê","Liên Chiểu"]),
 "Hải Phòng": ("hai-phong",20.845,106.688,["Lê Chân","Ngô Quyền","Hồng Bàng"]),
 "Bình Dương": ("binh-duong",10.980,106.651,["Thủ Dầu Một","Dĩ An","Thuận An"]),
 "Khánh Hòa": ("khanh-hoa",12.238,109.196,["Nha Trang","Cam Ranh"]),
 "Đồng Nai": ("dong-nai",10.945,106.824,["Biên Hòa","Nhơn Trạch"]),
 "Quảng Ninh": ("quang-ninh",20.951,107.080,["Hạ Long","Cẩm Phả"]),
}
def dslug(d, city):
    s = slug(d)
    return s if s not in ('quan-1','quan-7') else s + '-' + CITIES[city][0]  # quan-1-tp-hcm

BAN = [("can-ho-chung-cu","căn hộ chung cư",30),("can-ho-chung-cu-mini","chung cư mini, căn hộ dịch vụ",6),("nha-rieng","nhà riêng",22),
 ("nha-biet-thu-lien-ke","nhà biệt thự, liền kề",8),("nha-mat-pho","nhà mặt phố",10),("shophouse-nha-pho-thuong-mai","shophouse, nhà phố thương mại",4),
 ("dat-nen-du-an","đất nền dự án",7),("dat","đất",10),("trang-trai-khu-nghi-duong","trang trại, khu nghỉ dưỡng",2),("condotel","condotel",3),
 ("kho-nha-xuong","kho, nhà xưởng",3),("loai-bat-dong-san-khac","loại bất động sản khác",2)]
THUE = [("can-ho-chung-cu","căn hộ chung cư",26),("can-ho-chung-cu-mini","chung cư mini, căn hộ dịch vụ",10),("nha-rieng","nhà riêng",14),
 ("nha-biet-thu-lien-ke","nhà biệt thự, liền kề",4),("nha-mat-pho","nhà mặt phố",8),("shophouse-nha-pho-thuong-mai","shophouse, nhà phố thương mại",3),
 ("nha-tro-phong-tro","nhà trọ, phòng trọ",12),("van-phong","văn phòng",10),("sang-nhuong-cua-hang-ki-ot","cửa hàng, ki ốt",5),
 ("kho-nha-xuong-dat","kho, nhà xưởng, đất",4),("loai-bat-dong-san-khac","loại bất động sản khác",2)]
PROJ_TYPES = [("can-ho-chung-cu","Căn hộ chung cư"),("cao-oc-van-phong","Cao ốc văn phòng"),("trung-tam-thuong-mai","Trung tâm thương mại"),
 ("khu-do-thi-moi","Khu đô thị mới"),("khu-phuc-hop","Khu phức hợp"),("nha-o-xa-hoi","Nhà ở xã hội"),("khu-nghi-duong-sinh-thai","Khu nghỉ dưỡng, Sinh thái"),
 ("khu-cong-nghiep","Khu công nghiệp"),("biet-thu-lien-ke","Biệt thự, liền kề"),("shophouse","Shophouse"),("nha-mat-pho","Nhà mặt phố"),("khac","Dự án khác")]
WIKI_CATS = [("mua-bds","Mua BĐS"),("ban-bds","Bán BĐS"),("thue-bds","Thuê BĐS"),("tai-chinh","Tài chính BĐS"),("quy-hoach-phap-ly","Quy hoạch - Pháp lý"),("noi-ngoai-that","Nội - Ngoại thất"),("phong-tuc","Phong tục")]
DIRS = ["Đông","Tây","Nam","Bắc","Đông Nam","Đông Bắc","Tây Nam","Tây Bắc"]
IMG_N = 47
# ảnh theo nhóm (chỉ số file r#.jpg trong img/)
EXT = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,37,38,39,40,41,42,43,44,45,46,47]
INT = [15,16,17,18,19,20,21,22,23,24,25,26,27,28,36]
POOL = [29,30,31,32,33,34,35]
STREETS = ["Trần Duy Hưng","Nguyễn Văn Cừ","Lê Văn Lương","Phạm Hùng","Nguyễn Hữu Thọ","Võ Văn Kiệt","Hoàng Quốc Việt","Lạc Long Quân","Nguyễn Trãi","Điện Biên Phủ","Lê Lợi","Hai Bà Trưng","Bạch Đằng","Phan Chu Trinh","Nguyễn Văn Linh","Trường Chinh"]
AGENTS = [f"{a} {b}" for a,b in zip(["Nguyễn Văn","Trần Thị","Lê Minh","Phạm Thu","Hoàng Quốc","Vũ Thị","Đặng Hữu","Bùi Ngọc","Đỗ Mạnh","Hồ Thanh","Ngô Phương","Dương Tuấn","Lý Hải","Mai Anh","Tạ Quang","Phan Bảo","Trịnh Gia","Cao Hà","Lâm Khánh","Kiều Minh","Châu Ngọc","Hà Văn","Tôn Nữ","Quách Đức"],["An","Bình","Cường","Dung","Em","Giang","Hiếu","Hương","Khoa","Lan","Linh","Long","Mai","Nam","Ngân","Phúc","Quân","Sơn","Tâm","Thảo","Trang","Tuấn","Uyên","Vinh"])]
COMPANIES = ["Công ty TNHH BĐS Sao Việt","Công ty CP Địa ốc Phương Nam","Công ty CP BĐS Hòa Bình Land","Công ty TNHH Nhà Xanh","Công ty CP Đầu tư An Cư","Công ty CP Địa ốc Thịnh Phát","Công ty TNHH Môi giới Tâm An","Công ty CP BĐS Biển Đông","Công ty CP Phát triển Đô thị Sông Hồng","Công ty TNHH Bất động sản Kim Long","Công ty CP Đầu tư Hưng Thịnh Phú","Công ty TNHH Dịch vụ Nhà Việt","Công ty CP Địa ốc Miền Trung","Công ty CP BĐS Ánh Dương","Công ty TNHH Đất Lành","Công ty CP Tập đoàn Đông Á Land"]

def pick_place():
    c = R.choices(list(CITIES), weights=[30,30,10,6,8,6,5,5])[0]
    return c, R.choice(CITIES[c][3])

def price_for(mode, ts, city, area):
    mult = {"Hà Nội":1.0,"TP.HCM":1.05,"Đà Nẵng":.7,"Hải Phòng":.55,"Bình Dương":.45,"Khánh Hòa":.6,"Đồng Nai":.4,"Quảng Ninh":.45}[city]
    if mode=="ban":
        ppm = {"can-ho-chung-cu":65,"can-ho-chung-cu-mini":45,"nha-rieng":120,"nha-biet-thu-lien-ke":150,"nha-mat-pho":280,"shophouse-nha-pho-thuong-mai":170,
               "dat-nen-du-an":55,"dat":60,"trang-trai-khu-nghi-duong":4,"condotel":50,"kho-nha-xuong":12,"loai-bat-dong-san-khac":30}[ts]
        return round(area*ppm*mult*R.uniform(.8,1.25)*1e6, -7)
    pm = {"can-ho-chung-cu":.2,"can-ho-chung-cu-mini":.17,"nha-rieng":.18,"nha-biet-thu-lien-ke":.25,"nha-mat-pho":.5,"shophouse-nha-pho-thuong-mai":.4,
          "nha-tro-phong-tro":.15,"van-phong":.35,"sang-nhuong-cua-hang-ki-ot":.4,"kho-nha-xuong-dat":.08,"loai-bat-dong-san-khac":.1}[ts]
    return round(area*pm*mult*R.uniform(.8,1.3)*1e6, -5)

AREA = {"can-ho-chung-cu":(35,130),"can-ho-chung-cu-mini":(25,60),"nha-rieng":(30,90),"nha-biet-thu-lien-ke":(90,350),"nha-mat-pho":(50,200),
 "shophouse-nha-pho-thuong-mai":(75,180),"dat-nen-du-an":(70,200),"dat":(50,300),"trang-trai-khu-nghi-duong":(1000,8000),"condotel":(30,70),
 "kho-nha-xuong":(300,3000),"loai-bat-dong-san-khac":(40,400),"nha-tro-phong-tro":(15,35),"van-phong":(40,400),"sang-nhuong-cua-hang-ki-ot":(15,80),"kho-nha-xuong-dat":(200,3000)}
TITLE = {
 "can-ho-chung-cu":["Bán căn hộ {b}PN tầng trung, view thoáng, sổ hồng lâu dài","Căn góc {b}PN full nội thất, ban công Đông Nam","Chính chủ cần bán gấp căn {b}PN gần {s}"],
 "can-ho-chung-cu-mini":["Chung cư mini {b}PN gần {s}, sổ riêng từng căn","Căn hộ dịch vụ {b}PN đang cho thuê ổn định"],
 "nha-rieng":["Nhà {f} tầng ngõ ô tô gần {s}, sổ đỏ chính chủ","Nhà riêng {f} tầng, {b}PN, ngõ thông, gần chợ và trường","Bán nhà hẻm xe hơi {f} tầng, hoàn công đủ"],
 "nha-biet-thu-lien-ke":["Biệt thự song lập sân vườn rộng, khu compound","Liền kề {f} tầng mặt đường nội khu, đã hoàn thiện"],
 "nha-mat-pho":["Nhà mặt phố {s}, mặt tiền rộng, kinh doanh sầm uất","Mặt tiền {s} {f} tầng, đang cho thuê dòng tiền tốt"],
 "shophouse-nha-pho-thuong-mai":["Shophouse khối đế {f} tầng, mặt đường lớn","Nhà phố thương mại vị trí góc, tiện kinh doanh"],
 "dat-nen-du-an":["Đất nền dự án đã có sổ, hạ tầng hoàn chỉnh","Lô góc đất nền gần trục {s}, giá đầu tư"],
 "dat":["Đất thổ cư mặt tiền 5m, ngõ thông ô tô","Bán lô đất vuông vắn gần {s}, sổ đỏ riêng"],
 "trang-trai-khu-nghi-duong":["Trang trại view hồ, phù hợp làm nghỉ dưỡng","Khu nghỉ dưỡng mini đang hoạt động, chuyển nhượng"],
 "condotel":["Condotel view biển, cam kết lợi nhuận cho thuê","Căn condotel full nội thất, vận hành bởi đơn vị quốc tế"],
 "kho-nha-xuong":["Kho xưởng xe container ra vào, đủ PCCC","Nhà xưởng trong cụm công nghiệp, điện 3 pha"],
 "loai-bat-dong-san-khac":["Mặt bằng đa năng phù hợp nhiều mô hình","Bất động sản đặc thù, pháp lý đầy đủ"],
 "nha-tro-phong-tro":["Phòng trọ khép kín có gác, giờ tự do gần {s}","Phòng mới xây, có điều hòa, nóng lạnh, ban công"],
 "van-phong":["Văn phòng hạng B gần {s}, giá trọn gói","Sàn văn phòng thông sàn, có thang máy, chỗ để xe"],
 "sang-nhuong-cua-hang-ki-ot":["Sang nhượng cửa hàng mặt phố đang kinh doanh tốt","Cho thuê ki ốt mặt đường {s}"],
 "kho-nha-xuong-dat":["Cho thuê kho xưởng xe container ra vào","Cho thuê đất trống làm bãi xe, kho bãi"],
}
LISTINGS = []
def gen_listings():
    i = 0
    for mode, types in (("ban",BAN),("thue",THUE)):
        for ts, tn, w in types:
            for k in range(w*2 if mode=="ban" else w*2):
                i += 1
                city, dist = pick_place()
                a0,a1 = AREA[ts]; area = round(R.uniform(a0,a1))
                beds = 0 if ts in ("dat","dat-nen-du-an","kho-nha-xuong","kho-nha-xuong-dat","van-phong","trang-trai-khu-nghi-duong","sang-nhuong-cua-hang-ki-ot") else max(1,min(6,area//28 if 'can-ho' in ts else R.randint(2,6)))
                if ts=="nha-tro-phong-tro": beds=1
                st = R.choice(STREETS); f = R.randint(2,6)
                title = R.choice(TITLE[ts]).format(b=beds,s=st,f=f)
                if mode=="thue" and not title.lower().startswith(("cho thuê","sang")): title = "Cho thuê " + title[0].lower()+title[1:]
                cs = CITIES[city]
                lat = cs[1] + (cs[3].index(dist)-len(cs[3])/2)*0.012 + R.uniform(-.01,.01); lng = cs[2] + ((cs[3].index(dist)*7)%5-2)*0.012 + R.uniform(-.01,.01)
                pool = INT if 'can-ho' in ts or ts in ('van-phong','condotel','nha-tro-phong-tro') else (POOL+EXT if ts in('nha-biet-thu-lien-ke','trang-trai-khu-nghi-duong') else EXT)
                imgs = [R.choice(pool)] + R.sample(EXT+INT, 5)
                LISTINGS.append(dict(id=i, mode=mode, ts=ts, tn=tn, city=city, dist=dist, street=st, title=title, area=area, beds=beds, baths=max(1,min(beds,4)),
                    floors=f if 'nha' in ts else 0, dir=R.choice(DIRS), price=price_for(mode,ts,city,area), lat=round(lat,5), lng=round(lng,5), img=imgs,
                    vip=R.choices(["kimcuong","vang","bac","thuong"],[1,2,3,8])[0], verified=R.random()<.4, agent=R.randrange(len(AGENTS)),
                    day=R.randint(0,13), legal=R.choice(["Sổ đỏ/Sổ hồng","Hợp đồng mua bán","Đang chờ sổ"]) if mode=="ban" else "Hợp đồng thuê",
                    furn=R.choice(["Đầy đủ","Cơ bản","Không nội thất"])))
gen_listings()

PROJ_NAMES = ["Sông Xanh Riverside","Ánh Dương Residence","Biển Ngọc Ocean","Lotus Garden","Hoa Sen Tower","Phú Mỹ Park","An Khang Center","Sky Garden Plaza","Green Valley Home","Hồ Tây Lake View","The Horizon Place","Minh Châu Eco City","Kim Long Bay","Thăng Long Heights","Sài Gòn Pearl Park","Vườn Đào Villa","Cầu Giấy Central","Saigon South Bay","Hải Châu Tower","Nha Trang Seaview","Thủ Đức Park City","Long Biên Garden","Gia Lâm Smart City","Dĩ An Green","Hạ Long Marina","Biên Hòa Universe","Tây Hồ Residence","Quận 7 Sky Linked","Sơn Trà Ocean Villas","Hà Đông Starlight","Bình Thạnh Grand","Hồng Bàng Plaza","Cam Ranh Bay Resort","Nhơn Trạch Riverside","Thuận An Central Park","Đống Đa Premier"]
PROJECTS = []
for i,n in enumerate(PROJ_NAMES):
    city = list(CITIES)[[0,0,2,1,0,1,4,1,0,0,1,0,5,0,1,0,0,1,2,5,1,0,0,4,7,6,0,1,2,0,1,3,5,6,4,0][i]]
    dist = CITIES[city][3][i % len(CITIES[city][3])]
    pt = PROJ_TYPES[[0,0,6,3,0,3,4,0,8,0,0,3,6,0,4,8,1,3,0,6,3,0,3,5,6,3,0,0,6,0,0,2,6,3,4,0][i]]
    PROJECTS.append(dict(id=i+1, name=n, slug=slug(n), city=city, dist=dist, pt=pt, status=["Đang mở bán","Sắp mở bán","Đã bàn giao"][i%3],
        ha=round(R.uniform(1.2,120),1), units=R.randint(300,4500), price=round(R.uniform(35,120)), dev=COMPANIES[i%len(COMPANIES)], img=[R.choice(EXT)]+R.sample(EXT+INT+POOL,5),
        year=2024+i%4, lat=CITIES[city][1]+R.uniform(-.04,.04), lng=CITIES[city][2]+R.uniform(-.04,.04)))

NEWS_T = ["Thị trường căn hộ quý IV/2026: nguồn cung mới tăng mạnh tại hai đầu cầu","Giá chung cư Hà Nội hạ nhiệt sau giai đoạn tăng nóng","TP.HCM: nhà phố trung tâm hút khách mua để ở thực","Lãi suất vay mua nhà giảm nhẹ, người mua lần đầu hưởng lợi","Đà Nẵng: phân khúc căn hộ ven biển sôi động trở lại","Hạ tầng giao thông vành đai thúc đẩy đất nền vùng ven","Nhà ở xã hội: thêm nhiều dự án được khởi công trong năm","Thị trường cho thuê văn phòng ổn định, tỷ lệ lấp đầy cao","Bình Dương đón làn sóng dịch chuyển dân cư từ TP.HCM","Luật Đất đai mới: những thay đổi người mua cần biết","Khu đô thị vệ tinh: xu hướng an cư của gia đình trẻ","Condotel và bài toán pháp lý: góc nhìn sau 5 năm","Giá thuê phòng trọ quanh các trường đại học tăng nhẹ","Thị trường nhà phố Hải Phòng nhờ cầu cảng và công nghiệp","Người mua ưu tiên dự án có pháp lý minh bạch, tiến độ rõ ràng","Nguồn cung biệt thự, liền kề phía Tây Hà Nội tăng","Đất nền Đồng Nai: kỳ vọng từ sân bay Long Thành","Khánh Hòa: căn hộ nghỉ dưỡng phục hồi theo du lịch"]
NEWS = []
for i in range(36):
    city = ["Hà Nội","TP.HCM"][i%2] if i%3 else R.choice(list(CITIES))
    NEWS.append(dict(id=i+1, t=NEWS_T[i%18] + ("" if i<18 else f" – cập nhật tháng {10-i%9}/2026"), cat="Bất động sản Hà Nội" if city=="Hà Nội" else ("Bất động sản TP.HCM" if city=="TP.HCM" else "Tin thị trường"),
        city=city, date=f"{26-(i%25):02d}/10/2026" if i<25 else f"{28-(i-25)*2:02d}/09/2026", img=R.choice(EXT), author=R.choice(["Ban Biên tập","Minh Anh","Quốc Huy","Thanh Hà"])))
for n in NEWS: n['slug'] = slug(n['t']) + f"-{n['id']}"
for p in PROJECTS: p['slug'] = p['slug'] + f"-{p['id']}"

WIKI_T = {
 "mua-bds":["Quy trình mua nhà lần đầu từ A đến Z","Kinh nghiệm xem nhà trước khi đặt cọc","Mua chung cư cũ cần kiểm tra những gì","Có nên mua nhà khi lãi suất đang thấp"],
 "ban-bds":["Định giá nhà trước khi rao bán","Cách viết tin đăng bán nhà hiệu quả","Thuế và phí khi bán nhà đất","Chụp ảnh bất động sản đẹp bằng điện thoại"],
 "thue-bds":["Hợp đồng thuê nhà cần những điều khoản gì","Kinh nghiệm thuê phòng trọ cho sinh viên","Thuê văn phòng: chọn hạng A, B hay C","Quyền và nghĩa vụ của bên thuê nhà"],
 "tai-chinh":["Cách tính khoản vay mua nhà phù hợp thu nhập","Dư nợ giảm dần và trả góp đều: khác nhau thế nào","Lãi suất thả nổi là gì","Chuẩn bị hồ sơ vay ngân hàng mua nhà"],
 "quy-hoach-phap-ly":["Quy hoạch chi tiết là gì và cách tra cứu","Sổ đỏ và sổ hồng khác nhau ra sao","Thủ tục sang tên sổ đỏ mới nhất","Đất thổ cư là gì, có những loại nào"],
 "noi-ngoai-that":["Bố trí phòng khách nhỏ cho căn hộ 2PN","Chọn sàn gỗ hay sàn gạch cho nhà phố","Ý tưởng ban công xanh cho chung cư","Màu sơn ngoại thất bền đẹp với khí hậu nóng ẩm"],
 "phong-tuc":["Thủ tục nhập trạch về nhà mới","Xem hướng nhà theo tuổi: hiểu đúng để không lo lắng","Lễ động thổ cần chuẩn bị gì","Phong tục cúng tân gia ở ba miền"],
}
WIKI = []
for cs, cn in WIKI_CATS:
    for t in WIKI_T[cs]:
        WIKI.append(dict(id=len(WIKI)+1, cat=cs, catn=cn, t=t, slug=slug(t), img=R.choice(EXT+INT), date=f"{R.randint(1,28):02d}/{R.randint(5,10):02d}/2026"))

REPORTS = []
for c in CITIES:
    REPORTS.append(dict(kind="bieu-do-gia", t=f"Biến động giá bất động sản {c} 24 tháng qua", city=c))
for t in ["Thị trường BĐS quý 3/2026: giá hạ nhiệt, chung cư dẫn dắt","Nguồn cung căn hộ mới tại TP.HCM có cải thiện?","Đất nền vùng ven: khi nào nên xuống tiền","Văn phòng hạng B và xu hướng làm việc linh hoạt","Nhà ở xã hội: nút thắt và cơ hội","Nhà đầu tư cá nhân nên làm gì cuối năm 2026"]:
    REPORTS.append(dict(kind="goc-nhin-chuyen-gia", t=t, city=R.choice(["Hà Nội","TP.HCM"])))
for r in REPORTS: r['slug'] = slug(r['t']); r['img'] = R.choice(EXT)
VIDEOS = [dict(t=t, img=R.choice(EXT+POOL), dur=f"{R.randint(2,14)}:{R.randint(10,59)}") for t in ["Review khu Thủ Thiêm sau 5 năm","Đi xem căn hộ 2PN dưới 3 tỷ ở Hà Nội","Đánh giá hạ tầng phía Đông Hà Nội","Có nên mua đất nền Đồng Nai","Một vòng Sơn Trà, Đà Nẵng","Căn hộ studio: tối ưu 30m²","Biệt thự ven sông Quận 7","Nhà phố Hải Phòng có đắt?"]]

BROKERS = [dict(id=i+1, name=AGENTS[i], city=list(CITIES)[i%8], phone=f"09{(13572468+i*3141593)%100000000:08d}", years=1+i%12, company=COMPANIES[i%16]) for i in range(len(AGENTS))]
COMPS = [dict(id=i+1, name=n, slug=slug(n), city=list(CITIES)[i%8], addr=f"{R.randint(1,300)} {R.choice(STREETS)}, {CITIES[list(CITIES)[i%8]][3][0]}, {list(CITIES)[i%8]}", phone=f"02{(87654321+i*2718281)%100000000:08d}", founded=2005+i%15) for i,n in enumerate(COMPANIES)]
