/* ═══════════════════════════════════════════════════════
   Road Accident Severity Prediction — Frontend JS
   ═══════════════════════════════════════════════════════ */

// Animate stat cards on page load
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.stat-card, .glass-card, .eda-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.5s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, i * 80);
  });
});
