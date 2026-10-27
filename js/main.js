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
