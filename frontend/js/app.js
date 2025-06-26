import { SYMPTOMS } from './symptoms.js';

const API = ' http://127.0.0.1:8000'; // ← update after backend deploy

const inp       = document.getElementById('sym');
const dd        = document.getElementById('dd');
const pickedBox = document.getElementById('picked');
const btn       = document.getElementById('go');
const out       = document.getElementById('out');
const predList  = document.getElementById('pred-list');
const suggList  = document.getElementById('suggest-list');

let picked = [];

/* -------- autocomplete -------- */
inp.addEventListener('input', () => {
  const q = inp.value.trim().toLowerCase();
  dd.innerHTML = '';
  if (!q) return dd.style.display = 'none';

  const hits = SYMPTOMS.filter(s => s.includes(q) && !picked.includes(s));
  if (!hits.length) return dd.style.display = 'none';

  hits.forEach(sym => {
    const d = document.createElement('div');
    d.className = 'dropdown-item';
    d.textContent = sym;
    d.onclick = () => add(sym);
    dd.appendChild(d);
  });
  dd.style.display = 'block';
});

function add(sym) {
  if (picked.includes(sym)) return;
  picked.push(sym);

  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = sym;

  const x = document.createElement('span');
  x.textContent = '✖';
  x.onclick = () => {
    picked = picked.filter(p => p !== sym);
    badge.remove();
  };

  badge.appendChild(x);
  pickedBox.appendChild(badge);
  inp.value = '';
  dd.style.display = 'none';
}

/* -------- predict -------- */
btn.onclick = async () => {
  if (!picked.length) return alert('Pick some symptoms first.');

  btn.disabled = true;
  btn.textContent = 'Predicting…';
  try {
    const res  = await fetch(API, {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ symptoms: picked })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Server error');
    showResult(data);
  } catch (e) {
    alert(e.message);
  }
  btn.disabled = false;
  btn.textContent = 'Predict';
};

function bar(percent) {
  const wrap = document.createElement('div');
  wrap.className = 'progress';
  const fill = document.createElement('div');
  fill.style.width = `${percent}%`;
  wrap.appendChild(fill);
  return wrap;
}

function showResult({ top, suggest }) {
  predList.innerHTML = '';
  suggList.innerHTML = '';

  top.forEach(t => {
    const p = document.createElement('p');
    p.innerHTML = `<strong>${t.disease}</strong> — ${t.prob.toFixed(1)}%`;
    predList.appendChild(p);
    predList.appendChild(bar(t.prob));
  });

  suggest.forEach(s => {
    const li = document.createElement('li');
    li.textContent = s;
    suggList.appendChild(li);
  });

  out.style.display = 'block';
}
