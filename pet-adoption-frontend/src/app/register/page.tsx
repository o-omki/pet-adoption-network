"use client";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import Link from "next/link";
import { useState } from "react";
import config from "@//resources/config"; // Adjust path as needed

export default function Register() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onSubmit = async (data: any) => {
    setLoading(true);
    setErrorMessage("");

    // Build payload for your backend
    const payload = {
      username: data.username,
      password: data.password,
      email: data.email,
      role: "adopter", // static role for now
      additional_info: {} // default empty object
    };

    try {
      const response = await fetch(`${config.BASE_URL}/api/v1/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
console.log(payload);
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message);
      }

      // Redirect after successful registration
      window.location.href = "/login";
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      setErrorMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex justify-center items-center min-h-screen bg-gray-100 px-6"
    >
      <div className="bg-white shadow-xl rounded-2xl p-12 max-w-lg w-full transition transform hover:shadow-2xl">
        
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Create an Account 🐾
        </h2>

        {errorMessage && (
          <p className="text-red-500 text-center mb-4">{errorMessage}</p>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Username Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Username</label>
            <input
              type="text"
              {...register("username", { required: "Username is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.username && <p className="text-red-500 text-sm mt-1"></p>}
          </div>

          {/* Email Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Email</label>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.email && <p className="text-red-500 text-sm mt-1"></p>}
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Password</label>
            <input
              type="password"
              {...register("password", { 
                required: "Password is required", 
                minLength: { value: 6, message: "Password must be at least 6 characters" } 
              })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.password && <p className="text-red-500 text-sm mt-1"></p>}
          </div>

          {/* Submit Button */}
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-purple-600 text-white py-4 rounded-2xl text-xl font-semibold hover:bg-purple-700 transition"
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="mt-6 text-center text-md text-gray-600">
          Already have an account?  
          <Link href="/login" className="text-purple-600 hover:underline ml-1 font-medium">Login</Link>
        </p>
      </div>
    </motion.div>
  );
}
