"use client";

import { useState } from "react";
import Image from "next/image";
import logo from "@/resources/logo1.png"; // Sample image for now

// Sample Pet Data (Can be replaced with API data)
const pets = Array.from({ length: 20 }, (_, i) => ({
  id: i + 1,
  name: `Pet ${i + 1}`,
  type: i % 2 === 0 ? "Dog" : "Cat",
  age: `${1 + (i % 5)} years`,
  location: "City, Country",
  description: "This adorable pet is looking for a loving home! ❤️",
}));

export default function MainContent() {
  const [selectedFilter, setSelectedFilter] = useState("All");

  // Filter pets based on type
  const filteredPets = selectedFilter === "All" ? pets : pets.filter(pet => pet.type === selectedFilter);
  return (
    <div className="flex flex-col mt-15 items-center sm:items-start w-full">
      {/* Main Intro Section */}
      <main className="text-center sm:text-left p-4">
        <p className="text-lg font-medium leading-relaxed">
          Welcome to <span className="font-bold">PAWSITIVE</span> – Where Every Paw Finds a Home! 🐾🏡 <br />
          Looking for a loyal companion? A snuggle buddy? A playful friend? At PAWSITIVE, we connect loving hearts with adorable pets in need of a forever home. Start your journey today and make a difference—because every wag, purr, and happy tail deserves a second chance! ✨ <br />
          <span className="font-semibold">Adopt. Love. Repeat.</span> ✨🐶🐱 Meet Your New Best Friend Now!
        </p>
      </main>

      {/* Filter Buttons */}
      <div className="flex gap-4 my-4">
        {["All", "Dog", "Cat"].map(type => (
          <button
            key={type}
            className={`px-4 py-2 rounded-md font-semibold ${
              selectedFilter === type ? "bg-purple-600 text-white" : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setSelectedFilter(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Scrollable Pet Cards Panel */}
      <div className="w-full h-300 overflow-y-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4 bg-gray-50 rounded-lg shadow-md">
        {filteredPets.map(pet => (
          <div key={pet.id} className="bg-white shadow-lg rounded-lg p-4 flex flex-col items-center text-center">
            {/* Pet Image */}
            <Image src={logo} alt={pet.name} width={80} height={80} className="rounded-md" />

            {/* Pet Info */}
            <h3 className="text-lg font-semibold mt-2">{pet.name}</h3>
            <p className="text-gray-600 text-sm">{pet.type} - {pet.age}</p>
            <p className="text-gray-500 text-xs">{pet.location}</p>
            <p className="text-gray-700 text-sm mt-2">{pet.description}</p>

            {/* Adopt Button */}
            <button className="mt-3 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700">
              Adopt Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
