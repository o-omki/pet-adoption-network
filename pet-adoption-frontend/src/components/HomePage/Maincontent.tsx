
export default function maincontent() {
    return (
        <div>
        {/* Main Content */}
        <main className="flex flex-col gap-8 items-center sm:items-start relative">
          
          {/* Floating Search Bar
          <div className="w-full flex justify-center">
            <div className="w-full max-w-lg p-4 bg-white shadow-md rounded-md mt-4 sm:mt-0">
              <input 
                type="text" 
                placeholder="Search for pets..." 
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div> */}
  
          {/* Main Content Text */}
          <div className="flex gap-4 items-center flex-col sm:flex-row mt-8 sm:mt-16 text-center sm:text-left">
            <p className="text-lg font-medium leading-relaxed">
              Welcome to <span className="font-bold">PAWSITIVE</span> – Where Every Paw Finds a Home! 🐾🏡 <br />
              Looking for a loyal companion? A snuggle buddy? A playful friend? At PAWSITIVE, we connect loving hearts with adorable pets in need of a forever home. Start your journey today and make a difference—because every wag, purr, and happy tail deserves a second chance! ✨ <br />
              <span className="font-semibold">Adopt. Love. Repeat.</span> ✨🐶🐱 Meet Your New Best Friend Now!
            </p>
          </div>
        </main>
        </div>
    );
  }
  