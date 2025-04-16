"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Menu, X } from "lucide-react";
import { useRouter } from "next/navigation";

import logo from "@/resources/logo1.png";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  // Check token on mount
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    router.push("/login");
  };

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
            height={50}
            priority
          />
          <Link href="/" className="text-lg font-semibold flex items-center">
            PAWSITIVE 🐾🏡
          </Link>
        </div>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-6 text-sm font-medium text-purple-700">
          <li>
            <Link href="/pawblog" className="hover:text-purple-900 transition">
              PawBlog
            </Link>
          </li>
          {isAuthenticated ? (
            <li>
              <button
                onClick={handleLogout}
                className="hover:text-purple-900 transition"
              >
                Logout
              </button>
            </li>
          ) : (
            <li>
              <Link href="/login" className="hover:text-purple-900 transition">
                Login
              </Link>
            </li>
          )}
        </ul>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-black"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          {isOpen ? <X size={25} /> : <Menu size={25} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <ul className="md:hidden bg-white text-purple-600 font-medium text-sm flex flex-col items-center py-4 space-y-3 shadow-md">
          <li>
            <Link
              href="/pawblog"
              onClick={() => setIsOpen(false)}
              className="hover:text-purple-900 transition"
            >
              PawBlog
            </Link>
          </li>
          {isAuthenticated ? (
            <li>
              <button
                onClick={() => {
                  handleLogout();
                  setIsOpen(false);
                }}
                className="hover:text-purple-900 transition"
              >
                Logout
              </button>
            </li>
          ) : (
            <li>
              <Link
                href="/login"
                onClick={() => setIsOpen(false)}
                className="hover:text-purple-900 transition"
              >
                Login
              </Link>
            </li>
          )}
        </ul>
      )}
    </nav>
  );
};

export default Navbar;
