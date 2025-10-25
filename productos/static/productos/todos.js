  document.querySelectorAll('[data-collapse]').forEach(btn => {
    btn.addEventListener('click', () => {
      const body = btn.parentElement.querySelector('.facet__body');
      body.style.display = (body.style.display === 'none') ? '' : 'none';
    });
  });

  const cards = document.getElementById('cards');
  document.querySelectorAll('.view-btn').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.view-btn').forEach(x => x.classList.remove('is-active'));
      b.classList.add('is-active');
      const mode = b.getAttribute('data-view');
      cards.classList.toggle('grid', mode === 'grid');
      cards.classList.toggle('list', mode === 'list');
    });
  });

  document.querySelectorAll('.pricing .off').forEach(el => {
    const o = parseFloat(el.dataset.old || '0');
    const n = parseFloat(el.dataset.new || '0');
    if (o > n && o > 0) {
      const pct = Math.round((1 - (n/o))*100);
      el.textContent = `-${pct}%`;
    } else {
      el.remove();
    }
  });

  const btnCart     = document.getElementById('btnCart');
  const drawer      = document.getElementById('cartDrawer');
  const overlay     = document.getElementById('overlay');
  const closeCart   = document.getElementById('closeCart');
  const cartItems   = document.getElementById('cartItems');
  const subtotalEl  = document.getElementById('subtotal');
  const ivaEl       = document.getElementById('iva');
  const totalEl     = document.getElementById('total');
  const clearCartBtn= document.getElementById('clearCart');
  const cartCount   = document.getElementById('cartCount');

  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  function guardarCarrito(){ localStorage.setItem('cart', JSON.stringify(cart)); }

  function actualizarContador(){
    const total = cart.reduce((s,i)=> s + (i.qty||0), 0);
    if (cartCount) cartCount.textContent = total;
  }

  function renderCart(){
    if (!cartItems) return;

    cartItems.innerHTML = '';
    let subtotal = 0;

    cart.forEach(item => {
      subtotal += (item.price * item.qty);
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
    if (ivaEl)      ivaEl.textContent      = `Q${iva.toFixed(2)}`;
    if (totalEl)    totalEl.textContent    = `Q${total.toFixed(2)}`;

    actualizarContador();
    guardarCarrito();

    cartItems.querySelectorAll('[data-action]').forEach(btn => {
      btn.onclick = () => {
        const id = String(btn.dataset.id);
        const action = btn.dataset.action;
        const item = cart.find(i => i.id === id);
        if (!item) return;
        if (action === 'plus')  item.qty++;
        if (action === 'minus'){
          item.qty--;
          if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
        }
        renderCart();
      };
    });
  }

  function openCart(){
    drawer?.classList.add('open');
    overlay?.classList.add('active');
  }
  function closeCartFn(){
    drawer?.classList.remove('open');
    overlay?.classList.remove('active');
  }

  btnCart?.addEventListener('click', openCart);
  closeCart?.addEventListener('click', closeCartFn);
  overlay?.addEventListener('click', closeCartFn);
  clearCartBtn?.addEventListener('click', ()=>{ cart = []; renderCart(); });

  document.querySelectorAll('.card .add').forEach(btn => {
    btn.addEventListener('click', () => {
      const card = btn.closest('.card');
      if (!card) return;

      const id    = String(card.dataset.id || '');
      const name  = card.dataset.name || (card.querySelector('.name')?.textContent.trim() || 'Producto');
      const price = parseFloat(card.dataset.price || (card.querySelector('.pricing strong')?.textContent.replace(/[^\d.]/g,'') || '0')) || 0;

      if (!id) return;

      const existing = cart.find(i => i.id === id);
      if (existing) existing.qty++;
      else cart.push({ id, name, price, qty:1 });

  renderCart();
    });
  });

  renderCart();
const checkoutBtn = document.getElementById('checkout');
checkoutBtn?.addEventListener('click', () => {
  if (cart.length === 0) {
    alert('Tu carrito está vacío.');
    return;
  }

  fetch('/pedido/crear-desde-carrito/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(), 
    },
    body: JSON.stringify({ items: cart })
  })
  .then(response => {
    if (response.ok) {
      cart = [];
      guardarCarrito();
      renderCart();
      window.location.href = '/pedido/confirmado/';
    } else {
      alert('Error al procesar el pedido.');
    }
  });
});
function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(value);
  }
  return '';
}
