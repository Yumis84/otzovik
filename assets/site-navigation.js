/* Unified navigation on informational pages; root landing keeps its existing header. */
(function(){
  var header=document.querySelector('header.site-header');
  if(!header)return;
  var toggle=header.querySelector('.site-toggle');
  var mobile=header.querySelector('.site-mobile');
  if(!toggle||!mobile)return;
  toggle.addEventListener('click',function(){
    var expanded=toggle.getAttribute('aria-expanded')==='true';
    toggle.setAttribute('aria-expanded',String(!expanded));
    mobile.hidden=expanded;
  });
  mobile.addEventListener('click',function(event){
    if(event.target.closest('a')){mobile.hidden=true;toggle.setAttribute('aria-expanded','false');}
  });
})();
