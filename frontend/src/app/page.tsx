import Image from "next/image";
import Link from "next/link";
import HomeBar from "@/components/HomeBar";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <HomeBar />
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center relative overflow-hidden" style={{ minHeight: "60vh" }}>
        <div className="absolute inset-0 backdrop-blur-2xl bg-white/5 border border-white/10 rounded-3xl m-6 shadow-2xl" />
        <div className="relative z-10 text-center px-6 max-w-3xl">
          <div className="w-40 h-40 mx-auto mb-8 relative">
            <Image
              src="/brainboxlogo.png"
              alt="BrainBox Logo"
              fill
              className="object-contain drop-shadow-lg"
            />
          </div>
          <h1 className="text-6xl md:text-7xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-pink-400">
            Welcome to BrainBox
          </h1>
          <p className="mt-6 text-2xl md:text-3xl text-gray-300">
            Your AI-powered assistant for all your needs.
          </p>
        </div>
      </section>

      {/* Calendar Button Section */}
      <section className="flex justify-center my-12">
        <Link
          href="/calendar"
          className="inline-block bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-4 px-12 rounded-full shadow-lg transition-colors text-xl"
        >
          Open Calendar
        </Link>
      </section>

      {/* Knowledge Network Section */}
      <section className="flex flex-col items-center justify-center py-28 px-4">
        <h2 className="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-indigo-400">
          Knowledge Network
        </h2>
        <div className="w-full max-w-4xl flex flex-col items-center">
          {/* Placeholder for future graphic */}
          <div className="w-full h-64 bg-white/10 border border-white/10 rounded-2xl flex items-center justify-center mb-6">
            <span className="text-gray-400 text-xl">[Knowledge Network Graphic Coming Soon]</span>
          </div>
          <p className="text-lg text-gray-300 text-center max-w-2xl">
            The Knowledge Network will visualize and connect your ideas, resources, and insights—helping you discover, organize, and grow your knowledge like never before.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-lg border-t border-white/10 text-gray-300 py-4 text-center text-sm">
        <p>&copy; 2025 BrainBox. All rights reserved.</p>
      </footer>
    </div>
  );
}