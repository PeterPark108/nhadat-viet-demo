/* Bản đồ Leaflet + OSM (demo). Tọa độ mẫu theo quận */
(function(){
var R=window.ROOT||'',ND=window.ND,box=document.getElementById('map');
if(!box||!ND)return;
if(!window.L){box.innerHTML='<p class="empty" style="margin:24px">Không tải được thư viện bản đồ (cần Internet).</p>';return}
var css=document.createElement('link');css.rel='stylesheet';css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(css);
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function money(p,m){return m==='thue'?(Math.round(p/1e5)/10+' tr'):(p>=1e9?Math.round(p/1e7)/100+' tỷ':Math.round(p/1e6)+' tr')}
var map=L.map(box,{scrollWheelZoom:true}).setView([16.2,106.5],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
var layer=L.layerGroup().addTo(map),mk={};
var q=new URLSearchParams(location.search),mm=document.getElementById('mm'),mc=document.getElementById('mc'),list=document.getElementById('mapList'),cnt=document.getElementById('mapCount');
var focusId=q.get('id'),focusPj=q.get('pj');
if(q.get('mode'))mm.value=q.get('mode');if(focusPj)mm.value='pj';
if(focusId){var f=ND.L.find(function(l){return l.id==focusId});if(f){mm.value=f.m;mc.value=f.cs}}
if(focusPj){var g=ND.P.find(function(p){return p.id==focusPj});if(g)mc.value=g.cs}
if(q.get('city'))mc.value=q.get('city');
function render(){layer.clearLayers();mk={};var m=mm.value,c=mc.value,items;
 if(m==='pj')items=ND.P.filter(function(p){return!c||p.cs===c}).map(function(p){return{k:'p'+p.id,id:p.id,lat:p.lat,lng:p.lng,t:p.n,lab:'DA',pr:p.pr,img:p.img,u:R+'du-an/'+p.s+'.html',loc:p.d+', '+p.c,pj:1}});
 else items=ND.L.filter(function(l){return l.m===m&&(!c||l.cs===c)}).map(function(l){return{k:'l'+l.id,id:l.id,lat:l.lat,lng:l.lng,t:l.t,lab:money(l.p,l.m),pr:money(l.p,l.m)+' · '+l.a+' m²',img:l.img,u:R+'tin/'+l.id+'.html',loc:l.d+', '+l.c}});
 cnt.textContent=items.length+(m==='pj'?' dự án':' tin đăng')+' trên bản đồ';
 var b=[];items.forEach(function(it){var ic=L.divIcon({className:'',html:'<span class="pin'+(it.pj?' pj':'')+'">'+esc(it.lab)+'</span>',iconSize:null});var x=L.marker([it.lat,it.lng],{icon:ic,title:it.t,keyboard:true}).bindPopup('<a href="'+it.u+'" style="display:block;width:200px"><img src="'+R+'img/r'+it.img+'.jpg" alt="" style="width:200px;height:120px;object-fit:cover;border-radius:6px"><b>'+esc(it.t)+'</b></a><div>'+esc(it.pr)+'</div><small>'+esc(it.loc)+'</small>');x.on('click',function(){hl(it.k)});x.addTo(layer);mk[it.k]=x;b.push([it.lat,it.lng])});
 list.innerHTML=items.slice(0,200).map(function(it){return'<button type="button" class="mi" data-k="'+it.k+'"><img src="'+R+'img/r'+it.img+'.jpg" alt="" loading="lazy"><span><b>'+esc(it.t)+'</b><span class="red">'+esc(it.pr)+'</span><br><small class="muted">'+esc(it.loc)+'</small></span></button>'}).join('');
 if(b.length)map.fitBounds(b,{padding:[30,30],maxZoom:14});
 var fk=focusId?'l'+focusId:focusPj?'p'+focusPj:null;if(fk&&mk[fk]){map.setView(mk[fk].getLatLng(),15);mk[fk].openPopup();hl(fk);focusId=focusPj=null}}
function hl(k){Array.prototype.forEach.call(list.querySelectorAll('.mi'),function(e){e.classList.toggle('on',e.dataset.k===k);if(e.dataset.k===k)e.scrollIntoView({block:'nearest'})})}
list.addEventListener('click',function(e){var b=e.target.closest('.mi');if(!b)return;var x=mk[b.dataset.k];if(x){map.setView(x.getLatLng(),15);x.openPopup();hl(b.dataset.k)}});
mm.addEventListener('change',render);mc.addEventListener('change',render);
document.body.classList.add('map-body');render();setTimeout(function(){map.invalidateSize()},300);
})();
