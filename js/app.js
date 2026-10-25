/* NhàĐất Việt – app.js (demo, không backend). Dữ liệu người dùng chỉ lưu localStorage */
(function(){
'use strict';
var R=window.ROOT||'',$=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var LS={get:function(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}},set:function(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function money(p,m){p=+p;if(m==='thue'){return p>=1e6?(Math.round(p/1e5)/10).toString().replace('.',',')+' triệu/tháng':'Thỏa thuận'}return p>=1e9?(Math.round(p/1e7)/100).toString().replace('.',',')+' tỷ':(Math.round(p/1e6))+' triệu'}
var toastT;function toast(m){var t=$('#toast');if(!t)return;t.textContent=m;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('show')},2600)}
window.NDtoast=toast;
/* app bar */
if(LS.get('nd_ab',0))$('#appbar')&&$('#appbar').classList.add('hide');
document.addEventListener('click',function(e){var b=e.target.closest('[data-close-appbar]');if(b){$('#appbar').classList.add('hide');LS.set('nd_ab',1)}});
/* menu drawer */
var mb=$('[data-menu]'),nw=$('#navWrap');
if(mb&&nw){mb.addEventListener('click',function(){nw.style.top=Math.max(0,document.querySelector('.hdr').getBoundingClientRect().bottom)+'px';var o=nw.classList.toggle('open');mb.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''});
 document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nw.classList.contains('open')){nw.classList.remove('open');mb.setAttribute('aria-expanded','false');document.body.style.overflow='';mb.focus()}})}
