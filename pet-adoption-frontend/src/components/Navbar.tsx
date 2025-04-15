"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Menu, X } from "lucide-react";

import logo from '@/resources/logo1.png';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white py-3 shadow-md w-full fixed top-0 left-0 z-50">
      <div className="container mx-auto flex justify-between items-center max-w-7xl px-4">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <Image 
            src={logo} 
            alt="logo"
            className="rounded-lg" 
            width={50} 
            height={0}
            priority
          />
          <Link href="/" className="text-lg font-medium flex items-center">
            PAWSITIVE 🐾🏡
          </Link>
        </div>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-4 text-sm font-medium">
          {/* <li><Link href="#">Pets</Link></li>
          <li><Link href="#">Pet Services</Link></li>
          <li><Link href="#">Breeds</Link></li>
          <li><Link href="#">Blog</Link></li>
          <li><Link href="#">Foods</Link></li>
          <li><Link href="#">List Your Pet</Link></li> */}
          <li><Link href="/login">Login</Link></li>
        </ul>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-black" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={25} /> : <Menu size={25} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <ul className="md:hidden bg-white text-purple-600 font-medium text-sm flex flex-col items-center py-3 space-y-3">
          {/* <li><Link href="#">Pets</Link></li>
          <li><Link href="#">Pet Services</Link></li>
          <li><Link href="#">Breeds</Link></li>
          <li><Link href="#">Blog</Link></li>
          <li><Link href="#">Foods</Link></li>
          <li><Link href="#">List Your Pet</Link></li> */}
          <li><Link href="/Login">Login</Link></li>
        </ul>
      )}
    </nav>
  );
};

export default Navbar;
