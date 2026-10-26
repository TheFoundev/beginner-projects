const links = document.querySelectorAll('.social-link');

links.forEach(link => {
  link.addEventListener('click', function(e) {
    const tooltip = this.getAttribute('data-tooltip');
    alert(`${tooltip}: ${this.href}`);
  });
});

const deployTime = document.getElementById('deployTime');
if (deployTime) {
  const now = new Date();
  deployTime.textContent = 'Updated: ' + now.toLocaleTimeString();
}

console.log('Link-in-Bio page loaded. Auto-deployed via GitHub Actions.');