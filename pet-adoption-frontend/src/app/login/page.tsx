"use client";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import Link from "next/link";
import Image from "next/image";
import logo from "@/resources/logo.png";
import { useState } from "react";
import config from "@/resources/config"; 

export default function Login() {
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
  
    try {
      const formData = new FormData();
      formData.append("username", data.username);
      formData.append("password", data.password);
  console.log(config.BASE_URL);
      const response = await fetch(`${config.BASE_URL}/api/v1/auth/login`, {
        method: "POST",
        body: formData,
      });
  
      const result = await response.json();
  
      if (!response.ok) {
        throw new Error(result.message || "Login failed");
      }
  
      // ✅ Store the access_token only in localStorage
      localStorage.setItem("access_token", result.access_token);
  
      // Optionally: redirect user
      window.location.href = "/";
  
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
      className="flex items-center justify-center min-h-screen bg-gray-100 px-6"
    >
      <div className="bg-white shadow-xl rounded-3xl p-12 max-w-lg w-full transition transform hover:shadow-2xl">
        
        {/* Logo Section */}
        <div className="flex justify-center mb-8">
          <Image src={logo} alt="Pawsitive Logo" width={120} height={120} />
        </div>

        {/* Welcome Text */}
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Welcome Back! 🐾
        </h2>

        {/* Error Message */}
        {errorMessage && (
          <p className="text-red-500 text-center mb-4">{errorMessage}</p>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Username Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Username</label>
            <input
              type="text"
              {...register("username", { required: "Username is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.username && <p className="text-red-500 text-sm"></p>}
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Password</label>
            <input
              type="password"
              {...register("password", { required: "Password is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.password && <p className="text-red-500 text-sm"></p>}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-purple-600 text-white py-4 rounded-2xl text-xl font-semibold hover:bg-purple-700 transition"
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {/* Register Link */}
        <p className="mt-6 text-center text-md text-gray-600">
          Don't have an account?  
          <Link href="/register" className="text-purple-600 hover:underline ml-1 font-medium">Sign Up</Link>
        </p>
      </div>
    </motion.div>
  );
}
