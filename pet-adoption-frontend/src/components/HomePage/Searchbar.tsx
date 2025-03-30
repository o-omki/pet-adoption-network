
export default function Searchbar() {
  return (
    <div >
      {/* Fixed Search Panel */}
      <div className="fixed top-18 left-1/2 transform -translate-x-1/2 w-full max-w-lg p-4 bg-white shadow-md rounded-md z-50">
        <input 
          type="text" 
          placeholder="Search for pets..." 
          className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>
    </div>
  );
}
