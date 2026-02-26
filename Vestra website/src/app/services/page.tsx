import SharedNavbar from "@/components/sections/SharedNavbar";
import Hero from "@/components/sections/hero";
import Showreel from "@/components/sections/showreel";
import Solutions from "@/components/sections/Solutions";
import Benefits from "@/components/sections/Benefits";
import Outro from "@/components/sections/outro";
import SharedFooter from "@/components/sections/SharedFooter";

export default function ServicesPage() {
  return (
    <main className="bg-white">
      <SharedNavbar />
      <Hero />
      <Showreel />
      <Solutions />
      <Benefits />
      <Outro />
      <SharedFooter />
    </main>
  );
}
