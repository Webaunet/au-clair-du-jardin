(function(){
  var b=document.querySelector('.burger'),n=document.getElementById('nav');
  if(b&&n){
    var set=function(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')};
    b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true')});
    n.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){set(false);b.focus()}});
    window.addEventListener('resize',function(){if(window.innerWidth>980)set(false)});
  }
  var r=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('on');io.unobserve(x.target)}})},{threshold:.12});
    r.forEach(function(e){io.observe(e)});
  }else{r.forEach(function(e){e.classList.add('on')})}
})();

/* Formulaire de contact : validation et récapitulatif (site statique, aucun envoi serveur) */
(function(){
  var f=document.getElementById('devis');if(!f)return;
  var TEL='+33661977828',MAIL='contact@auclairdujardin.com';
  var rules={
    nom:function(v){return v.trim().length>=2||'Indiquez votre nom.'},
    tel:function(v){return /^(?:(?:\+|00)33|0)[1-9](?:[\s.\-]?\d{2}){4}$/.test(v.trim())||'Indiquez un numéro valide, par exemple 06 12 34 56 78.'},
    commune:function(v){return v.trim().length>=2||'Indiquez votre commune.'},
    besoin:function(v){return v!==''||'Choisissez votre besoin.'}
  };
  function check(n){
    var el=f.elements[n],r=rules[n](el.value),e=document.getElementById('e-'+n);
    if(r===true){el.removeAttribute('aria-invalid');e.textContent='';return true}
    el.setAttribute('aria-invalid','true');e.textContent=r;return false;
  }
  Object.keys(rules).forEach(function(n){
    f.elements[n].addEventListener('blur',function(){check(n)});
    f.elements[n].addEventListener('input',function(){if(f.elements[n].getAttribute('aria-invalid'))check(n)});
  });
  var rc=document.getElementById('recap'),pre=document.getElementById('recap-texte'),cp=document.getElementById('copie');
  f.addEventListener('submit',function(ev){
    ev.preventDefault();
    var bad=Object.keys(rules).filter(function(n){return !check(n)});
    if(bad.length){f.elements[bad[0]].focus();rc.hidden=true;return}
    var m=f.elements.message.value.trim();
    var t='Demande de devis – Au Clair du Jardin\nNom : '+f.elements.nom.value.trim()+'\nTéléphone : '+f.elements.tel.value.trim()+'\nCommune : '+f.elements.commune.value.trim()+'\nBesoin : '+f.elements.besoin.value+(m?'\nMessage : '+m:'');
    pre.textContent=t;
    document.getElementById('b-sms').href='sms:'+TEL+'?body='+encodeURIComponent(t);
    document.getElementById('b-mail').href='mailto:'+MAIL+'?subject='+encodeURIComponent('Demande de devis')+'&body='+encodeURIComponent(t);
    cp.textContent='';rc.hidden=false;
    rc.scrollIntoView({behavior:'smooth',block:'nearest'});
    document.getElementById('recap-titre').focus();
  });
  document.getElementById('b-copier').addEventListener('click',function(){
    var t=pre.textContent;
    var ok=function(){cp.textContent='Récapitulatif copié.'};
    var ko=function(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);cp.textContent='Texte sélectionné : copiez-le avec Ctrl+C.'};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,ko)}else{ko()}
  });
})();
