"use client";

import { useState } from "react";

export default function Rightpanel() {
  const [quote] = useState(
    "“Adopting a pet is not just about changing their life, it's about changing yours too.”"
  );

  return (
    <aside className="bg-white shadow-md rounded-xl p-6 w-full max-w-[250px] sticky top-20 max-h-[80vh] overflow-y-auto">
      <div className="bg-purple-100 p-6 rounded-lg shadow-lg">
        {/* Adoption Quote */}
        <p className="text-center text-2xl font-semibold text-purple-700">
          {quote}
        </p>

        {/* Footer or Signature for Quote */}
        <p className="text-center text-sm text-gray-600 mt-4">
          — Mathew
        </p>
      </div>
    </aside>
  );
}
