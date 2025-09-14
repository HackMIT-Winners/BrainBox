"use client";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";

export default function HomeBar() {
  const pathname = usePathname();

  return (
    <header className="w-full py-6 flex items-center justify-between px-8 bg-black/30 backdrop-blur-lg border-b border-white/10">
      <div className="flex items-center">
        <Link href="/" className="flex items-center">
          <Image
            src="/brainboxlogo.png"
            alt="BrainBox Logo"
            width={48}
            height={48}
            className="object-contain mr-3"
            priority
          />
        </Link>
      </div>
      <nav className="flex gap-4 items-center">
        {pathname !== "/" && (
          <Link
            href="/"
            className="bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-2 px-6 rounded-full shadow transition-colors"
          >
            Home
          </Link>
        )}
        {pathname !== "/calendar" && (
          <Link
            href="/calendar"
            className="bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 px-6 rounded-full shadow transition-colors"
          >
            Calendar
          </Link>
        )}
        <span className="ml-6 text-white text-base cursor-pointer hover:underline">
          Log In
        </span>
        <span className="ml-2 text-white text-base cursor-pointer hover:underline">
          Sign up
        </span>
      </nav>
    </header>
  );
}