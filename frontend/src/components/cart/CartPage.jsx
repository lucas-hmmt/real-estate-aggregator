import React, { useEffect, useState } from 'react';
import { fetchCart, exportCartCsv, removeFromCart } from '../../api/cart';
import Card from '../ui/Card';
import Button from '../ui/Button';
import EmptyState from '../ui/EmptyState';
import LoadingState from '../ui/LoadingState';
import CartItemCard from './CartItemCard';

function CartPage() {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadCart = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await fetchCart();
      setCart(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError('Failed to load cart.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCart();
  }, []);

  const handleExport = async () => {
    try {
      await exportCartCsv();
    } catch (err) {
      console.error(err);
      alert('Failed to export cart.');
    }
  };

  const handleRemove = async (id) => {
    try {
      await removeFromCart(id);
      await loadCart();
    } catch (err) {
      console.error(err);
      alert('Failed to remove from cart.');
    }
  };

  if (loading) {
    return <LoadingState message="Loading cart…" />;
  }

  if (!cart.length) {
    return (
      <EmptyState
        title="Your cart is empty"
        description="Add buildings to your cart from the building detail page."
        actionLabel="Browse buildings"
        actionHref="/"
      />
    );
  }

  return (
    <section className="page-section">
      <div className="page-header">
        <div>
          <h1 className="page-title">Shopping cart</h1>
          <p className="page-subtitle">
            Listings you’ve added to your cart.
          </p>
        </div>
        <div className="page-header-meta">
          <Button variant="primary" onClick={handleExport}>
            Export cart (CSV)
          </Button>
        </div>
      </div>

      {error && (
        <Card>
          <p className="text-error">{error}</p>
        </Card>
      )}

      <div className="cart-list">
        {cart.map((item) => (
          <CartItemCard key={item.a_id} building={item} onRemove={handleRemove} />
        ))}
      </div>
    </section>
  );
}

export default CartPage;
