"use client";

import React from "react";

const AboutPage = () => {
  return (
    <div className="min-h-screen mt-15 py-12 px-6 md:px-16 bg-white text-gray-800 w-full">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-purple-700 mb-6 text-center">
          🐾 About This Project
        </h1>

        <p className="text-lg mb-10 text-center">
          A group of four tech-savvy M.Tech students came together with one goal — to
          build a digital space where <strong>compassion meets code</strong>. From idea to deployment,
          each team member played a vital role in making <em>Pawsitive 🐾🏡</em> a reality.
        </p>

        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold text-purple-600">🔧 Omkar D Murty</h2>
            <p className="text-md text-gray-700">
              <strong>Backend Developer</strong> — Developed the core backend services using <strong>Python FastAPI</strong>, enabling fast
              and efficient data handling. Hosted on <strong>Replit</strong> for smooth integration and testing.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-purple-600">🗄️ Shivangi Tayal</h2>
            <p className="text-md text-gray-700">
              <strong>Database Designer & Manager</strong> — Designed a normalized PostgreSQL schema and managed data access.
              Used <strong>Supabase</strong> for real-time, hosted database services.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-purple-600">💻 Sibin Mathew & Abhishek Shekhawat</h2>
            <p className="text-md text-gray-700">
              <strong>Frontend Developers</strong> — Designed and built the user-facing side of the platform using
              <strong> Next.js</strong> and <strong>Tailwind CSS</strong>. Ensured smooth navigation, responsiveness, and a
              delightful user experience across devices.
            </p>
          </div>
        </div>

        <div className="mt-12">
          <h2 className="text-2xl font-bold text-purple-700 mb-4">🏡 What is PAWSITIVE?</h2>
          <p className="text-md text-gray-700 mb-4">
            <em>PAWSITIVE 🐾🏡</em> is a platform designed to help pets in need find forever homes.
            It simplifies the pet adoption process while celebrating every success story. The platform offers:
          </p>
          <ul className="list-disc pl-6 space-y-1 text-gray-700">
            <li>🐶 A gallery of lovable pets ready for adoption</li>
            <li>📝 A simple, secure form to request adoption</li>
            <li>📖 A heartfelt blog — <strong>PawBlog</strong> — where adopters share their happy stories</li>
            <li>🔐 Secure authentication using access tokens</li>
            <li>📱 Fully responsive UI for a smooth mobile & desktop experience</li>
          </ul>
        </div>

        <blockquote className="mt-10 border-l-4 border-purple-500 pl-4 italic text-purple-700">
          Our mission is simple: Leverage our tech skills to bring more tails into happy homes.
        </blockquote>
      </div>
    </div>
  );
};

export default AboutPage;
