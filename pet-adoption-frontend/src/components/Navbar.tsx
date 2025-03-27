"use client";
import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="g-gradient-to-r from-purple-300 to-purple-500 p-4 shadow-md w-full fixed top-0 left-0 z-50">
      <div className="container mx-auto flex justify-between items-center max-w-7xl px-4">
        {/* Logo */}
        <Link href="/" className=" text-2xl font-bold flex items-center">
        PAWSITIVE 🐾🏡
        </Link>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-6 font-semibold">
          <li><Link href="#">Pets </Link></li>
          <li><Link href="#">Pet Services </Link></li>
          <li><Link href="#">Breeds </Link></li>
          <li><Link href="#">Blog </Link></li>
          <li><Link href="#">Foods </Link></li>
          <li><Link href="#">List Your Pet </Link></li>
          <li><Link href="#">Login </Link></li>
        </ul>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-white" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={30} /> : <Menu size={30} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <ul className="md:hidden bg-white text-purple-600 font-semibold flex flex-col items-center py-4 space-y-4">
          <li><Link href="#">Pets</Link></li>
          <li><Link href="#">Pet Services</Link></li>
          <li><Link href="#">Breeds</Link></li>
          <li><Link href="#">Blog</Link></li>
          <li><Link href="#">Foods</Link></li>
          <li><Link href="#">List Your Pet</Link></li>
          <li><Link href="#">Login</Link></li>
        </ul>
      )}
    </nav>
  );
};

export default Navbar;
