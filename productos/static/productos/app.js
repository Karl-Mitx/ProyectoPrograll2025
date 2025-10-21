document.addEventListener('DOMContentLoaded', function() {

  const themeToggle = document.getElementById('themeToggle');

  function aplicarTemaGuardado() {
      let temaGuardado = localStorage.getItem('theme');
      if (!temaGuardado) {
          temaGuardado = 'dark';
      }
      document.documentElement.setAttribute('data-theme', temaGuardado);
  }

  function cambiarTema() {
      let temaActual = document.documentElement.getAttribute('data-theme');
      if (temaActual === 'light') {
          document.documentElement.setAttribute('data-theme', 'dark');
          localStorage.setItem('theme', 'dark');
      } else {
          document.documentElement.setAttribute('data-theme', 'light');
          localStorage.setItem('theme', 'light');
      }
  }

  if (themeToggle) {
      themeToggle.addEventListener('click', cambiarTema);
  }

  aplicarTemaGuardado();

  const btnCart = document.getElementById('btnCart');
  const drawer = document.getElementById('drawer');
  const closeCart = document.getElementById('closeCart');
  const cartItems = document.getElementById('cartItems');
  const subtotalEl = document.getElementById('subtotal');
  const ivaEl = document.getElementById('iva');
  const totalEl = document.getElementById('total');
  const clearCartBtn = document.getElementById('clearCart');
  const cartCount = document.getElementById('cartCount');
  const limpiarF = document.getElementById('limpiarF');
  const grid = document.getElementById('grid');

  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  function guardarCarrito() {
    localStorage.setItem('cart', JSON.stringify(cart));
  }

  function actualizarContador() {
    const total = cart.reduce(function(s, i) {
      return s + (i.qty || 0);
    }, 0);
    if (cartCount) cartCount.textContent = total;
  }

  function renderCart() {
    if (!cartItems) return;
    cartItems.innerHTML = '';
    let subtotal = 0;

    cart.forEach(function(item) {
      subtotal += item.price * item.qty;
      const div = document.createElement('div');
      div.className = 'item';
      div.innerHTML = `
        <div>${item.name}</div>
        <div class="qty">
          <button data-action="minus" data-id="${item.id}">-</button>
          <span>${item.qty}</span>
          <button data-action="plus" data-id="${item.id}">+</button>
        </div>
        <div>Q${(item.price * item.qty).toFixed(2)}</div>
      `;
      cartItems.appendChild(div);
    });

    const iva = subtotal * 0.12;
    const total = subtotal + iva;

    if (subtotalEl) subtotalEl.textContent = `Q${subtotal.toFixed(2)}`;
    if (ivaEl) ivaEl.textContent = `Q${iva.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `Q${total.toFixed(2)}`;

    actualizarContador();
    guardarCarrito();

    const botones = cartItems.querySelectorAll('[data-action]');
    botones.forEach(function(btn) {
      btn.onclick = function() {
        const id = this.dataset.id;
        const action = this.dataset.action;
        const item = cart.find(function(i) { return i.id === id; });
        if (!item) return;
        if (action === 'plus') item.qty++;
        if (action === 'minus') {
          item.qty--;
          if (item.qty <= 0) cart = cart.filter(function(i) { return i.id !== id; });
        }
        renderCart();
      };
    });
  }

  if (btnCart && drawer) btnCart.onclick = function() { drawer.classList.add('open'); };
  if (closeCart && drawer) closeCart.onclick = function() { drawer.classList.remove('open'); };
  if (clearCartBtn) clearCartBtn.onclick = function() { cart = []; renderCart(); };

  const botonesAgregar = document.querySelectorAll('[data-add]');
  botonesAgregar.forEach(function(btn) {
    btn.onclick = function() {
      const id = String(this.dataset.add);
      const card = this.closest('.card');
      const name = card ? (card.querySelector('.name')?.innerText || 'Producto') : 'Producto';
      const priceText = card ? (card.querySelector('.price')?.textContent.replace('Q','') || '0') : '0';
      const price = parseFloat(priceText) || 0;
      const existing = cart.find(function(i) { return i.id === id; });
      if (existing) existing.qty++;
      else cart.push({id, name, price, qty:1});
      renderCart();
    };
  });

  if (limpiarF) {
    limpiarF.addEventListener('click', async function(e) {
      e.preventDefault();

      const q = document.getElementById('q');
      const type = document.getElementById('type');
      const brand = document.getElementById('brand');
      const min = document.getElementById('min');
      const max = document.getElementById('max');
      const nuevo = document.getElementById('nuevo');
      const usado = document.getElementById('usado');
      const sort = document.getElementById('sort');

      if (q) q.value = '';
      if (type) type.selectedIndex = 0;
      if (brand) brand.selectedIndex = 0;
      if (min) min.value = '';
      if (max) max.value = '';
      if (nuevo) nuevo.checked = false;
      if (usado) usado.checked = false;
      if (sort) sort.selectedIndex = 0;

      const cleanUrl = window.location.protocol + '//' + window.location.host + window.location.pathname;
      history.replaceState({}, '', cleanUrl);
      if (!grid) return;

      try {
        const resp = await fetch(cleanUrl, {
          method: 'GET',
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (!resp.ok) throw new Error('fetch failed ' + resp.status);
        const text = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const newGrid = doc.getElementById('grid');
        if (newGrid) {
          grid.innerHTML = newGrid.innerHTML;
          const nuevosBotones = document.querySelectorAll('[data-add]');
          nuevosBotones.forEach(function(btn) {
            btn.onclick = function() {
              const id = String(this.dataset.add);
              const card = this.closest('.card');
              const name = card ? (card.querySelector('.name')?.innerText || 'Producto') : 'Producto';
              const priceText = card ? (card.querySelector('.price')?.textContent.replace('Q','') || '0') : '0';
              const price = parseFloat(priceText) || 0;
              const existing = cart.find(function(i) { return i.id === id; });
              if (existing) existing.qty++;
              else cart.push({id, name, price, qty:1});
              renderCart();
            };
          });
        }
      } catch (err) {
        console.warn('No se actualizó grid vía fetch:', err);
      }
    });
  }

  renderCart();
});