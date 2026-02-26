import React from "react";
import { Instagram, Mail } from "lucide-react";

const SharedFooter = () => {
  return (
    <footer className="bg-black text-white pt-24 pb-12 overflow-hidden">
      <div className="max-w-[1440px] mx-auto px-6 md:px-10 lg:px-20">
        {/* Top Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 mb-20">
          {/* Left: Office Info */}
          <div className="flex flex-col md:flex-row gap-14">
            <address className="not-italic">
              <a
                href="mailto:info@vestra.com"
                className="inline-flex items-center justify-center px-7 py-3 rounded-full border border-white/20 text-[15px] font-medium hover:bg-white hover:text-black transition-all duration-300 mb-6 block w-fit"
              >
                info@vestra.com
              </a>
              <p className="text-[12px] uppercase tracking-[0.15em] text-white/40 font-bold mb-2">
                Main office
              </p>
              <p className="text-[17px] leading-relaxed">
                Faisalabad, City Housing,
                <br />
                Block C, 21st Avenue
              </p>
            </address>

            <address className="not-italic">
              <a
                href="tel:+923015499309"
                className="inline-flex items-center justify-center px-7 py-3 rounded-full border border-white/20 text-[15px] font-medium hover:bg-white hover:text-black transition-all duration-300 mb-6 block w-fit"
              >
                +92 301 549 9309
              </a>
              <p className="text-[12px] uppercase tracking-[0.15em] text-white/40 font-bold mb-2">
                Second office
              </p>
              <p className="text-[17px] leading-relaxed">
                Na Perstyne
                <br />
                342/1, 11000 Prague
              </p>
            </address>
          </div>

          {/* Right: Navigation */}
          <div className="grid grid-cols-2 gap-x-10 gap-y-5 lg:pl-10">
            {[
              { label: "Services", href: "/services" },
              { label: "Projects", href: "/projects" },
              { label: "Workflow", href: "https://hello.cuberto.com/" },
              { label: "Company", href: "/about" },
              { label: "Contacts", href: "/contacts" },
            ].map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-[22px] font-medium hover:opacity-60 transition-opacity"
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col md:flex-row justify-between items-center border-t border-white/10 pt-10 gap-6">
          <div className="flex items-center gap-8 text-[14px] text-white/50">
            <a href="/privacy" className="hover:text-white transition-colors">
              Privacy Policy
            </a>
            <span>2025, Vestra Logics</span>
          </div>

          <div className="flex items-center gap-3">
            {[
              { Icon: Instagram, href: "https://www.instagram.com/cubertodesign/", label: "Instagram" },
              { Icon: Mail, href: "mailto:info@vestra.com", label: "Email" },
            ].map(({ Icon, href }, idx) => (
              <a
                key={idx}
                href={href}
                className="w-11 h-11 flex items-center justify-center rounded-full border border-white/10 hover:bg-white hover:text-black transition-all duration-300 group"
                suppressHydrationWarning
              >
                <Icon size={17} />
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default SharedFooter;
