"use client";

import { useState } from "react";
import Image from "next/image";

import logo from '@/resources/pawsitive_logo.png'

export default function Rightpanel() {
  // Sample Pet Data (For demo purposes)
  const [selectedPet, setSelectedPet] = useState({
    name: "Buddy",
    type: "Dog",
    breed: "Golden Retriever",
    age: "2 Years",
    size: "Medium",
    location: "New York, NY",
    adoptionStatus: "Available",
    image: logo , // Replace with actual pet image
    description:
      "Buddy is a friendly and energetic Golden Retriever who loves playing fetch and cuddles. He is looking for a loving home!",
  });

  return (
    <aside className="bg-white shadow-md rounded-xl p-4 hidden sm:block w-full max-w-[250px]">
      <h2 className="text-xl font-semibold text-gray-800 mb-2">Pet Details</h2>

      {/* Pet Image */}
      <div className="w-full flex justify-center">
        <Image
          src={selectedPet.image}
          alt={selectedPet.name}
          width={120}
          height={120}
          className="rounded-md"
        />
      </div>

      {/* Pet Information */}
      <ul className="mt-3 text-gray-700 text-sm space-y-2">
        <li><strong>Name:</strong> {selectedPet.name}</li>
        <li><strong>Type:</strong> {selectedPet.type}</li>
        <li><strong>Breed:</strong> {selectedPet.breed}</li>
        <li><strong>Age:</strong> {selectedPet.age}</li>
        <li><strong>Size:</strong> {selectedPet.size}</li>
        <li><strong>Location:</strong> {selectedPet.location}</li>
        <li><strong>Status:</strong> 
          <span className={`ml-1 font-semibold ${
            selectedPet.adoptionStatus === "Available"
              ? "text-green-600"
              : "text-red-500"
          }`}>
            {selectedPet.adoptionStatus}
          </span>
        </li>
      </ul>

      {/* Adoption Button */}
      <button className="mt-4 w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition">
        Adopt {selectedPet.name}
      </button>
    </aside>
  );
}
