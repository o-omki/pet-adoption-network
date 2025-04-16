"use client";

import Image from "next/image";

const stories = [
  {
    pet_id: 1,
    adopter_id: 101,
    story_title: "A Purrfect Friendship",
    story_content:
      "When we adopted Luna, we had no idea how quickly she'd become part of our lives. Her playful nature and loving eyes brought warmth into our home. We can’t imagine life without her now!",
    image_url: "",
  },
  {
    pet_id: 2,
    adopter_id: 102,
    story_title: "Max's New Home",
    story_content:
      "Max was shy at first, but with a little love and a lot of treats, he opened up to us. Watching him run around the backyard with joy made every moment worth it.",
    image_url: "",
  },
  {
    pet_id: 3,
    adopter_id: 103,
    story_title: "Barking Up the Right Tree",
    story_content:
      "We had been searching for a loyal companion, and Buddy came into our lives just in time. His energy and loyalty have turned our house into a happy home.",
    image_url: "",
  },
  {
    pet_id: 4,
    adopter_id: 104,
    story_title: "Whiskers and Wonders",
    story_content:
      "Whiskers was rescued from the streets, and now she’s the queen of the couch. Her quirky habits and loud purring fill our home with charm and laughter.",
    image_url: "",
  },
  {
    pet_id: 5,
    adopter_id: 105,
    story_title: "From Shelter to Snuggles",
    story_content:
      "Rocky had a rough start, but his strength amazed us. Now he sleeps soundly by our side and greets us every day with a wagging tail and bright eyes.",
    image_url: "",
  },
];

export default function BlogPage() {
  return (
    <main className="min-h-screen pt-24 px-6 bg-gray-50">
      <h1 className="text-4xl font-bold text-center mb-10 text-purple-700">Adoption Stories</h1>

      <div className="grid gap-8 grid-cols-1 md:grid-cols-2 xl:grid-cols-2 max-w-6xl mx-auto">
        {stories.map((story, index) => (
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
