
export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <a
            className=" flex items-center justify-center  font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
          >

Welcome to PAWSITIVE – Where Every Paw Finds a Home! 🐾🏡

Looking for a loyal companion? A snuggle buddy? A playful friend? At PAWSITIVE, we connect loving hearts with adorable pets in need of a forever home. Start your journey today and make a difference—because every wag, purr, and happy tail deserves a second chance!

✨ Adopt. Love. Repeat. ✨

🐶🐱 Meet Your New Best Friend Now!
          </a>
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
        >
          Pet Adoption Network
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
        >
          About →
        </a>
      </footer>
    </div>
  );
}
