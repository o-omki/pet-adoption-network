"use client";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import Link from "next/link";
import Image from "next/image";
import logo from "@/resources/logo.png"; // Update with correct path

export default function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data: any) => {
    console.log("Login Data:", data);
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

        {/* Login Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Email Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Email</label>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.email && <p className="text-red-500 text-sm"></p>}
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
          <button type="submit" className="w-full bg-purple-600 text-white py-4 rounded-2xl text-xl font-semibold hover:bg-purple-700 transition">
            Login
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
