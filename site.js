(() => {
  const btn = document.querySelector('.menu-btn');
  const nav = document.querySelector('.main-nav');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }));
  }

  const series = Array.isArray(window.SEER_SERIES) ? window.SEER_SERIES : [];

  const chips = s => `<ul class="series-chips" aria-label="What to expect from ${s.name}">${s.highlights.map(item => `<li>${item}</li>`).join('')}</ul>`;

  const homeCard = (s, index) => `<article class="series-feature series-${s.slug}${index % 2 ? ' series-feature-reverse' : ''}">
    <a class="series-feature-visual" href="${s.website}" target="_blank" rel="noopener" aria-label="Visit ${s.name}">
      <img src="${s.image}" alt="${s.name} series artwork" loading="${index === 0 ? 'eager' : 'lazy'}" decoding="async">
    </a>
    <div class="series-feature-copy">
      <div class="series-meta"><span>${s.category}</span><span>${s.audience}</span></div>
      <h3>${s.name}</h3>
      <p class="series-tagline">${s.tagline}</p>
      <p class="series-description">${s.description}</p>
      <p class="series-reader-hook"><strong>For readers who want:</strong> ${s.readerHook.replace(/^Start here if you /, '')}</p>
      ${chips(s)}
      <a class="btn btn-navy series-cta" href="${s.website}" target="_blank" rel="noopener">${s.cta} <span aria-hidden="true">↗</span></a>
    </div>
  </article>`;

  const directoryCard = s => `<article class="series-card series-card-rich">
    <a class="series-visual" href="${s.website}" target="_blank" rel="noopener" aria-label="Visit ${s.name}"><img src="${s.image}" alt="${s.name} series artwork" loading="lazy" decoding="async"></a>
    <div class="series-card-body">
      <div class="series-meta"><span>${s.category}</span><span>${s.audience}</span></div>
      <h3>${s.name}</h3>
      <p class="series-card-tagline">${s.tagline}</p>
      <p>${s.description}</p>
      ${chips(s)}
      <p class="series-reader-mini">${s.readerHook}</p>
      <div class="series-actions"><a class="series-visit" href="${s.website}" target="_blank" rel="noopener">${s.cta} <span aria-hidden="true">↗</span></a></div>
    </div>
  </article>`;

  const pressCard = s => `<article class="series-card">
    <a class="series-visual" href="${s.website}" target="_blank" rel="noopener" aria-label="Visit ${s.name}"><img src="${s.image}" alt="${s.name} series artwork" loading="lazy" decoding="async"></a>
    <div class="series-card-body"><div class="series-meta"><span>${s.category}</span><span>${s.audience}</span></div><h3>${s.name}</h3><p>${s.description}</p><div class="series-actions"><a class="series-visit" href="${s.website}" target="_blank" rel="noopener">Visit series <span aria-hidden="true">↗</span></a><a class="text-link" href="${s.press}">Press assets →</a></div></div>
  </article>`;

  document.querySelectorAll('[data-series-grid]').forEach(grid => {
    const mode = grid.getAttribute('data-series-grid') || 'home';
    if (mode === 'home') {
      grid.classList.add('series-showcase');
      grid.innerHTML = series.map(homeCard).join('');
    } else if (mode === 'directory') {
      grid.innerHTML = series.map(directoryCard).join('');
    } else if (mode === 'press') {
      grid.innerHTML = series.map(pressCard).join('');
    }
  });
})();
