"use client";
import { useState } from "react";

interface Product {
  product_id: number;
  product_name: string;
  price: number;
  purchase_count: number;
}

export default function DashboardPage() {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [data, setData] = useState<{
    products: Product[];
    total_sales: number;
    total_revenue: number;
  } | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await fetch("http://localhost:8000/sellers/products", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: credentials.username,
          password: credentials.password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to fetch products");
      }
      setData(data);
    } catch (err: any) {
      setMessage(err.message);
    }
  };

  const handleDelete = async (product_id: number) => {
    try {
      const res = await fetch(`http://localhost:8000/products/${product_id}?username=${credentials.username}&password=${credentials.password}`, {
        method: "DELETE",
      });
      const dataRes = await res.json();
      if (!res.ok) {
        throw new Error(dataRes.detail || "Delete failed");
      }
      setData((prev) =>
        prev
          ? {
              ...prev,
              products: prev.products.filter((p) => p.product_id !== product_id),
            }
          : prev
      );
    } catch (err: any) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-semibold mb-6">Seller Dashboard</h1>
      <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
        <input
          required
          placeholder="Username"
          name="username"
          value={credentials.username}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          type="password"
          placeholder="Password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 rounded"
        >
          See Products
        </button>
      </form>
      {message && <p className="text-red-500 mb-4">{message}</p>}
      {data && (
        <div className="space-y-4">
          <p>Total Sales: {data.total_sales}</p>
          <p>Total Revenue: ${data.total_revenue.toFixed(2)}</p>
          <div className="overflow-x-auto">
            <table className="min-w-full border">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2">Product Name</th>
                  <th className="p-2">Price</th>
                  <th className="p-2">Sold</th>
                  <th className="p-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.products.map((p) => (
                  <tr key={p.product_id} className="border-t">
                    <td className="p-2">{p.product_name}</td>
                    <td className="p-2">${p.price}</td>
                    <td className="p-2">{p.purchase_count}</td>
                    <td className="p-2">
                      <button
                        onClick={() => handleDelete(p.product_id)}
                        className="text-red-600 hover:underline"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
} 