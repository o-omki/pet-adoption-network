"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Filter, ChevronDown, ChevronUp, PawPrint, Baby } from "lucide-react";

export default function Leftpanel() {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    type: false,
    age: false,
  });

  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);

  const filters = [
    {
      category: "Animal Type",
      id: "type",
      icon: <PawPrint className="w-5 h-5" />,
      subFilters: ["Dogs", "Cats"],
    },
    {
      category: "Age",
      id: "age",
      icon: <Baby className="w-5 h-5" />,
      subFilters: ["1yrs", "2yrs", "3yrs", "4yrs", "5yrs"],
    },
  ];

  const toggleSection = (id: string) => {
    setOpenSections((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleFilter = (filter: string) => {
    setSelectedFilters((prev) =>
      prev.includes(filter) ? prev.filter((f) => f !== filter) : [...prev, filter]
    );
  };

  return (
    <aside className="bg-white shadow-md rounded-xl p-4 hidden sm:block w-full max-w-[250px]">
      {/* Header */}
      <div className="flex items-center justify-between text-gray-700 font-semibold">
        <span className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-purple-500" />
          Filters
        </span>
      </div>

      {/* Filter Categories */}
      {filters.map((filter) => (
        <div key={filter.id} className="mt-4">
          {/* Category Header */}
          <div
            className="flex justify-between items-center cursor-pointer text-gray-700 font-medium"
            onClick={() => toggleSection(filter.id)}
          >
            <span className="flex items-center gap-2">{filter.icon} {filter.category}</span>
            {openSections[filter.id] ? <ChevronUp className="w-5 h-5 text-gray-600" /> : <ChevronDown className="w-5 h-5 text-gray-600" />}
          </div>

          {/* Sub-Filters (Collapsible) */}
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: openSections[filter.id] ? "auto" : 0, opacity: openSections[filter.id] ? 1 : 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <ul className="mt-2 space-y-2 pl-4 text-gray-600">
              {filter.subFilters.map((subFilter) => (
                <li
                  key={subFilter}
                  className={`flex items-center gap-2 p-2 rounded-md cursor-pointer transition-colors ${
                    selectedFilters.includes(subFilter) ? "bg-purple-100 text-purple-600 font-semibold" : "hover:text-purple-600"
                  }`}
                  onClick={() => toggleFilter(subFilter)}
                >
                  {subFilter}
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      ))}
    </aside>
  );
}