$$('.nv-t').forEach(function(b){b.addEventListener('click',function(){var li=b.closest('.nv'),o=li.classList.toggle('open');b.setAttribute('aria-expanded',o)})});
$$('.nv').forEach(function(li){li.addEventListener('keydown',function(e){if(e.key==='Escape'){li.classList.remove('open');var a=$('.nv-a',li);a&&a.focus();if(document.activeElement)document.activeElement.blur&&a.focus()}})});
/* favourites */
var favs=LS.get('nd_favs',[]);
function syncFav(){$$('[data-fav]').forEach(function(b){var on=favs.indexOf(+b.dataset.fav)>-1;b.setAttribute('aria-pressed',on);b.setAttribute('aria-label',on?'Bỏ lưu tin':'Lưu tin')});var c=$('#favCount');if(c){c.textContent=favs.length;c.hidden=!favs.length}}
document.addEventListener('click',function(e){var b=e.target.closest('[data-fav]');if(!b)return;e.preventDefault();var id=+b.dataset.fav,i=favs.indexOf(id);if(i>-1){favs.splice(i,1);toast('Đã bỏ lưu tin')}else{favs.push(id);toast('Đã lưu tin – xem ở "Tin đã lưu"')}LS.set('nd_favs',favs);syncFav();if($('#savedList'))renderSaved()});
syncFav();
/* phone reveal */
document.addEventListener('click',function(e){var b=e.target.closest('[data-phone]');if(!b)return;var s=$('span',b)||b;if(b.dataset.shown){location.href='tel:'+b.dataset.phone.replace(/\s/g,'');return}s.textContent=b.dataset.phone;b.dataset.shown=1;toast('Số điện thoại mẫu (demo)')});
/* share */
document.addEventListener('click',function(e){var b=e.target.closest('[data-share]');if(!b)return;var u=location.href;if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){toast('Đã sao chép liên kết')})}else toast(u)});
/* demo forms */
document.addEventListener('submit',function(e){var f=e.target;if(f.matches('[data-demo-form]')){e.preventDefault();if(!f.checkValidity()){f.reportValidity();return}toast(f.dataset.demoForm||'Đã gửi (demo)');f.reset()}});
/* select navigate */
$$('select[data-nav]').forEach(function(s){s.addEventListener('change',function(){if(s.value)location.href=s.value})});
/* modal helper */
var lastFocus;
function modal(html,cls){closeModal();lastFocus=document.activeElement;var m=document.createElement('div');m.className='modal';m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');m.innerHTML='<div class="modal-in '+(cls||'')+'"><button class="hbtn modal-x" aria-label="Đóng" data-x><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6 6 18"/></svg></button>'+html+'</div>';document.body.appendChild(m);document.body.style.overflow='hidden';m.addEventListener('click',function(e){if(e.target===m||e.target.closest('[data-x]'))closeModal()});var f=m.querySelector('input,button:not([data-x]),a');(f||m.querySelector('[data-x]')).focus();return m}
function closeModal(){var m=$('.modal');if(m){m.remove();document.body.style.overflow='';lastFocus&&lastFocus.focus&&lastFocus.focus()}}
document.addEventListener('keydown',function(e){var m=$('.modal');if(!m)return;if(e.key==='Escape')closeModal();if(e.key==='Tab'){var f=$$('a,button,input,select,textarea',m).filter(function(x){return!x.disabled&&x.offsetParent});if(!f.length)return;if(e.shiftKey&&document.activeElement===f[0]){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&document.activeElement===f[f.length-1]){e.preventDefault();f[0].focus()}}});
/* auth */
function user(){return LS.get('nd_user',null)}
function renderAcct(){var a=$('#acct'),u=user();if(!a)return;if(u){a.innerHTML='<a class="hbtn user-chip" href="'+R+'trang-ca-nhan.html"><span class="av" aria-hidden="true">'+esc((u.name||'U').trim().split(' ').pop()[0])+'</span>'+esc(u.name)+'</a>';$$('.nv-mob [data-auth]').forEach(function(x){x.parentNode.hidden=true})}}
renderAcct();
function authForm(kind){return kind==='register'?'<form class="ctf" data-auth-form="register"><label>Họ tên<input name="n" required autocomplete="name"></label><label>Số điện thoại hoặc email<input name="u" required autocomplete="username"></label><label>Mật khẩu (tối thiểu 6 ký tự)<input name="p" type="password" required minlength="6" autocomplete="new-password"></label><button class="btn btn-red btn-blk">Đăng ký</button><p class="muted">Đã có tài khoản? <a href="'+R+'dang-nhap.html" data-auth="login" class="red">Đăng nhập</a></p></form>':'<form class="ctf" data-auth-form="login"><label>Số điện thoại hoặc email<input name="u" required autocomplete="username"></label><label>Mật khẩu<input name="p" type="password" required minlength="6" autocomplete="current-password"></label><div class="row-sb"><label class="tgl"><input type="checkbox" checked> Nhớ tài khoản</label><a href="'+R+'quen-mat-khau.html" class="red">Quên mật khẩu?</a></div><button class="btn btn-red btn-blk">Đăng nhập</button><p class="muted">Chưa có tài khoản? <a href="'+R+'dang-ky.html" data-auth="register" class="red">Đăng ký tại đây</a></p></form>'}
document.addEventListener('click',function(e){var a=e.target.closest('[data-auth]');if(!a||e.ctrlKey||e.metaKey)return;if(/dang-(nhap|ky)\.html$/.test(location.pathname))return;e.preventDefault();var k=a.dataset.auth;if(nw&&nw.classList.contains('open'))mb.click();modal('<p class="muted" style="margin:0">Xin chào bạn</p><h2 style="margin:4px 0 16px">'+(k==='register'?'Đăng ký tài khoản mới':'Đăng nhập để tiếp tục')+'</h2>'+authForm(k)+'<p class="note">Demo: không có máy chủ, tài khoản chỉ lưu trong trình duyệt. Đừng nhập mật khẩu thật.</p>')});
document.addEventListener('submit',function(e){var f=e.target;if(!f.matches('[data-auth-form]'))return;e.preventDefault();if(!f.checkValidity()){f.reportValidity();return}var u=f.u.value.trim(),n=f.n?f.n.value.trim():(LS.get('nd_user_name',u.split('@')[0]));LS.set('nd_user',{name:n,u:u});if(f.n)LS.set('nd_user_name',n);closeModal();toast('Đăng nhập thành công (demo)');renderAcct();if(/dang-(nhap|ky)\.html$/.test(location.pathname))setTimeout(function(){location.href=R+'trang-ca-nhan.html'},500)});
document.addEventListener('click',function(e){if(e.target.closest('[data-logout]')){localStorage.removeItem('nd_user');toast('Đã đăng xuất');setTimeout(function(){location.href=R+'index.html'},500)}});
/* gallery lightbox */
$$('[data-gallery]').forEach(function(g){var src=$('[data-gallery-src]');var list=src?JSON.parse(src.textContent):$$('img',g).map(function(i){return i.src});
 g.addEventListener('click',function(e){var b=e.target.closest('[data-open]');if(!b)return;var i=+b.dataset.open;var m=modal('<img alt="Ảnh tin đăng"><div class="lb-nav"><button class="hbtn" data-p aria-label="Ảnh trước">‹ Trước</button><span aria-live="polite"></span><button class="hbtn" data-n aria-label="Ảnh sau">Sau ›</button></div>','wide');
  function show(){i=(i+list.length)%list.length;$('img',m).src=list[i];$('.lb-nav span',m).textContent=(i+1)+' / '+list.length}show();
  $('[data-p]',m).onclick=function(){i--;show()};$('[data-n]',m).onclick=function(){i++;show()};m.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){i--;show()}if(e.key==='ArrowRight'){i++;show()}})})});
