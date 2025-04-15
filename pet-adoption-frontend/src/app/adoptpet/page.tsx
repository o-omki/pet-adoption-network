/* eslint-disable @next/next/no-img-element */
"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import config from "@/resources/config"; // BASE_URL

interface Pet {
  name: string;
  pet_type_name: string;
  breed_name: string;
  age: number;
  gender: string;
  description: string;
  image_url: string;
  status: string;
  pet_id: string;
}

export default function PetDetails() {
  const [formData, setFormData] = useState({
    name: "",
    address: "",
    phone: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [pet, setPet] = useState<Pet | null>(null);

  const searchParams = useSearchParams();
  const petId = searchParams.get("pet_id");

  useEffect(() => {
    async function fetchPetDetails() {
      if (!petId) return;
      try {
        const res = await fetch(`${config.BASE_URL}/api/v1/pets/${petId}`); // replace with actual endpoint
        const data = await res.json();
        setPet(data);
      } catch (err) {
        console.error("Failed to fetch pet data", err);
      }
    }

    fetchPetDetails();
  }, [petId]);

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!petId) return;

    try {
      const response = await fetch(`${config.BASE_URL}/api/v1/adoptions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`, // or however you're storing your auth token
        },
        body: JSON.stringify({
          pet_id: petId, // Send the petId as a string, not converted to Number
          message: `Hi, my name is ${formData.name}. I live at ${formData.address} and can be reached at ${formData.phone}. I would love to provide a loving home.`,
        }),
      });

      if (response.ok) {
        setSubmitted(true);
      } else if (response.status === 401) {
        alert("⚠️ Unauthorized: Please log in to apply for adoption.");
      } else {
        alert("❌ Failed to submit adoption request. Please try again.");
      }
    } catch (err) {
      console.error("Error submitting application:", err);
      alert("Something went wrong. Please try again later.");
    }
  };

  if (!pet) return <p className="text-center mt-10">Loading pet details...</p>;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gray-100 flex justify-center items-center px-4"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full max-w-6xl">
        {/* Pet Info */}
        <div className="bg-white shadow-lg rounded-2xl p-6 w-full">
          <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
            <img
              src={`/pet_images/${pet.pet_id}.jpg`}
              alt={pet.name}
              className="w-56 h-56 object-cover rounded-xl"
            />
            <div className="text-center md:text-left">
              <h2 className="text-3xl font-bold mb-2">{pet.name}</h2>
              <p>
                <strong>Type:</strong> {pet.pet_type_name}
              </p>
              <p>
                <strong>Breed:</strong> {pet.breed_name}
              </p>
              <p>
                <strong>Age:</strong> {pet.age}{" "}
                {pet.age === 1 ? "year" : "years"}
              </p>
              <p>
                <strong>Gender:</strong> {pet.gender}
              </p>
              <p className="mt-2">
                <strong>Description:</strong> {pet.description}
              </p>
              <p className="mt-2 text-purple-600 font-semibold">
                <strong>Status:</strong> {pet.status}
              </p>
            </div>
          </div>
        </div>

        {/* Form */}
        <div className="bg-white shadow-lg rounded-2xl p-6 w-full">
          <h3 className="text-xl font-semibold mb-4 text-center">
            Adoption Application Form 📝
          </h3>
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
              {/* Error message for invalid phone number */}
              {formData.phone &&
                (formData.phone.length < 10 || formData.phone.length > 10) && (
                  <p className="text-red-600 text-sm">
                    Phone number must be exactly 10 digits.
                  </p>
                )}
              <button
                type="submit"
                className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition"
                disabled={formData.phone.length !== 10} // Disable submit if phone number is invalid
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
