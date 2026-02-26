"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Services", href: "/services/" },
    { name: "Projects", href: "/projects/" },
    { name: "Company", href: "/about/" },
    { name: "Blog", href: "/blog/" },
    { name: "Contacts", href: "/contacts/", active: true },
  ];

  return (
    <header className="cb-navbar fixed top-0 left-0 w-full z-[100]">
      {/* Background Fill on Scroll */}
      <div 
        className={cn(
          "cb-navbar-fill fixed top-0 left-0 w-full h-[80px] bg-white/95 transition-transform duration-500 ease-in-out z-[-1]",
          isScrolled ? "translate-y-0" : "-translate-y-full"
        )}
      />

      <div className="cb-navbar-strip relative w-full h-[80px] flex items-center">
        <div className="container px-5 md:px-[80px] lg:px-[120px] max-w-[1440px] mx-auto w-full">
          <div className="cb-navbar-grid flex items-center justify-between">
            {/* Logo Section */}
            <div className="cb-navbar-grid-col -left flex-shrink-0">
              <Link href="/" className="cb-navbar-logo block" aria-label="Home">
                <svg
                  width="116"
                  height="24"
                  viewBox="0 0 116 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-[116px] h-[24px]"
                >
                  <path
                    d="M12.64 12c0 4.14-3.36 7.5-7.5 7.5S-2.36 16.14-2.36 12s3.36-7.5 7.5-7.5 7.5 3.36 7.5 7.5zM7.5 7.5c-2.48 0-4.5 2.02-4.5 4.5s2.02 4.5 4.5 4.5 4.5-2.02 4.5-4.5-2.02-4.5-4.5-4.5z"
                    fill="currentColor"
                  />
                  <path
                    d="M20.63 4.5h3v7.5c0 2.48 2.02 4.5 4.5 4.5s4.5-2.02 4.5-4.5v-7.5h3v7.5c0 4.14-3.36 7.5-7.5 7.5s-7.5-3.36-7.5-7.5V4.5z"
                    fill="currentColor"
                  />
                  <path
                    d="M48 4.5h3v15H48V4.5zM36 4.5h3v15h-3V4.5z"
                    fill="currentColor"
                  />
                  <path
                    d="M60 4.5h3v6c1.1-1.1 2.5-1.5 4-1.5 2.5 0 4.5 2 4.5 4.5v6h-3v-6c0-0.8-0.7-1.5-1.5-1.5s-1.5 0.7-1.5 1.5v6H60V4.5z"
                    fill="currentColor"
                  />
                  <path
                    d="M84 4.5h3v15h-3V4.5z"
                    fill="currentColor"
                  />
                  <path
                    d="M96 12c0 4.14-3.36 7.5-7.5 7.5S81 16.14 81 12s3.36-7.5 7.5-7.5 7.5 3.36 7.5 7.5zm-7.5 4.5c2.48 0 4.5-2.02 4.5-4.5s-2.02-4.5-4.5-4.5-4.5 2.02-4.5 4.5 2.02 4.5 4.5 4.5z"
                    fill="currentColor"
                  />
                </svg>
              </Link>
            </div>

            {/* Navigation Desktop Section */}
            <div className="cb-navbar-grid-col -right flex items-center space-x-12">
              <nav className="cb-navbar-navs hidden xl:flex items-center space-x-10">
                {navLinks.map((link) => (
                  <div 
                    key={link.name} 
                    className={cn(
                      "cb-navbar-nav group relative",
                      link.active && "after:content-[''] after:absolute after:bottom-[-4px] after:left-0 after:w-full after:h-[1px] after:bg-black"
                    )}
                  >
                    <Link
                      href={link.href}
                      className="cb-navbar-nav-toggle text-[14px] font-medium uppercase tracking-wider block overflow-hidden h-[18px]"
                    >
                      <span className="cb-navbar-nav-title relative block transition-transform duration-500 ease-out group-hover:-translate-y-full">
                        <span className="block" data-text={link.name}>{link.name}</span>
                        <span className="absolute top-full left-0 block italic" data-text={link.name}>{link.name}</span>
                      </span>
                    </Link>
                  </div>
                ))}
              </nav>

              {/* Hamburger Button */}
              <div className="cb-navbar-toggle ml-8">
                <button
                  onClick={() => setIsOpen(!isOpen)}
                  className="cb-btn cb-btn_menu group flex flex-col items-end justify-center w-[40px] h-[40px] cursor-pointer focus:outline-none"
                  aria-label="Toggle menu"
                >
                  <span className={cn(
                    "block w-[24px] h-[2px] bg-black mb-1.5 transition-all duration-300 origin-right",
                    isOpen && "-rotate-45 translate-x-[-2px] translate-y-[1px]"
                  )}></span>
                  <span className={cn(
                    "block w-[18px] h-[2px] bg-black transition-all duration-300 origin-right",
                    isOpen && "rotate-45 translate-x-[-2px] translate-y-[-1px] w-[24px]"
                  )}></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Fullscreen Overlay Menu */}
      <div 
        className={cn(
          "cb-navbar-menu fixed inset-0 bg-white z-[99] transition-transform duration-700 ease-[cubic-bezier(0.19,1,0.22,1)] will-change-transform",
          isOpen ? "translate-y-0" : "-translate-y-full"
        )}
        id="navbar-menu"
      >
        <div className="container h-full flex flex-col justify-between py-[120px] px-5 md:px-[80px] lg:px-[120px]">
          <div className="cb-navbar-menu-top flex flex-col">
            <div className="cb-navbar-menu-caption mb-12">
              <h3 className="text-[14px] uppercase tracking-widest text-[#9b9b9b]">Menu</h3>
            </div>
            <div className="cb-navbar-menu-navs flex flex-col space-y-6">
              {navLinks.map((link, i) => (
                <div 
                  key={link.name} 
                  className="cb-navbar-menu-nav overflow-hidden"
                  style={{ transitionDelay: `${i * 0.1}s` }}
                >
                  <Link
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className={cn(
                      "cb-btn cb-btn_nav text-[clamp(2.5rem,8vw,5rem)] font-semibold leading-tight flex items-baseline hover:italic transition-all duration-300",
                      link.active && "underline decoration-1 underline-offset-8"
                    )}
                  >
                    <span className="cb-btn_nav-title">
                      <span data-text={link.name}>{link.name}</span>
                    </span>
                  </Link>
                </div>
              ))}
            </div>
          </div>

          <div className="cb-navbar-menu-bottom grid grid-cols-1 md:grid-cols-2 gap-8 items-end">
            <div className="cb-navbar-menu-caption -rb">
              <h3 className="text-[14px] uppercase tracking-widest text-[#9b9b9b]">Get in touch</h3>
            </div>
            <div className="cb-navbar-menu-links flex flex-col space-y-4">
              <div className="cb-navbar-menu-link">
                <a 
                  href="mailto:info@cuberto.com" 
                  className="text-[clamp(1.25rem,3vw,2.5rem)] font-medium hover:opacity-70 transition-opacity underline decoration-1 underline-offset-4"
                >
                  info@cuberto.com
                </a>
              </div>
              <div className="cb-navbar-menu-link">
                <Link 
                  href="https://hello.cuberto.com/" 
                  className="text-[clamp(1.25rem,3vw,1.5rem)] font-normal hover:opacity-70 transition-opacity"
                >
                  Our workflow
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;