"use client";
import { useState } from "react";

export default function BuyPage() {
  const [form, setForm] = useState({
    product_id: 0,
    identity_no: "",
    CVV: "",
    card_no: "",
    address: "",
    e_mail: "",
  });
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/purchase", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          product_id: Number(form.product_id),
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Purchase failed");
      }
      setMessage("Product purchased successfully!");
      setForm({
        product_id: 0,
        identity_no: "",
        CVV: "",
        card_no: "",
        address: "",
        e_mail: "",
      });
    } catch (err: any) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-xl">
      <h1 className="text-2xl font-semibold mb-6">Buy Product</h1>
      {message && <p className="mb-4 text-center text-red-500">{message}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          required
          type="number"
          placeholder="Product ID"
          name="product_id"
          value={form.product_id}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="Identity Number (11 digits)"
          name="identity_no"
          value={form.identity_no}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="CVV"
          name="CVV"
          value={form.CVV}
          maxLength={3}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="Card Number"
          name="card_no"
          value={form.card_no}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <textarea
          required
          placeholder="Address"
          name="address"
          value={form.address}
          onChange={handleChange}
          className="border p-2 rounded h-24"
        />
        <input
          required
          type="email"
          placeholder="Email"
          name="e_mail"
          value={form.e_mail}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded"
        >
          Buy Product
        </button>
      </form>
    </div>
  );
} 