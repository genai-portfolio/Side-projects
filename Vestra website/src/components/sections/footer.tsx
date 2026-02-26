"use client";

import React from 'react';
import { Instagram, Youtube, Github, Facebook, Dribbble } from 'lucide-react';

/**
 * Footer component cloned from Vestra's design.
 * Features:
 * - Dark theme with white/gray text.
 * - Office addresses with pill-style CTA links.
 * - Site navigation grid.
 * - Social media round buttons with hover effects.
 * - Rotating contact-text badge in the bottom right.
 */
const Footer = () => {
  const socialIcons = [
    { Icon: Instagram, href: "https://www.instagram.com/vestralogics/" },
    { Icon: Youtube, href: "https://www.youtube.com/vestra" },
    { Icon: Github, href: "https://github.com/vestra" },
    { Icon: Facebook, href: "https://www.facebook.com/vestra" },
    { Icon: Dribbble, href: "https://dribbble.com/vestra" },
  ];

  return (
    <footer className="bg-black text-white py-20 px-5 md:px-20 relative overflow-hidden">
      <div className="max-w-[1440px] mx-auto">
        {/* Top Section: Addresses and Links */}
        <div className="flex flex-col lg:flex-row justify-between items-start gap-12 lg:gap-0 mb-32">

          {/* Left Column: Office Addresses */}
          <div className="flex flex-col md:flex-row gap-16 lg:gap-24">
            {/* Main Office */}
            <address className="not-italic">
              <div className="mb-6">
                <a
                  href="mailto:info@vestra.com"
                  className="inline-flex items-center justify-center px-8 py-3 rounded-full border border-white/20 text-lg font-medium transition-all duration-300 hover:bg-white hover:text-black"
                >
                  info@vestra.com
                </a>
              </div>
              <div className="text-[14px] uppercase tracking-wider text-[#9B9B9B] mb-2">Main office</div>
              <div className="text-[18px] leading-relaxed text-[#FFFFFF]">
                Faisalabad,<br />
                Pakistan
              </div>
            </address>

            {/* Second Office */}
            {/* Second Office Placeholder or Hidden */}
          </div>

          {/* Right Column: Navigation Links */}
          <div className="grid grid-cols-2 gap-x-12 gap-y-4 md:gap-x-20">
            <a href="/services/" className="text-[28px] font-medium hover:opacity-70 transition-opacity">Services</a>
            <a href="/projects/" className="text-[28px] font-medium hover:opacity-70 transition-opacity">Projects</a>
            <a href="https://hello.vestra.com/" className="text-[28px] font-medium hover:opacity-70 transition-opacity">Workflow</a>
            <a href="/about/" className="text-[28px] font-medium hover:opacity-70 transition-opacity">Company</a>
            <a href="/contacts/" className="text-[28px] font-medium hover:opacity-70 transition-opacity">Contacts</a>
          </div>
        </div>

        {/* Bottom Section: Legal and Socials */}
        <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-8 md:gap-0">

          {/* Privacy and Copyright */}
          <div className="flex flex-col gap-2">
            <a href="/privacy/" className="text-[14px] font-medium hover:underline underline-offset-4">Privacy Policy</a>
            <div className="text-[14px] text-[#9B9B9B]">2025, Vestra Logics</div>
          </div>

          {/* Social Icons */}
          <div className="flex flex-wrap gap-4">
            {socialIcons.map((social, index) => (
              <a
                key={index}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="w-12 h-12 flex items-center justify-center rounded-full bg-[#1A1A1A] border border-transparent transition-all duration-300 hover:bg-white group"
              >
                <social.Icon className="w-5 h-5 text-white group-hover:text-black transition-colors" />
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Rotating Badge - Bottom Right */}
      <div className="absolute bottom-10 right-10 hidden xl:block pointer-events-none">
        <div className="relative w-28 h-28 flex items-center justify-center animate-[spin_10s_linear_infinite]">
          <svg viewBox="0 0 100 100" className="w-full h-full fill-white/40">
            <path id="circlePath" d="M 50, 50 m -37, 0 a 37,37 0 1,1 74,0 a 37,37 0 1,1 -74,0" fill="none" />
            <text className="text-[10px] uppercase tracking-[0.2em] font-medium">
              <textPath xlinkHref="#circlePath">
                contact - contact - contact - contact -
              </textPath>
            </text>
          </svg>
        </div>
      </div>
    </footer>
  );
};

export default Footer;