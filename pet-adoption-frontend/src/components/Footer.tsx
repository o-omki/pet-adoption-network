import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-white col-span-3 flex gap-6 flex-wrap items-center justify-center w-full h-12 fixed bottom-0 left-0 z-50 shadow-md">
      <p className="text-sm text-gray-700">© 2025 Pet Adoption Network</p>
      <Link 
        href="/about" 
        className="text-sm text-purple-700 hover:underline hover:underline-offset-4 transition" 
        aria-label="Learn more about this project"
      >
        About →
      </Link>
    </footer>
  );
}
