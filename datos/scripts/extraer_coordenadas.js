// Pegar en la consola del navegador (pestaña de maptap.gg) o correr con la herramienta javascript del navegador de Claude.
// Devuelve, para una lista de fechas, las 5 ubicaciones EXACTAS del dia en orden de ronda: "lat|lng|nombre;...".
// Dias nuevos: las historias estan en /history/<Mes><dia>.html y cada historia trae STORY_MAP.targets {lat,lng,name,locIndex}.
// Dias viejos (22/7 al 1/8): getCitiesData() en la misma pagina (lat, lng, name en orden de ronda).
// Importante: leer el HTML crudo con fetch (el DOM del dia actual esconde las historias hasta que el usuario juega, pero el HTML las trae).
const FECHAS=[["October",19]];   // ej. [["October",19]]
async function dia(n,d){
  const h=await fetch(`/history/${n}${d}.html`).then(r=>r.text());
  const links=[...new Set([...h.matchAll(/href="(\/history\/2026\/[A-Za-z]+\d+\/[^"]+\.html)"/g)].map(x=>x[1]))];
  const out={};
  for(const l of links){
    const s=await fetch(l).then(r=>r.text());
    const m=s.match(/targets:\s*(\[[^\]]*\])/);   // JSON.parse, sin eval
    if(m){JSON.parse(m[1]).forEach(t=>{out[t.locIndex]=[t.lat,t.lng,t.name]})}
  }
  if(Object.keys(out).length!==5){ // formato viejo
    const body=h.slice(h.indexOf('function getCitiesData'));
    body.slice(0,body.indexOf('];')).split(/\{\s*\n\s*name:/).slice(1).forEach((p,i)=>{
      const nm=p.match(/^\s*"((?:[^"\\]|\\.)*)"/),la=p.match(/\blat:\s*(-?[\d.]+)/),lo=p.match(/\blng:\s*(-?[\d.]+)/);
      if(nm&&la&&lo)out[i]=[+la[1],+lo[1],nm[1]]});
  }
  if(Object.keys(out).length!==5) throw new Error(`${n}${d}: se esperaban 5 ubicaciones y hay ${Object.keys(out).length}`);
  return [0,1,2,3,4].map(i=>out[i].join('|')).join(';');
}
const res=[];for(const [n,d] of FECHAS)res.push(n+d+'#'+await dia(n,d));
res.join('\n')
