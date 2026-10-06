document.querySelectorAll('.chip').forEach(chip=>{
    chip.addEventListener('click', ()=>{
      const group = chip.closest('.filters') || chip.closest('.filters-row');
      (group ? group.querySelectorAll('.chip') : document.querySelectorAll('.chip')).forEach(c=>c.classList.remove('is-active'));
      chip.classList.add('is-active');
    });
  });
  document.querySelectorAll('.tab').forEach(tab=>{
    tab.addEventListener('click', ()=>{
      const group = tab.closest('.tabs');
      group.querySelectorAll('.tab').forEach(t=>t.classList.remove('is-active'));
      tab.classList.add('is-active');
      const target = tab.getAttribute('data-target');
      if(target){
        document.querySelectorAll('.tab-panel').forEach(p=>p.style.display='none');
        const panel = document.querySelector(target);
        if(panel) panel.style.display='grid';
      }
    });
  });
  document.querySelectorAll('form.mock-form').forEach(f=>{
    f.addEventListener('submit', e=>{
      e.preventDefault();
      const btn = f.querySelector('button[type=submit]');
      if(btn){ const orig = btn.textContent; btn.textContent = 'Demande envoyée ✓'; setTimeout(()=>btn.textContent=orig, 2200); }
    });
  });
  const toggle = document.querySelector('.navtoggle');
  const links = document.querySelector('.navlinks');
  if(toggle){
    toggle.addEventListener('click', ()=>{
      const shown = links.style.display === 'flex';
      links.style.display = shown ? 'none' : 'flex';
      links.style.cssText += shown ? '' : 'position:absolute;top:76px;left:0;right:0;background:var(--sable);flex-direction:column;padding:20px 28px;border-bottom:1px solid var(--line);gap:16px;z-index:60;';
    });
  }

// Hero word cycler (home page only)
(function(){
  const words = ["Concevoir","Construire","Gérer","Importer"];
  const el = document.getElementById('cycler');
  if(!el) return;
  el.style.transition = 'opacity .2s ease';
  let i = 0;
  setInterval(() => {
    i = (i+1) % words.length;
    el.style.opacity = 0;
    setTimeout(()=>{ el.textContent = words[i]; el.style.opacity = 1; }, 200);
  }, 2200);
})();
