class CanvasStudio {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    // Default 1080x1080 Instagram 1:1 format
    this.width = 1080;
    this.height = 1080;
    
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    
    this.currentTheme = 'mindset'; // 'mindset'|'food'|'cinema'|'music'|'wealth'|'fitness'|'tech'|'books'|'peace'|'productivity'
    this.currentQuote = null;
    this.brandHandle = '@the_logical_minds.1';
  }

  setTheme(themeName) {
    this.currentTheme = themeName;
    if (this.currentQuote) {
      this.render(this.currentQuote, this.brandHandle);
    }
  }

  setHandle(handle) {
    this.brandHandle = handle.startsWith('@') ? handle : `@${handle}`;
    if (this.currentQuote) {
      this.render(this.currentQuote, this.brandHandle);
    }
  }

  render(quoteObj, handle = '@the_logical_minds.1') {
    this.currentQuote = quoteObj;
    this.brandHandle = handle;
    
    const { ctx, width, height } = this;
    ctx.clearRect(0, 0, width, height);

    switch (this.currentTheme) {
      case 'food':
        this.renderFoodTheme(quoteObj, handle);
        break;
      case 'cinema':
        this.renderCinemaTheme(quoteObj, handle);
        break;
      case 'music':
        this.renderMusicTheme(quoteObj, handle);
        break;
      case 'wealth':
        this.renderWealthTheme(quoteObj, handle);
        break;
      case 'fitness':
        this.renderFitnessTheme(quoteObj, handle);
        break;
      case 'tech':
        this.renderTechTheme(quoteObj, handle);
        break;
      case 'books':
        this.renderBooksTheme(quoteObj, handle);
        break;
      case 'peace':
        this.renderPeaceTheme(quoteObj, handle);
        break;
      case 'productivity':
        this.renderProductivityTheme(quoteObj, handle);
        break;
      case 'mindset':
      default:
        this.renderMindsetTheme(quoteObj, handle);
        break;
    }
  }

  // 1. Mindset (Obsidian & Gold)
  renderMindsetTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    const bgGrad = ctx.createRadialGradient(width/2, height/2, 100, width/2, height/2, width*0.7);
    bgGrad.addColorStop(0, '#111520');
    bgGrad.addColorStop(1, '#07090e');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 4;
    ctx.strokeRect(60, 60, width - 120, height - 120);

    ctx.font = '600 24px "Outfit", sans-serif';
    ctx.fillStyle = '#8b5cf6';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`— ${quoteObj.category.toUpperCase()} —`, width / 2, 140);

    ctx.font = '600 48px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#f3f4f6';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '500 26px "Outfit", sans-serif';
    ctx.fillStyle = '#f59e0b';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#6b7280';
    ctx.fillText(`DAY ${quoteObj.day} OF 365`, width / 2, height - 90);
  }

  // 2. Food & Culinary (Warm Terracotta & Sage)
  renderFoodTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#231510';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#84a98c';
    ctx.lineWidth = 3;
    ctx.strokeRect(70, 70, width - 140, height - 140);

    ctx.font = '600 24px "Cinzel", serif';
    ctx.fillStyle = '#e0a96d';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`🌿 CULINARY WISDOM • ${quoteObj.category.toUpperCase()} 🌿`, width / 2, 150);

    ctx.font = '500 46px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#fdfbf7';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 15, width - 240, 62);

    ctx.font = '600 26px "Outfit", sans-serif';
    ctx.fillStyle = '#84a98c';
    ctx.fillText(handle, width / 2, height - 135);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#e0a96d';
    ctx.fillText(`DAY ${quoteObj.day} / 365`, width / 2, height - 95);
  }

  // 3. Cinema (Velvet Noir & Film Gold)
  renderCinemaTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#120404';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#e5a93c';
    ctx.lineWidth = 4;
    ctx.strokeRect(60, 60, width - 120, height - 120);

    ctx.font = '700 24px "Cinzel", serif';
    ctx.fillStyle = '#e5a93c';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`🎬 CINEMA TRUTH • [ ${quoteObj.category.toUpperCase()} ]`, width / 2, 140);

    ctx.font = '600 48px "Cinzel", serif';
    ctx.fillStyle = '#ffffff';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 20, width - 240, 66);

    ctx.font = '600 26px "Outfit", sans-serif';
    ctx.fillStyle = '#e5a93c';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#888';
    ctx.fillText(`DAY ${quoteObj.day} • 365`, width / 2, height - 90);
  }

  // 4. Music (Cyber Purple & Neon Cyan)
  renderMusicTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#0a0714';
    ctx.fillRect(0, 0, width, height);

    ctx.shadowColor = '#06b6d4';
    ctx.shadowBlur = 25;
    ctx.strokeStyle = '#8b5cf6';
    ctx.lineWidth = 4;
    ctx.strokeRect(65, 65, width - 130, height - 130);
    ctx.shadowBlur = 0;

    ctx.font = '600 24px "Outfit", sans-serif';
    ctx.fillStyle = '#06b6d4';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`🎧 MUSIC & HARMONY • ${quoteObj.category.toUpperCase()}`, width / 2, 145);

    ctx.font = '600 46px "Outfit", sans-serif';
    ctx.fillStyle = '#ffffff';
    this.drawWrappedText(`"${quoteObj.quote}"`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '700 28px "Outfit", sans-serif';
    ctx.fillStyle = '#8b5cf6';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#9ca3af';
    ctx.fillText(`DAY ${quoteObj.day} OF 365`, width / 2, height - 90);
  }

  // 5. Wealth (Emerald Green & Pure Gold)
  renderWealthTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#041d15';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#d4af37';
    ctx.lineWidth = 3;
    ctx.strokeRect(65, 65, width - 130, height - 130);

    ctx.font = '600 24px "Cinzel", serif';
    ctx.fillStyle = '#d4af37';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`💎 WEALTH & LEVERAGE • ${quoteObj.category.toUpperCase()}`, width / 2, 145);

    ctx.font = '600 48px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#f4f6f0';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 20, width - 240, 66);

    ctx.font = '600 26px "Cinzel", serif';
    ctx.fillStyle = '#d4af37';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#7a9e8f';
    ctx.fillText(`DAY ${quoteObj.day} / 365`, width / 2, height - 90);
  }

  // 6. Fitness (Matte Charcoal & Blaze Orange)
  renderFitnessTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#111111';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#ff5722';
    ctx.lineWidth = 5;
    ctx.strokeRect(60, 60, width - 120, height - 120);

    ctx.font = '700 26px "Outfit", sans-serif';
    ctx.fillStyle = '#ff5722';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`⚡ DISCIPLINE & POWER • [ ${quoteObj.category.toUpperCase()} ]`, width / 2, 140);

    ctx.font = '700 48px "Outfit", sans-serif';
    ctx.fillStyle = '#ffffff';
    this.drawWrappedText(`"${quoteObj.quote.toUpperCase()}"`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '700 28px "Outfit", sans-serif';
    ctx.fillStyle = '#ff5722';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '500 20px "Outfit", sans-serif';
    ctx.fillStyle = '#888';
    ctx.fillText(`DAY ${quoteObj.day} • 365`, width / 2, height - 90);
  }

  // 7. Tech & Systems (Cyber Slate & Matrix Green)
  renderTechTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#09101d';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 3;
    ctx.strokeRect(65, 65, width - 130, height - 130);

    ctx.font = '600 22px "Courier New", monospace';
    ctx.fillStyle = '#10b981';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`> TECH_SYSTEMS :: ${quoteObj.category.toUpperCase()}`, width / 2, 145);

    ctx.font = '600 46px "Outfit", sans-serif';
    ctx.fillStyle = '#e2e8f0';
    this.drawWrappedText(`"${quoteObj.quote}"`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '600 26px "Courier New", monospace';
    ctx.fillStyle = '#10b981';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`DAY ${quoteObj.day} / 365`, width / 2, height - 90);
  }

  // 8. Books & Philosophy (Vintage Parchment & Ink Charcoal)
  renderBooksTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#f4ecd8';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#8c6d1f';
    ctx.lineWidth = 3;
    ctx.strokeRect(70, 70, width - 140, height - 140);

    ctx.font = '600 24px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#8c6d1f';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`📖 PHILOSOPHY & BOOKS • ${quoteObj.category.toUpperCase()}`, width / 2, 150);

    ctx.font = '600 48px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#1a1a1a';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 20, width - 240, 66);

    ctx.font = '600 26px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText(handle, width / 2, height - 140);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#8c6d1f';
    ctx.fillText(`DAY ${quoteObj.day} / 365`, width / 2, height - 100);
  }

  // 9. Peace & Psychology (Midnight Sky & Soft Rose)
  renderPeaceTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#0b1324';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#f472b6';
    ctx.lineWidth = 3;
    ctx.strokeRect(65, 65, width - 130, height - 130);

    ctx.font = '600 24px "Outfit", sans-serif';
    ctx.fillStyle = '#f472b6';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`🕊️ PEACE & CLARITY • ${quoteObj.category.toUpperCase()}`, width / 2, 145);

    ctx.font = '500 48px "Playfair Display", Georgia, serif';
    ctx.fillStyle = '#f3f4f6';
    this.drawWrappedText(`“${quoteObj.quote}”`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '600 26px "Outfit", sans-serif';
    ctx.fillStyle = '#f472b6';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '400 20px "Outfit", sans-serif';
    ctx.fillStyle = '#94a3b8';
    ctx.fillText(`DAY ${quoteObj.day} OF 365`, width / 2, height - 90);
  }

  // 10. Productivity & Life Hacks (Clean White & Jet Black)
  renderProductivityTheme(quoteObj, handle) {
    const { ctx, width, height } = this;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth = 4;
    ctx.strokeRect(60, 60, width - 120, height - 120);

    ctx.font = '700 24px "Outfit", sans-serif';
    ctx.fillStyle = '#2563eb';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`⚡ PRODUCTIVITY HACK • ${quoteObj.category.toUpperCase()}`, width / 2, 140);

    ctx.font = '600 48px "Inter", sans-serif';
    ctx.fillStyle = '#0f172a';
    this.drawWrappedText(`"${quoteObj.quote}"`, width / 2, height / 2 - 20, width - 240, 64);

    ctx.font = '700 26px "Outfit", sans-serif';
    ctx.fillStyle = '#0f172a';
    ctx.fillText(handle, width / 2, height - 130);

    ctx.font = '500 20px "Outfit", sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText(`DAY ${quoteObj.day} / 365`, width / 2, height - 90);
  }

  drawWrappedText(text, x, startY, maxWidth, lineHeight) {
    const { ctx } = this;
    const words = text.split(' ');
    let lines = [];
    let currentLine = '';

    for (let word of words) {
      let testLine = currentLine ? `${currentLine} ${word}` : word;
      let metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && currentLine) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    }
    lines.push(currentLine);

    const totalHeight = lines.length * lineHeight;
    let y = startY - (totalHeight / 2) + (lineHeight / 2);

    for (let line of lines) {
      ctx.fillText(line, x, y);
      y += lineHeight;
    }
  }

  downloadImage(filename = 'instagram_quote.png') {
    const link = document.createElement('a');
    link.download = filename;
    link.href = this.canvas.toDataURL('image/png', 1.0);
    link.click();
  }
}
