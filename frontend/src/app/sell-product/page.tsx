"use client";
import { useState } from "react";

export default function SellProductPage() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    explanation: "",
    price: 0,
  });
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    setImageFile(file || null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageFile) {
      setMessage("Image is required");
      return;
    }

    const formData = new FormData();
    formData.append("username", form.username);
    formData.append("password", form.password);
    formData.append("explanation", form.explanation);
    formData.append("price", String(form.price));
    formData.append("image", imageFile);

    try {
      const res = await fetch("http://localhost:8000/products", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to add product");
      }
      setMessage("Product added successfully!");
      setForm({ username: "", password: "", explanation: "", price: 0 });
      setImageFile(null);
    } catch (err: any) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-xl">
      <h1 className="text-2xl font-semibold mb-6">Sell Product</h1>
      {message && <p className="mb-4 text-center text-red-500">{message}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          required
          placeholder="Username"
          name="username"
          value={form.username}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          type="password"
          placeholder="Password"
          name="password"
          value={form.password}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <textarea
          required
          placeholder="Short explanation of your product"
          name="explanation"
          value={form.explanation}
          onChange={handleChange}
          className="border p-2 rounded h-24"
        />
        <input
          required
          type="number"
          step="0.01"
          placeholder="Price"
          name="price"
          value={form.price}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-green-600 hover:bg-green-700 text-white py-2 rounded"
        >
          Submit Product
        </button>
      </form>
    </div>
  );
} 