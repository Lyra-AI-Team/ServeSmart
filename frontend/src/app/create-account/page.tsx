/* eslint-disable @next/next/no-img-element */
"use client";
import { useState } from "react";

export default function CreateAccountPage() {
  const [form, setForm] = useState({
    user_name: "",
    identity_no: "",
    IBAN: "",
    business_address: "",
    e_mail: "",
    password: "",
  });
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    try {
      const res = await fetch("http://localhost:8000/sellers/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Registration failed");
      }
      setMessage("Account created successfully!");
      setForm({
        user_name: "",
        identity_no: "",
        IBAN: "",
        business_address: "",
        e_mail: "",
        password: "",
      });
    } catch (err: any) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-xl">
      <h1 className="text-2xl font-semibold mb-6">Create Seller Account</h1>
      {message && <p className="mb-4 text-center text-red-500">{message}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          required
          placeholder="Username"
          name="user_name"
          value={form.user_name}
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
          placeholder="IBAN"
          name="IBAN"
          value={form.IBAN}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="Business Address"
          name="business_address"
          value={form.business_address}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="Email"
          type="email"
          name="e_mail"
          value={form.e_mail}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          required
          placeholder="Password"
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
        >
          Create Account
        </button>
      </form>
    </div>
  );
} 