import SharedNavbar from "@/components/sections/SharedNavbar";
import Hero from "@/components/sections/hero";
import ShowreelSection from "@/components/sections/showreel";
import AboutSummary from "@/components/sections/about-summary";
import FeaturedProjects from "@/components/sections/featured-projects";
import OurServices from "@/components/sections/our-services";
import Outro from "@/components/sections/outro";
import SharedFooter from "@/components/sections/SharedFooter";

export default function Home() {
  return (
    <main className="bg-white">
      <SharedNavbar />
      <Hero />
      <ShowreelSection />
      <AboutSummary />
      <FeaturedProjects />
      <OurServices />
      <Outro />
      <SharedFooter />
    </main>
  );
}
