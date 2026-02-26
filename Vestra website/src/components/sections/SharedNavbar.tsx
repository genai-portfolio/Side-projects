"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const VestraLogo = () => (
  <svg
    width="116"
    height="24"
    viewBox="0 0 120 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className="h-[24px] w-auto"
  >
    <text
      x="0"
      y="19"
      fontFamily="Inter, sans-serif"
      fontSize="20"
      fontWeight="600"
      letterSpacing="-0.5"
      fill="currentColor"
    >
      vestra
    </text>
  </svg>
);

const SharedNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 50);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [isOpen]);

  const navLinks = [
    { name: "Services", href: "/services" },
    { name: "Projects", href: "/projects" },
    { name: "Company", href: "/about" },
    { name: "Contacts", href: "/contacts" },
  ];

  const isActive = (href: string) => {
    if (href === "/") return pathname === "/";
    return pathname.startsWith(href);
  };

  return (
    <header className="cb-navbar fixed top-0 left-0 w-full z-[100]">
      <div
        className={cn(
          "absolute inset-0 transition-all duration-500 ease-in-out pointer-events-none",
          isScrolled ? "bg-white/95 backdrop-blur-md" : "bg-transparent"
        )}
      />

      <div className="relative w-full h-[80px] flex items-center">
        <div className="w-full max-w-[1440px] mx-auto px-6 md:px-10 lg:px-20">
          <div className="flex items-center justify-between h-full">
            <Link href="/" className="relative z-10 flex items-center gap-3" aria-label="Home">
              <img src="/logo.jpg" alt="Vestra Logics Logo" className="h-8 w-8 rounded-full object-cover" />
              <span className="text-[22px] font-semibold tracking-tight">Vestra Logics</span>
            </Link>

            <div className="flex items-center gap-10">
              <nav className="hidden lg:flex items-center gap-8">
                {navLinks.map((link) => (
                  <Link
                    key={link.name}
                    href={link.href}
                    className={cn(
                      "relative h-[20px] overflow-hidden text-[15px] font-medium leading-none group",
                      isActive(link.href) ? "text-black" : "text-black/70 hover:text-black"
                    )}
                  >
                    <div className="flex flex-col transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] group-hover:-translate-y-1/2 will-change-transform">
                      <span className="h-[20px] flex items-center">
                        {link.name}
                      </span>
                      <span className="h-[20px] flex items-center">
                        {link.name}
                      </span>
                    </div>
                    {isActive(link.href) && (
                      <span className="absolute bottom-0 left-0 w-full h-[1px] bg-black" />
                    )}
                  </Link>
                ))}
              </nav>

              <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-3 group relative z-[101]"
                aria-label="Toggle menu"
              >
                <span className="text-[13px] font-medium uppercase tracking-widest hidden sm:block">
                  Menu
                </span>
                <div className="flex flex-col justify-center items-end w-8 h-8 gap-1.5">
                  <span
                    className={cn(
                      "block h-[2px] bg-black transition-all duration-300",
                      isOpen ? "w-8 rotate-45 translate-y-[5px]" : "w-8"
                    )}
                  />
                  <span
                    className={cn(
                      "block h-[2px] bg-black transition-all duration-300",
                      isOpen ? "w-8 -rotate-45 -translate-y-[3px]" : "w-5"
                    )}
                  />
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Fullscreen Overlay Menu */}
      <div
        className={cn(
          "fixed inset-0 bg-white z-[99] transition-transform duration-700 ease-[cubic-bezier(0.19,1,0.22,1)]",
          isOpen ? "translate-y-0" : "-translate-y-full invisible pointer-events-none"
        )}
      >
        <div className="h-full flex flex-col justify-between px-6 md:px-20 lg:px-40 pt-[140px] pb-16 max-w-[1440px] mx-auto">
          <div>
            <p className="text-[12px] uppercase tracking-[0.2em] text-black/40 font-bold mb-10">Menu</p>
            <nav className="flex flex-col gap-3">
              {[{ name: "Home", href: "/" }, ...navLinks].map((link, i) => (
                <div key={link.name} className="overflow-hidden">
                  <Link
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className={cn(
                      "block text-[clamp(3rem,8vw,6rem)] font-medium leading-[1.1] tracking-tight hover:pl-6 transition-all duration-500",
                      isActive(link.href) && "underline underline-offset-8 decoration-1"
                    )}
                    style={{ transitionDelay: `${i * 40}ms` }}
                  >
                    {link.name}
                  </Link>
                </div>
              ))}
            </nav>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 border-t border-black/10 pt-10">
            <div>
              <p className="text-[12px] uppercase tracking-[0.2em] text-black/40 font-bold mb-4">
                Get in touch
              </p>
              <a
                href="mailto:info@vestra.com"
                className="text-[20px] font-medium hover:underline underline-offset-8 decoration-1"
              >
                info@vestra.com
              </a>
            </div>
            <div className="flex items-end gap-6">
              {[
                { name: "Instagram", href: "https://www.instagram.com/vestralogics/" },
                { name: "Email", href: "mailto:info@vestra.com" },
              ].map((s) => (
                <a
                  key={s.name}
                  href={s.href}
                  className="text-[13px] font-medium uppercase tracking-widest hover:opacity-50 transition-opacity"
                >
                  {s.name}
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default SharedNavbar;
