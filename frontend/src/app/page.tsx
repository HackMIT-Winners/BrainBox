import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col" style={{ height: "310vh" }}>
      <div className="flex-1 bg-gray-900">

        <div className="flex flex-col items-center justify-center h-full text-white">
          <h1 className="text-4xl font-bold mb-4">Welcome to BrainBox</h1>
          <p className="text-lg mb-8">Your AI-powered assistant for all your needs</p>
          <p className="text-lg mb-8 text-center text-white">
        hello world
        <Link href="/calendar">Go to the calendar</Link>

        </p>
          <div className="w-48 h-48 relative">
            <Image
              src="/brainbox-logo.png"
              alt="BrainBox Logo"
              layout="fill"
              objectFit="contain"
            />
          </div>
        </div>

      </div>


      <div className="flex-1 bg-gray-200">

      </div>

      <div className="flex-1 bg-gray-500"></div>
      <footer className="bg-gray-800 text-white py-4">
        <div className="container mx-auto text-center">
          <p>&copy; 2025 BrainBox. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
