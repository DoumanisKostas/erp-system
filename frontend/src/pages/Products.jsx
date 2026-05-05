import { useEffect, useState } from "react";

export default function Products() {
  const [products, setProducts] = useState([]);

  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editStock, setEditStock] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/products/")
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
      })
      .catch((err) => console.error(err));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch(
      `http://127.0.0.1:8000/products/?name=${name}&price=${price}&stock=${stock}`,
      {
        method: "POST",
      }
    )
      .then((res) => res.json())
      .then((newProduct) => {
        setProducts((prev) => [...prev, newProduct]);

        setName("");
        setPrice("");
        setStock("");
      })
      .catch((err) => console.error(err));
  };

  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:8000/products/${id}`, {
      method: "DELETE",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot delete product");
        }

        setProducts((prev) => prev.filter((p) => p.id !== id));
      })
      .catch((err) => {
        alert("This product cannot be deleted (maybe used in sales)");
        console.error(err);
      });
  };

  const handleEdit = (product) => {
    setEditingId(product.id);
    setEditName(product.name);
    setEditPrice(product.price);
    setEditStock(product.stock);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditName("");
    setEditPrice("");
    setEditStock("");
  };

  const handleUpdate = (id) => {
    fetch(
      `http://127.0.0.1:8000/products/${id}?name=${editName}&price=${editPrice}&stock=${editStock}`,
      {
        method: "PUT",
      }
    )
      .then((res) => res.json())
      .then((updatedProduct) => {
        setProducts((prev) =>
          prev.map((p) => (p.id === id ? updatedProduct : p))
        );

        handleCancelEdit();
      })
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <h1>Products</h1>

      <form onSubmit={handleSubmit} className="form">
        <h2>Add Product</h2>

        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Stock"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          required
        />

        <button type="submit">Add</button>
      </form>

      {products.length === 0 ? (
        <p>No products found</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Price (€)</th>
              <th>Stock</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>

                <td>
                  {editingId === p.id ? (
                    <input
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                    />
                  ) : (
                    p.name
                  )}
                </td>

                <td>
                  {editingId === p.id ? (
                    <input
                      type="number"
                      value={editPrice}
                      onChange={(e) => setEditPrice(e.target.value)}
                    />
                  ) : (
                    p.price
                  )}
                </td>

                <td>
                  {editingId === p.id ? (
                    <input
                      type="number"
                      value={editStock}
                      onChange={(e) => setEditStock(e.target.value)}
                    />
                  ) : (
                    p.stock
                  )}
                </td>

                <td>
                  {editingId === p.id ? (
                    <>
                      <button onClick={() => handleUpdate(p.id)}>Save</button>
                      <button onClick={handleCancelEdit}>Cancel</button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => handleEdit(p)}>Edit</button>
                      <button
                        onClick={() => handleDelete(p.id)}
                        className="delete-btn"
                      >
                        Delete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}