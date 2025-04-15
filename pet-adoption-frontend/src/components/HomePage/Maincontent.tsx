/* eslint-disable @next/next/no-img-element */
"use client";

import { useState, useEffect } from "react";
import config from "@/resources/config"; // BASE_URL
import logo from "@/resources/logo1.png"; // Fallback image
import Link from "next/link";

export default function MainContent() {
  // useEffect(() => {
  //   const token = localStorage.getItem("access_token");
  //   console.log("Access Token:", token);
  // }, []);
  const [pets, setPets] = useState<any[]>([]);
  const [selectedFilter, setSelectedFilter] = useState("All");

  // Fetch pets on load
  useEffect(() => {
    const fetchPets = async () => {
      try {
        const response = await fetch(`${config.BASE_URL}/api/v1/pets`);
        const data = await response.json();

        // ✅ Filter only Dog and Cat
        const filtered = data.filter(
          (pet: any) =>
            pet.pet_type_name === "Dog" || pet.pet_type_name === "Cat"
        );

        setPets(filtered);
      } catch (error) {
        console.error("Error fetching pets:", error);
      }
    };

    fetchPets();
  }, []);

  // Filter pets based on selected type
  const filteredPets =
    selectedFilter === "All"
      ? pets
      : pets.filter((pet) => pet.pet_type_name === selectedFilter);

  return (
    <div className="flex flex-col mt-1 items-center sm:items-start w-full">
      {/* Main Intro Section */}
      <main className="text-center sm:text-left p-4">
        <p className="text-lg font-medium leading-relaxed">
          Welcome to <span className="font-bold">PAWSITIVE</span> – Where Every
          Paw Finds a Home! 🐾🏡 <br />
          Looking for a loyal companion? A snuggle buddy? A playful friend? At
          PAWSITIVE, we connect loving hearts with adorable pets in need of a
          forever home. Start your journey today and make a difference—because
          every wag, purr, and happy tail deserves a second chance! ✨ <br />
          <span className="font-semibold">Adopt. Love. Repeat.</span> ✨🐶🐱
          Meet Your New Best Friend Now!
        </p>
      </main>

      {/* Filter Buttons */}
      <div className="flex gap-4 my-4">
        {["All", "Dog", "Cat"].map((type) => (
          <button
            key={type}
            className={`px-4 py-2 rounded-md font-semibold ${
              selectedFilter === type
                ? "bg-purple-600 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setSelectedFilter(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Pet Listings */}
      <div className="w-full h-300 overflow-y-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4 bg-gray-50 rounded-lg shadow-md">
        {filteredPets.map((pet) => {
          const imagePath =
            pet.breed_id != null
              ? `/pet_images/${pet.pet_id}.jpg` // adjust extension if needed
              : logo.src;

          return (
            <div
              key={pet.pet_id}
              className="bg-white shadow-lg rounded-lg p-4 flex flex-col items-center text-center"
            >
              {/* Pet Image - Using <img> instead of <Image> */}
              <img
                src={imagePath}
                alt={pet.name}
                width={120}
                height={120}
                className="rounded-md object-cover"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = logo.src;
                }}
              />

              {/* Pet Info */}
              <h3 className="text-lg font-semibold mt-2">{pet.name}</h3>
              <p className="text-gray-600 text-sm">
                {pet.pet_type_name} - {pet.age} years
              </p>
              <p className="text-gray-700 text-sm mt-2">{pet.description}</p>

              {/* Adopt Button */}
              <Link href={`/adoptpet?pet_id=${pet.pet_id}`}>
                <button className="mt-3 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700">
                  Adopt Now
                </button>
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
}
