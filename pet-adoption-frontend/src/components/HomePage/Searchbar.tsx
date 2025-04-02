import { Search } from "lucide-react";

export default function Searchbar() {
  return (
    <div className="fixed top-20 left-1/2 transform -translate-x-1/2 w-full max-w-xl z-50">
      <div className="relative flex items-center w-full bg-white shadow-lg rounded-full px-5 py-2 border border-gray-300">
        <Search className="text-gray-500 w-5 h-5 absolute left-8" />
        <input
          type="text"
          placeholder="Search for pets..."
          className="w-full pl-10 pr-4 py-2 text-gray-700 bg-transparent rounded-full outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>
    </div>
  );
}
