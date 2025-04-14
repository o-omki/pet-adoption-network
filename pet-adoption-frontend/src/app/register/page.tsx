"use client";
import { useForm } from "react-hook-form";
import { motion } from "framer-motion";
import Link from "next/link";

export default function Register() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data: any) => {
    console.log("Register Data:", data);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex justify-center items-center min-h-screen bg-gray-100 px-6"
    >
      <div className="bg-white shadow-xl rounded-2xl p-12 max-w-lg w-full transition transform hover:shadow-2xl">
        
        {/* Header Section */}
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Create an Account 🐾
        </h2>

        {/* Registration Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Full Name Input */}
          <div>
            <label className="block text-gray-700 font-medium text-lg">Full Name</label>
            <input
              type="text"
              {...register("name", { required: "Name is required" })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.name && <p className="text-red-500 text-sm mt-1"></p>}
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
              {...register("password", { required: "Password is required", minLength: { value: 6, message: "Password must be at least 6 characters" } })}
              className="w-full px-5 py-3 border rounded-2xl text-lg focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
            {errors.password && <p className="text-red-500 text-sm mt-1"></p>}
          </div>

          {/* Submit Button */}
          <button type="submit" className="w-full bg-purple-600 text-white py-4 rounded-2xl text-xl font-semibold hover:bg-purple-700 transition">
            Register
          </button>
        </form>

        {/* Login Link */}
        <p className="mt-6 text-center text-md text-gray-600">
          Already have an account?  
          <Link href="/login" className="text-purple-600 hover:underline ml-1 font-medium">Login</Link>
        </p>
      </div>
    </motion.div>
  );
}
