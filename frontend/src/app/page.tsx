import Image from "next/image";
import Link from "next/link";
import HomeBar from "@/components/HomeBar";

export function GraphIframe() {
  return (
    <iframe
      src="http://localhost:8000/graph"
      style={{ width: "100%", height: 600, border: 0 }}
      title="graph"
    />
  );
}

async function callBackend() {
  const params = new URLSearchParams({
    text: "/Users/xiangzhousun/Documents/GitHub/BrainBox/backend/script.txt",
    meeting_name: "Example Meeting",
    speaker_name: "John Doe",
  });

try {
  const response = await fetch(`http://localhost:8000/transcript?${params.toString()}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  alert(data.message);
} catch (error) {
  console.error("Error calling backend:", error);
  alert("Failed to call backend. Check the console for details.");
}
}
callBackend()

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
            The agentic database for enterprise knowledge.
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
          <GraphIframe />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-lg border-t border-white/10 text-gray-300 py-4 text-center text-sm">
        <p>&copy; 2025 BrainBox. All rights reserved.</p>
      </footer>
    </div>
  );
}