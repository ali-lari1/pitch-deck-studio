(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var body=document.body, deck=document.querySelector('.deck');
  var bar=document.querySelector('.hud .bar'), count=document.querySelector('.hud .count');
  var params=new URLSearchParams(location.search), cur=0;
  var panel=document.createElement('div'); panel.className='notes-panel'; body.appendChild(panel);

  function fit(){
    var s=Math.min(innerWidth/1920, innerHeight/1080);
    document.documentElement.style.setProperty('--s', s);
    document.documentElement.style.setProperty('--z', Math.min(1,(innerWidth-48)/1920));
  }
  function show(i, push){
    cur=Math.max(0, Math.min(slides.length-1, i));
    slides.forEach(function(s,k){ s.classList.toggle('active', k===cur); });
    bar.style.width=((cur+1)/slides.length*100)+'%';
    count.textContent=(cur+1)+' / '+slides.length;
    var n=slides[cur].nextElementSibling;
    panel.innerHTML=(n && n.classList.contains('notes')) ? n.innerHTML : '<p style="opacity:.5">No notes on this slide.</p>';
    if(push!==false && !body.classList.contains('reader')) history.replaceState(null,'','#'+(cur+1));
    if(body.classList.contains('overview')||body.classList.contains('reader')) slides[cur].scrollIntoView({block:'center'});
  }
  function mode(name){
    ['overview','reader'].forEach(function(m){ if(m!==name) body.classList.remove(m); });
    body.classList.toggle(name);
    show(cur,false);
  }
  addEventListener('resize', fit);
  addEventListener('keydown', function(e){
    if(e.metaKey||e.ctrlKey||e.altKey) return;
    var k=e.key;
    if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].indexOf(k)>-1){ e.preventDefault(); show(cur+1); }
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(k)>-1){ e.preventDefault(); show(cur-1); }
    else if(k==='Home') show(0); else if(k==='End') show(slides.length-1);
    else if(k==='o'||k==='O'||k==='Escape'&&body.classList.contains('overview')) mode('overview');
    else if(k==='r'||k==='R') mode('reader');
    else if(k==='n'||k==='N') body.classList.toggle('show-notes');
    else if(k==='f'||k==='F'){ document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
    else if(k==='p'||k==='P') print();
  });
  slides.forEach(function(s,k){
    s.addEventListener('click', function(e){
      if(e.target.closest('a')) return;
      if(body.classList.contains('overview')){ body.classList.remove('overview'); show(k); return; }
      if(body.classList.contains('reader')) return;
      show(e.clientX < innerWidth*0.25 ? cur-1 : cur+1);
    });
  });
  var tx=null;
  addEventListener('touchstart', function(e){ tx=e.touches[0].clientX; }, {passive:true});
  addEventListener('touchend', function(e){ if(tx===null) return; var dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40) show(cur+(dx<0?1:-1)); tx=null; });

  fit();
  var start=parseInt((location.hash||'').slice(1),10);
  if(params.has('solo')){
    body.classList.add('solo'); var i=parseInt(params.get('solo'),10)-1;
    slides.forEach(function(s,k){ s.classList.toggle('active', k===i); });
    return;
  }
  if(params.has('check')){
    body.classList.add('check');
    var run=function(){
      var issues=[];
      slides.forEach(function(sl,k){
        var inn=sl.querySelector('.in'); if(!inn||sl.classList.contains('bleed')) return;
        var ir=inn.getBoundingClientRect(), seen=[];
        if(inn.scrollHeight>inn.clientHeight+12) issues.push({slide:k+1,what:'content is '+(inn.scrollHeight-inn.clientHeight)+'px taller than the safe area'});
        [].forEach.call(inn.querySelectorAll('*'),function(el){
          if(seen.some(function(p){return p.contains(el);})) return;
          var r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
          var d=Math.max(r.bottom-ir.bottom, r.right-ir.right, ir.left-r.left, ir.top-r.top);
          if(d>12){ seen.push(el); issues.push({slide:k+1,what:'<'+el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.split(' ')[0]:'')+'> '+Math.round(d)+'px outside the safe area: "'+(el.textContent||'').trim().slice(0,50)+'"'}); }
        });
      });
      var pre=document.createElement('pre'); pre.id='qa-result';
      pre.textContent=JSON.stringify({slides:slides.length,issues:issues}); body.appendChild(pre);
    };
    (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(run,50); });
    return;
  }
  if(params.has('grid')){ body.classList.add('grid'); slides.forEach(function(s){ s.classList.add('active'); }); return; }
  if(params.has('reader')) body.classList.add('reader');
  if(params.has('notes')) body.classList.add('show-notes');
  show(isNaN(start)?0:start-1, false);
})();
