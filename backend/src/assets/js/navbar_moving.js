const mobileMenuButton = document.getElementById('mobile-menu-button')
const mobileMenu = document.getElementById('mobile-menu')

mobileMenuButton.addEventListener('click', function(event) {
  event.stopPropagation();  // Чтобы события не поднимались по родителям
  mobileMenu.classList.toggle('translate-y-full');
});

// Чтобы по клику за пределами всплывшего меню оно закрывалось
document.addEventListener('click', function(e) {
  if (!mobileMenu.contains(e.target)) {
    mobileMenu.classList.remove('translate-y-full');
  }
});
