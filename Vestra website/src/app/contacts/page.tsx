import SharedNavbar from "@/components/sections/SharedNavbar";
import ContactForm from "@/components/sections/contact-form";
import StickyContactWidget from "@/components/sections/sticky-contact-widget";
import SharedFooter from "@/components/sections/SharedFooter";

export default function ContactsPage() {
  return (
    <main className="bg-white">
      <SharedNavbar />
      <ContactForm />
      <StickyContactWidget />
      <SharedFooter />
    </main>
  );
}
