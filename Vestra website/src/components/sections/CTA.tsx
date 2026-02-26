"use client";

import React from 'react';

/**
 * CTA component cloning the "Have an idea? TELL US" section.
 * Features large typography, interactive pill-shaped link, and black background
 * that transitions seamlessly into the footer as per the design instructions.
 */
const CTA: React.FC = () => {
  return (
    <section 
      className="cb-cta bg-[#111111] text-[#ffffff] pt-[150px] pb-[100px] md:pt-[200px] md:pb-[150px] overflow-hidden"
      style={{
        borderTopLeftRadius: '40px',
        borderTopRightRadius: '40px',
        marginTop: '-40px', // Creates the overlapping rounded transition effect
        position: 'relative',
        zIndex: 10
      }}
    >
      <div className="container mx-auto px-10 flex flex-col items-center text-center">
        <div className="cb-cta-content max-w-[1000px] w-full">
          {/* Main Headline */}
          <h2 
            className="mb-8 md:mb-12 font-medium tracking-tighter"
            style={{
              fontSize: 'clamp(64px, 12vw, 120px)',
              lineHeight: '0.9',
              color: '#ffffff'
            }}
          >
            Have <br className="hidden md:block" />
            an idea?
          </h2>

          {/* Large Interactive Pill Button */}
          <div className="cb-cta-action flex justify-center mt-4">
            <a 
              href="/contacts/"
              className="cb-cta-link group relative inline-flex items-center justify-center px-12 py-5 md:px-20 md:py-8 border border-white rounded-full transition-all duration-500 ease-in-out hover:bg-white hover:text-black overflow-hidden"
              style={{
                fontSize: 'clamp(40px, 8vw, 80px)',
                fontWeight: 500,
                letterSpacing: '-0.02em'
              }}
            >
              <span className="relative z-10 transition-transform duration-500 transform group-hover:scale-110">
                TELL US
              </span>
              
              {/* Circular hover effect background (optional, but follows Cuberto's liquid feel) */}
              <div className="absolute inset-0 bg-white scale-0 group-hover:scale-100 transition-transform duration-500 ease-in-out origin-center rounded-full -z-0"></div>
            </a>
          </div>
        </div>
      </div>

      {/* Subtle Divider (Optional, mimics footer separation if needed) */}
      <div className="container mx-auto px-10 mt-[150px] opacity-20">
        <div className="w-full h-px bg-white"></div>
      </div>
    </section>
  );
};

export default CTA;