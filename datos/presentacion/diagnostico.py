"""Uso: python3 diagnostico.py -> salida/diag.html: la presentacion completa + un script que mide cada diapositiva
(escala de ajuste, desbordes del marco, textos truncados) y lo escribe en la consola. Sirve para revisar sin mirar las 96 a ojo."""
import pathlib
aqui = pathlib.Path(__file__).resolve().parent
h = (aqui / "salida" / "presentacion.html").read_text(encoding="utf-8")
diag = r"""<script>
addEventListener('load',function(){setTimeout(function(){
var D=window.__deck,out=[],lim=22;var ks=[];
D.slides.forEach(function(s,i){
  D.show(i);var k=s.getAttribute('data-k'),prob=[];ks.push(k);
  var h1=s.querySelector('h1'),t=(h1?h1.textContent:'').replace(/\s+/g,' ').trim().slice(0,28)||('['+s.className.replace('slide ','')+']');
  var inner=s.querySelector('.inner');
  if(inner&&inner.scrollHeight>inner.clientHeight+2)prob.push('inner desborda '+(inner.scrollHeight-inner.clientHeight)+'px');
  [].forEach.call(s.querySelectorAll('*'),function(e){
    if(e.closest('svg')&&e.tagName!=='svg')return;
    var r=e.getBoundingClientRect();if(!r.width||!r.height)return;
    var sr=s.getBoundingClientRect();var kk=sr.width/1280;
    var R=(r.right-sr.left)/kk,B=(r.bottom-sr.top)/kk,L=(r.left-sr.left)/kk,T=(r.top-sr.top)/kk;
    if(R>1280-lim+1||B>720-lim+1||L<lim-1||T<lim-1){if(prob.length<4)prob.push('fuera del marco: '+e.tagName+'.'+(e.className.baseVal!==undefined?e.className.baseVal:e.className)+' '+(e.textContent||'').trim().slice(0,22)+' ['+Math.round(L)+','+Math.round(T)+','+Math.round(R)+','+Math.round(B)+']');}
    if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible'&&e.clientWidth>0&&prob.length<6)prob.push('texto cortado: '+e.tagName+'.'+e.className+' '+(e.textContent||'').trim().slice(0,24));
  });
  if(prob.length||parseFloat(k)<0.6)out.push((i+1)+' | '+t+' | k='+k+(prob.length?' | '+prob.join(' ; '):''));
});
D.show(0);
console.log('KS '+ks.join(','));
console.log('DIAG '+D.slides.length+' diapositivas; con problemas o k<0.8: '+out.length+' || '+out.join(' || ').slice(0,1500));
},800);});
</script>"""
(aqui / "salida" / "diag.html").write_text(h.replace("</body>", diag + "</body>") if "</body>" in h else h + diag, encoding="utf-8")
print("ok -> salida/diag.html")
