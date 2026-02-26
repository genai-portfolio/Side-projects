import SharedNavbar from "@/components/sections/SharedNavbar";
import AboutHero from "@/components/sections/hero";
import SplitShow from "@/components/sections/SplitShow";
import Stats from "@/components/sections/Stats";
import AwwwardsSection from "@/components/sections/Awwwards";
import Partners from "@/components/sections/Partners";
import Benefits from "@/components/sections/Benefits";
import AboutHistory from "@/components/sections/AboutHistory";
import OutroCTA from "@/components/sections/OutroCTA";
import SharedFooter from "@/components/sections/SharedFooter";

export default function AboutPage() {
  return (
    <main className="bg-white">
      <SharedNavbar />
      <AboutHero />
      <SplitShow />
      <Stats />
      <AwwwardsSection />
      <Partners />
      <Benefits />
      <AboutHistory />
      <OutroCTA />
      <SharedFooter />
    </main>
  );
}