/* carousels */
document.addEventListener('click',function(e){var b=e.target.closest('[data-car]');if(!b)return;var c=document.getElementById(b.dataset.car);if(!c)return;var w=(c.firstElementChild?c.firstElementChild.getBoundingClientRect().width+20:300);c.scrollBy({left:+b.dataset.dir*w*2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})});
/* video dialog */
document.addEventListener('click',function(e){var b=e.target.closest('[data-video]');if(!b)return;var im=$('img',b);modal('<div style="position:relative"><img src="'+(im?im.src:'')+'" alt=""><span class="play" style="pointer-events:none"><svg class="ic" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span></div><p style="color:#fff;padding:12px 16px;margin:0"><b>'+esc(b.dataset.video)+'</b><br><small>Bản demo không có video thật – đây là ảnh minh họa.</small></p>','wide')});
/* listing filters */
var rows=$('#rows');
if(rows){var st={},items=$$('article.lr',rows),sortSel=$('[data-sort]'),ver=$('[data-verified]');
 function apply(){var n=0;items.forEach(function(a){var ok=true;for(var k in st){var v=+a.dataset[k];if(v<st[k][0]||v>=st[k][1])ok=false}if(ver&&ver.checked&&a.dataset.ver!=='1')ok=false;a.hidden=!ok;if(ok)n++});
  var s=sortSel&&sortSel.value;if(s){var arr=items.slice().sort(function(x,y){if(s==='new')return x.dataset.day-y.dataset.day;if(s==='pa')return x.dataset.price-y.dataset.price;if(s==='pd')return y.dataset.price-x.dataset.price;if(s==='aa')return x.dataset.area-y.dataset.area;if(s==='ad')return y.dataset.area-x.dataset.area;return 0});arr.forEach(function(a){rows.appendChild(a)})}
  var nr=$('#noRes');if(nr)nr.hidden=n>0||!items.length}
 $$('[data-k]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.k,on=b.getAttribute('aria-pressed')==='true';$$('[data-k="'+k+'"]').forEach(function(x){x.setAttribute('aria-pressed','false')});if(on)delete st[k];else{st[k]=[+b.dataset.min,+b.dataset.max];b.setAttribute('aria-pressed','true')}apply()})});
 $$('select[data-k-sel]').forEach(function(s){s.addEventListener('change',function(){var k=s.dataset.kSel;if(!s.value)delete st[k];else{var p=s.value.split('-');st[k]=[+p[0],+p[1]]}apply()})});
 sortSel&&sortSel.addEventListener('change',apply);ver&&ver.addEventListener('change',apply);
 $$('[data-reset]').forEach(function(b){b.addEventListener('click',function(){st={};$$('[data-k]').forEach(function(x){x.setAttribute('aria-pressed','false')});if(ver)ver.checked=false;apply()})})}
/* loan */
$$('[data-loan]').forEach(function(f){function calc(){var P=+f.dataset.price*(+f.r.value/100),n=+f.y.value*12,i=+f.i.value/1200;var m=i?P*i/(1-Math.pow(1+i,-n)):P/n;$('.loan-out',f).innerHTML='Vay <b>'+money(P)+'</b> · trả góp khoảng <b class="red">'+(Math.round(m/1e5)/10).toString().replace('.',',')+' triệu/tháng</b> (minh họa)'}f.addEventListener('input',calc);f.addEventListener('submit',function(e){e.preventDefault()});calc()});
/* chart tooltip */
function bindTips(root){$$('.chart',root).forEach(function(c){var t=$('.tip',c);$$('[data-tip]',c).forEach(function(p){function on(){var r=c.getBoundingClientRect(),b=p.getBoundingClientRect();t.textContent=p.dataset.tip;t.hidden=false;t.style.left=Math.max(4,Math.min(b.left-r.left-40,r.width-180))+'px';t.style.top=(b.top-r.top-30)+'px'}p.addEventListener('mouseenter',on);p.addEventListener('click',on);p.addEventListener('mouseleave',function(){t.hidden=true})})})}
bindTips(document);
var sd=$('#seriesData');
if(sd){var D=JSON.parse(sd.textContent),C=['#C4321F','#00807F'];
 function draw(){var names=$$('[data-cmp]').map(function(s){return s.value});var all=names.map(function(n){return D.s[n]}),W=720,h=280,P=48,L=D.labels,flat=[].concat.apply([],all),mn=Math.min.apply(0,flat)*.95,mx=Math.max.apply(0,flat)*1.03;function X(i){return P+i*(W-P-16)/(L.length-1)}function Y(v){return h-32-(v-mn)/(mx-mn)*(h-60)}
  var g='';for(var k=0;k<5;k++){var v=mn+(mx-mn)*k/4;g+='<line x1="'+P+'" x2="'+(W-16)+'" y1="'+Y(v)+'" y2="'+Y(v)+'" stroke="#EEE"/><text x="'+(P-6)+'" y="'+(Y(v)+4)+'" text-anchor="end" font-size="11" fill="#555">'+v.toFixed(0)+'</text>'}
  for(var i=0;i<L.length;i+=4)g+='<text x="'+X(i)+'" y="'+(h-10)+'" text-anchor="middle" font-size="11" fill="#555">'+L[i]+'</text>';
  all.forEach(function(vals,j){g+='<polyline fill="none" stroke="'+C[j]+'" stroke-width="2.5" points="'+vals.map(function(v,i){return X(i)+','+Y(v)}).join(' ')+'"/>'+vals.map(function(v,i){return'<circle cx="'+X(i)+'" cy="'+Y(v)+'" r="8" fill="transparent" data-tip="'+esc(names[j])+' · '+L[i]+': '+v+' tr/m²"/>'}).join('')});
  $('#cmpChart').innerHTML='<figure class="chart"><svg viewBox="0 0 '+W+' '+h+'" role="img" aria-label="So sánh giá '+esc(names.join(', '))+'">'+g+'</svg><figcaption class="legend">'+names.map(function(n,j){return'<span><i style="background:'+C[j]+'"></i>'+esc(n)+'</span>'}).join('')+'<small>Đơn vị: tr/m² · số liệu mẫu</small></figcaption><div class="tip" hidden></div></figure>';bindTips($('#cmpChart'))}
 $$('[data-cmp]').forEach(function(s){s.addEventListener('change',draw)})}
/* directory filter */
$$('[data-dir-filter]').forEach(function(f){var q=$('#dq'),c=$('#dc');function run(){var n=0,qq=q.value.trim().toLowerCase();$$('.dir-list .dir').forEach(function(a){var ok=(!qq||a.dataset.name.indexOf(qq)>-1||a.textContent.toLowerCase().indexOf(qq)>-1)&&(!c.value||a.dataset.city===c.value);a.hidden=!ok;if(ok)n++});var nr=$('#noRes');if(nr)nr.hidden=n>0}q.addEventListener('input',run);c.addEventListener('change',run);f.addEventListener('submit',function(e){e.preventDefault();run()})});
/* FAQ filter */
$$('[data-faq-filter]').forEach(function(i){i.addEventListener('input',function(){var q=i.value.trim().toLowerCase();$$('details').forEach(function(d){var ok=!q||d.textContent.toLowerCase().indexOf(q)>-1;d.hidden=!ok;if(q&&ok)d.open=true})})});
/* cards from data.js */
function lcard(l){return'<article class="pc"><a class="th" href="'+R+'tin/'+l.id+'.html" tabindex="-1" aria-hidden="true"><img src="'+R+'img/r'+l.img+'.jpg" alt="" loading="lazy" width="400" height="300"></a><div class="pc-b"><h3><a href="'+R+'tin/'+l.id+'.html">'+esc(l.t)+'</a></h3><p class="pr"><b>'+money(l.p,l.m)+'</b> · '+l.a+' m²</p><p class="loc">'+esc(l.d+', '+l.c)+'</p><div class="pc-f"><span>'+esc(l.tn)+'</span><button class="heart" data-fav="'+l.id+'" aria-pressed="false" aria-label="Lưu tin"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.5-9.5-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.5 6c-2.5 4.5-9.5 9-9.5 9z"/></svg></button></div></div></article>'}
function pjcard(p){return'<article class="pc"><a class="th" href="'+R+'du-an/'+p.s+'.html" tabindex="-1" aria-hidden="true"><img src="'+R+'img/r'+p.img+'.jpg" alt="" loading="lazy" width="400" height="300"></a><div class="pc-b"><h3><a href="'+R+'du-an/'+p.s+'.html">'+esc(p.n)+'</a></h3><p class="pr"><b>'+esc(p.pr)+'</b></p><p class="loc">'+esc(p.d+', '+p.c)+'</p></div></article>'}
function renderSaved(){var box=$('#savedList');if(!box||!window.ND)return;var L=ND.L.filter(function(l){return favs.indexOf(l.id)>-1});box.innerHTML=L.map(lcard).join('');$('#savedEmpty').hidden=!!L.length;$('#savedCount').textContent=L.length?L.length+' tin đã lưu':'';syncFav()}
if($('#savedList')){if(window.ND)renderSaved();else{var s=document.createElement('script');s.src=R+'js/data.js';s.onload=renderSaved;document.body.appendChild(s)}}
/* search results */
var sres=$('#sres');
if(sres&&window.ND){var p=new URLSearchParams(location.search),q=(p.get('q')||'').trim(),mode=p.get('mode')||'ban',city=p.get('city')||'',ts=p.get('ts')||'',pr=p.get('price'),ar=p.get('area'),scope=p.get('scope');
 function norm(s){return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d')}var nq=norm(q),out='',n=0;
 if(scope==='wiki'){var A=ND.A.filter(function(a){return!nq||norm(a.t).indexOf(nq)>-1});n=A.length;out='<ul class="lk">'+A.map(function(a){return'<li><a href="'+R+a.u+'">'+esc(a.t)+'</a></li>'}).join('')+'</ul>';sres.className=''}
 else if(mode==='duan'){var P=ND.P.filter(function(x){return(!nq||norm(x.n+' '+x.d+' '+x.c).indexOf(nq)>-1)&&(!city||x.cs===city||x.c===city)});n=P.length;out=P.map(pjcard).join('')}
 else{var L=ND.L.filter(function(l){if(l.m!==mode)return false;if(city&&l.cs!==city&&l.c!==city)return false;if(ts&&l.ts!==ts)return false;if(nq&&norm(l.t+' '+l.d+' '+l.c+' '+l.tn).indexOf(nq)<0)return false;if(pr){var a=pr.split('-');if(l.p<+a[0]||l.p>=+a[1])return false}if(ar){var b=ar.split('-');if(l.a<+b[0]||l.a>=+b[1])return false}return true});n=L.length;out=L.slice(0,120).map(lcard).join('')}
 $('#sqh').textContent=q?'Kết quả cho "'+q+'"':'Kết quả tìm kiếm';$('#sqc').textContent=n?('Tìm thấy '+n+' kết quả'+(n>120?' (hiện 120 đầu tiên)':'')):'Không tìm thấy kết quả. Thử từ khóa khác như "Cầu Giấy", "căn hộ".';sres.innerHTML=out;syncFav()}
/* home search tabs */
var hs=$('[data-search-home]');
if(hs){var mi=document.createElement('input');mi.type='hidden';mi.name='mode';mi.value='ban';hs.appendChild(mi);$$('[data-m]',hs).forEach(function(b){b.addEventListener('click',function(){$$('[data-m]',hs).forEach(function(x){x.setAttribute('aria-selected','false')});b.setAttribute('aria-selected','true');mi.value=b.dataset.m;var t=$('#ht');if(t)t.disabled=b.dataset.m==='duan'})});
 hs.addEventListener('submit',function(){$$('select',hs).forEach(function(s){if(!s.value)s.disabled=true})})}
/* post wizard */
var pf=$('#postForm');
if(pf){var step=0,steps=$$('.step',pf),lis=$$('.stepper li'),D=JSON.parse(pf.dataset.dists||'{}'),err=$('#postErr');
 pf.city.addEventListener('change',function(){var ds=D[pf.city.value]||[];pf.dist.innerHTML='<option value="">Chọn quận/huyện</option>'+ds.map(function(d){return'<option>'+esc(d)+'</option>'}).join('')});
 function tot(){var r=$('input[name=plan]:checked',pf),d=+pf.days.value;$('#total').textContent=((r?+r.dataset.price:0)*d).toLocaleString('vi-VN')+' đ'}pf.addEventListener('change',tot);tot();
 pf.photos.addEventListener('change',function(){var t=$('#thumbs');t.innerHTML='';Array.prototype.slice.call(pf.photos.files,0,12).forEach(function(f){var i=document.createElement('img');i.alt=f.name;i.src=URL.createObjectURL(f);t.appendChild(i)})});
 function valid(){var bad=$$('input,select,textarea',steps[step]).filter(function(x){return!x.checkValidity()});if(bad.length){err.textContent='Vui lòng điền đúng: '+bad.map(function(x){var l=x.closest('label');return l?l.firstChild.textContent.replace('*','').trim():x.name}).join(', ');bad[0].focus();return false}err.textContent='';return true}
 function go(n){step=n;steps.forEach(function(s,i){s.hidden=i!==step});lis.forEach(function(l,i){l.className=i<step?'done':i===step?'on':''});$('[data-prev]',pf).hidden=!step;$('[data-next]',pf).hidden=step===steps.length-1;$('[data-submit]',pf).hidden=step!==steps.length-1;
  if(step===3)$('#preview').innerHTML='<b>'+esc(pf.title.value)+'</b><br>'+esc(pf.mode.value==='ban'?'Bán':'Cho thuê')+' · '+esc(pf.type.options[pf.type.selectedIndex].text)+' · '+esc(pf.area.value)+' m² · '+esc(pf.price.value+' '+pf.unit.value)+'<br>'+esc([pf.street.value,pf.dist.value,pf.city.value].filter(Boolean).join(', '))+'<br>Gói: '+esc($('input[name=plan]:checked',pf).value)+' · '+pf.days.value+' ngày · '+$('#total').textContent;
  window.scrollTo(0,pf.offsetTop-100)}
 $('[data-next]',pf).onclick=function(){if(valid())go(step+1)};$('[data-prev]',pf).onclick=function(){go(step-1)};
 pf.addEventListener('submit',function(e){e.preventDefault();if(!valid())return;var posts=LS.get('nd_posts',[]);posts.unshift({t:pf.title.value,m:pf.mode.value,city:pf.city.value,dist:pf.dist.value,area:pf.area.value,price:pf.price.value+' '+pf.unit.value,plan:$('input[name=plan]:checked',pf).value,at:new Date().toLocaleString('vi-VN')});LS.set('nd_posts',posts);toast('Đã đăng tin (demo) – xem ở Trang cá nhân');setTimeout(function(){location.href=R+'trang-ca-nhan.html#tin'},700)})}
/* profile */
var mp=$('#myPosts');
if(mp){var posts=LS.get('nd_posts',[]);mp.innerHTML=posts.length?posts.map(function(p,i){return'<div class="mp"><div><b>'+esc(p.t)+'</b><br><small class="muted">'+esc((p.m==='ban'?'Bán':'Cho thuê')+' · '+p.dist+', '+p.city+' · '+p.area+' m² · '+p.price+' · '+p.plan+' · '+p.at)+'</small></div><button class="btn btn-sm" data-del="'+i+'">Xóa</button></div>'}).join(''):'<p class="empty">Chưa có tin đăng nào. <a class="red" href="'+R+'dang-tin.html">Đăng tin đầu tiên</a></p>';
 mp.addEventListener('click',function(e){var b=e.target.closest('[data-del]');if(!b)return;posts.splice(+b.dataset.del,1);LS.set('nd_posts',posts);location.reload()})}
var pr2=$('[data-profile]');if(pr2){var u=user()||{};if(pr2.name)pr2.name.value=u.name||'';pr2.addEventListener('submit',function(e){e.preventDefault();var u=user()||{};u.name=pr2.name.value;LS.set('nd_user',u);toast('Đã lưu thông tin (demo)');renderAcct()})}
})();
