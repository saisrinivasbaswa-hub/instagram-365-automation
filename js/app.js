document.addEventListener('DOMContentLoaded', () => {
  // Check if QUOTES_DATA loaded
  if (typeof QUOTES_DATA === 'undefined' || !QUOTES_DATA.length) {
    console.error('Quotes dataset missing!');
    return;
  }

  // Initialize Canvas Studio
  const studio = new CanvasStudio('quoteCanvas');
  let currentQuote = QUOTES_DATA[0];
  let activeCategory = 'all';
  let searchTerm = '';

  // Elements
  const brandHandleInput = document.getElementById('brandHandle');
  const currentDayBadge = document.getElementById('currentDayBadge');
  const captionText = document.getElementById('captionText');
  const hashtagsText = document.getElementById('hashtagsText');
  const btnDownload = document.getElementById('btnDownload');
  const btnCopyCaption = document.getElementById('btnCopyCaption');
  const copyToast = document.getElementById('copyToast');
  const daySlider = document.getElementById('daySlider');
  const sliderVal = document.getElementById('sliderVal');
  const searchInput = document.getElementById('searchInput');
  const categoryTags = document.getElementById('categoryTags');
  const quotesGrid = document.getElementById('quotesGrid');
  const themeBtns = document.querySelectorAll('.style-btn');

  // Initial Setup
  function selectQuote(quoteObj) {
    currentQuote = quoteObj;
    
    // Update badge & slider
    currentDayBadge.textContent = `Day ${quoteObj.day} / 365`;
    daySlider.value = quoteObj.day;
    sliderVal.textContent = `Day ${quoteObj.day}`;
    
    // Update caption panel
    captionText.textContent = quoteObj.caption;
    hashtagsText.textContent = quoteObj.hashtags;

    // Render Canvas
    studio.render(currentQuote, brandHandleInput.value);

    // Update selected item in grid
    document.querySelectorAll('.quote-item').forEach(el => {
      if (parseInt(el.dataset.day) === quoteObj.day) {
        el.classList.add('selected');
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        el.classList.remove('selected');
      }
    });
  }

  // Render Grid Items
  function renderGrid() {
    quotesGrid.innerHTML = '';

    const filtered = QUOTES_DATA.filter(item => {
      const matchCat = activeCategory === 'all' || item.category.toLowerCase() === activeCategory.toLowerCase();
      const matchSearch = searchTerm === '' || 
        item.quote.toLowerCase().includes(searchTerm.toLowerCase()) || 
        item.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
        `day ${item.day}`.includes(searchTerm.toLowerCase());
      return matchCat && matchSearch;
    });

    if (filtered.length === 0) {
      quotesGrid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding: 2rem; color: var(--text-muted);">No quotes match your filter.</div>`;
      return;
    }

    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = `quote-item ${item.day === currentQuote.day ? 'selected' : ''}`;
      card.dataset.day = item.day;

      card.innerHTML = `
        <div class="item-top">
          <span class="item-day">Day ${item.day}</span>
          <span class="item-tag">${item.category}</span>
        </div>
        <div class="item-quote">“${item.quote}”</div>
      `;

      card.addEventListener('click', () => {
        selectQuote(item);
      });

      quotesGrid.appendChild(card);
    });
  }

  // Event Listeners
  brandHandleInput.addEventListener('input', (e) => {
    studio.setHandle(e.target.value || '@yourbrand');
  });

  themeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      themeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      studio.setTheme(btn.dataset.theme);
    });
  });

  daySlider.addEventListener('input', (e) => {
    const dayNum = parseInt(e.target.value);
    const targetQuote = QUOTES_DATA.find(q => q.day === dayNum) || QUOTES_DATA[dayNum - 1];
    if (targetQuote) {
      selectQuote(targetQuote);
    }
  });

  searchInput.addEventListener('input', (e) => {
    searchTerm = e.target.value.trim();
    renderGrid();
  });

  categoryTags.addEventListener('click', (e) => {
    if (e.target.classList.contains('tag-btn')) {
      document.querySelectorAll('.tag-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      activeCategory = e.target.dataset.cat;
      renderGrid();
    }
  });

  btnDownload.addEventListener('click', () => {
    const filename = `day_${String(currentQuote.day).padStart(3, '0')}_quote.png`;
    studio.downloadImage(filename);
  });

  btnCopyCaption.addEventListener('click', () => {
    const fullText = `${currentQuote.caption}\n\n${currentQuote.hashtags}`;
    navigator.clipboard.writeText(fullText).then(() => {
      copyToast.style.display = 'inline';
      setTimeout(() => {
        copyToast.style.display = 'none';
      }, 2500);
    }).catch(err => {
      console.error('Failed to copy caption:', err);
    });
  });

  // Background Music Toggle
  const bgMusic = document.getElementById('bgMusic');
  const btnPlayMusic = document.getElementById('btnPlayMusic');
  const musicBtnLabel = document.getElementById('musicBtnLabel');

  if (btnPlayMusic && bgMusic) {
    btnPlayMusic.addEventListener('click', () => {
      if (bgMusic.paused) {
        bgMusic.play();
        musicBtnLabel.textContent = '🔊 Pause Music';
        btnPlayMusic.style.borderColor = 'var(--primary)';
      } else {
        bgMusic.pause();
        musicBtnLabel.textContent = '🎵 Play Music';
        btnPlayMusic.style.borderColor = 'transparent';
      }
    });
  }


  // Start with Day 1
  renderGrid();
  selectQuote(QUOTES_DATA[0]);
});
