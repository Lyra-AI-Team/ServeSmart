"use client";
import { useState } from "react";

interface Product {
  product_id: number;
  seller_id: number;
  product_name: string;
  description: string;
  purchase_count: number;
  product_image_path: string | null;
  price: number;
  discount: number;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/products?query=${query}`);
      if (!res.ok) {
        throw new Error("Failed to fetch products");
      }
      const data = await res.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-semibold mb-6">Search Products</h1>
      <form onSubmit={handleSubmit} className="mb-6 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search product name"
          className="border p-2 rounded flex-grow"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
        >
          Search
        </button>
      </form>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {results.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {results.map((product) => (
            <div
              key={product.product_id}
              className="border rounded p-4 flex flex-col gap-2"
            >
              <h2 className="font-semibold text-lg">{product.product_name}</h2>
              <p className="text-sm text-gray-500">
                ID: {product.product_id} | Vendor: {product.seller_id}
              </p>
              <p>{product.description}</p>
              <p>
                Price: ${product.price} | Discount: ${product.discount}
              </p>
              <p>Purchased: {product.purchase_count} times</p>
              {product.product_image_path && (
                <img
                  src={`http://localhost:8000/${product.product_image_path}`}
                  alt={product.product_name}
                  className="w-full h-40 object-cover rounded"
                />
              )}
            </div>
          ))}
        </div>
      ) : (
        <p>No products found.</p>
      )}
    </div>
  );
} 