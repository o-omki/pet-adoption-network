"use client";
import { useState } from "react";
import { motion } from "framer-motion";

export default function PetDetails() {
  const [formData, setFormData] = useState({ name: "", address: "", phone: "" });
  const [submitted, setSubmitted] = useState(false);

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted Application:", formData);
    setSubmitted(true);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gray-100 flex justify-center items-center px-4"
    >
      {/* Grid Container */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full max-w-6xl">
        
        {/* Pet Info Card */}
        <div className="bg-white shadow-lg rounded-2xl p-6 w-full">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
            <img
              src="/pet-photo.jpg"
              alt="Pet"
              className="w-56 h-56 object-cover rounded-xl"
            />
            <div className="text-center md:text-left">
              <h2 className="text-3xl font-bold mb-2">Coco</h2>
              <p><strong>Type:</strong> Dog</p>
              <p><strong>Breed:</strong> Labrador</p>
              <p><strong>Age:</strong> 2 years</p>
              <p><strong>Gender:</strong> Female</p>
              <p className="mt-2"><strong>Description:</strong> Friendly and energetic, great with kids.</p>
              <p className="mt-2 text-purple-600 font-semibold"><strong>Status:</strong> Available</p>
            </div>
          </div>
        </div>

        {/* Adoption Form */}
        <div className="bg-white shadow-lg rounded-2xl p-6 w-full">
          <h3 className="text-xl font-semibold mb-4 text-center">Adoption Application Form 📝</h3>
          {!submitted ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleFormChange}
                className="w-full px-4 py-2 border rounded-lg"
                required
              />
              <input
                type="text"
                name="address"
                placeholder="Address"
                value={formData.address}
                onChange={handleFormChange}
                className="w-full px-4 py-2 border rounded-lg"
                required
              />
              <input
                type="text"
                name="phone"
                placeholder="Phone Number"
                value={formData.phone}
                onChange={handleFormChange}
                className="w-full px-4 py-2 border rounded-lg"
                required
              />
              <button
                type="submit"
                className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition"
              >
                Submit Application
              </button>
            </form>
          ) : (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-green-600 text-center font-medium text-lg"
            >
              ✅ Your application has been submitted!
            </motion.p>
          )}
        </div>
      </div>
    </motion.div>
  );
}
