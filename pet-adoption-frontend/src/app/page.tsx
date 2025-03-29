export default function Home() {
  return (
    <div className="grid grid-cols-[20%_70%_10%] min-h-screen p-8 pb-20 gap-4 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      {/* Left Sidebar */}
      <aside className="bg-gray-100 p-4 hidden sm:block"> {/* You can add navigation or filters here */} </aside>
      
      {/* Main Content */}
      <main className="flex flex-col gap-8 items-center sm:items-start relative">
        {/* Floating Search Bar */}
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-full max-w-lg p-4 bg-white shadow-md rounded-md">
          <input 
            type="text" 
            placeholder="Search for pets..." 
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        {/* Main Content Text */}
        <div className="flex gap-4 items-center flex-col sm:flex-row mt-16">
          <a className="flex items-center justify-center font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto">
            Welcome to PAWSITIVE – Where Every Paw Finds a Home! 🐾🏡
            Looking for a loyal companion? A snuggle buddy? A playful friend? At PAWSITIVE, we connect loving hearts with adorable pets in need of a forever home. Start your journey today and make a difference—because every wag, purr, and happy tail deserves a second chance!
            ✨ Adopt. Love. Repeat. ✨
            🐶🐱 Meet Your New Best Friend Now!
          </a>
        </div>
      </main>
      
      {/* Right Sidebar */}
      <aside className="bg-gray-100 p-4 hidden sm:block"> {/* You can add additional info or ads here */} </aside>
      
      {/* Footer */}
      <footer className="col-span-3 flex gap-6 flex-wrap items-center justify-center mt-8">
        <a className="flex items-center gap-2 hover:underline hover:underline-offset-4">Pet Adoption Network</a>
        <a className="flex items-center gap-2 hover:underline hover:underline-offset-4">About →</a>
      </footer>
    </div>
  );
}
