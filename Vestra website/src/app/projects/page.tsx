import SharedNavbar from "@/components/sections/SharedNavbar";
import ProjectGrid from "@/components/sections/ProjectGrid";
import OutroCTA from "@/components/sections/OutroCTA";
import SharedFooter from "@/components/sections/SharedFooter";

export default function ProjectsPage() {
  return (
    <main className="bg-white">
      <SharedNavbar />
      <ProjectGrid />
      <OutroCTA />
      <SharedFooter />
    </main>
  );
}
