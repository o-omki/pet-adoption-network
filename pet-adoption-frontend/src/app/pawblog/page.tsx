"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import config from "@/resources/config";
import { data } from "framer-motion/client";

export default function BlogPage() {
  const [stories, setStories] = useState([]);

  useEffect(() => {
    const fetchStories = async () => {
      try {
        const response = await fetch(`${config.BASE_URL}/api/v1/stories`);
        const data = await response.json();
        setStories(data);
      } catch (error) {
        console.error("Error fetching stories:", error);
      }
    };

    console.log(data)

    fetchStories();
  }, []);

  return (
    <main className="min-h-screen pt-24 px-6 bg-gray-50 mb-15">
      <h1 className="text-4xl font-bold text-center mb-10 text-purple-700">Adoption Stories</h1>

      <div className="grid gap-8 grid-cols-1 md:grid-cols-2 xl:grid-cols-2 max-w-6xl mx-auto">
        {stories.map((story: any, index) => (
          <div
            key={index}
            className="bg-white rounded-2xl shadow-lg p-6 flex flex-col h-full w-full transition hover:shadow-xl"
          >
            {story.image_url ? (
              <div className="w-full h-[300px] relative mb-4">
                <Image
                  src={story.image_url}
                  alt={story.story_title}
                  fill
                  className="rounded-lg object-cover"
                />
              </div>
            ) : null}

            <h2 className="text-2xl font-semibold text-purple-700 mb-2">{story.story_title}</h2>
            <p className="text-gray-700 text-base leading-relaxed">{story.story_content}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
