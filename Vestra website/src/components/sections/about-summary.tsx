"use client";

import React, { useState, useEffect, useRef } from 'react';

/**
 * AboutSummary Component
 * 
 * Clones the brief summary section of Cuberto's website.
 * Features:
 * - Side video loop with large border radius.
 * - Text about Vestra Logics's history since 2025.
 * - Magnetic "What we do" CTA button with ripple effect.
 */

export default function AboutSummary() {
  const [isHovered, setIsHovered] = useState(false);
  const [magneticPos, setMagneticPos] = useState({ x: 0, y: 0 });
  const [ripplePos, setRipplePos] = useState({ x: 0, y: 0, active: false });
  const buttonRef = useRef<HTMLAnchorElement>(null);

  // Magnetic effect logic
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!buttonRef.current) return;
    const rect = buttonRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const x = (e.clientX - centerX) * 0.35;
    const y = (e.clientY - centerY) * 0.35;

    setMagneticPos({ x, y });
  };

  const handleMouseEnter = (e: React.MouseEvent) => {
    setIsHovered(true);
    if (!buttonRef.current) return;
    const rect = buttonRef.current.getBoundingClientRect();
    setRipplePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      active: true
    });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setMagneticPos({ x: 0, y: 0 });
    setRipplePos(prev => ({ ...prev, active: false }));
  };

  return (
    <section className="bg-white py-[80px] md:py-[160px] overflow-hidden">
      <div className="container mx-auto px-[5%] lg:px-[160px]">
        <div className="flex flex-col lg:flex-row items-center gap-[60px] lg:gap-[120px]">

          {/* Left Column: Video Figure */}
          <div className="w-full lg:w-1/2 flex justify-center lg:justify-start">
            <div className="relative w-full aspect-square max-w-[500px] overflow-hidden rounded-[40px] md:rounded-[80px] lg:rounded-[120px]">
              <video
                autoPlay
                loop
                muted
                playsInline
                className="w-full h-full object-cover"
                poster="https://cuberto.com/assets/home/summary/2.mp4"
              >
                <source src="https://cuberto.com/assets/home/summary/2.mp4" type="video/mp4" />
              </video>
            </div>
          </div>

          {/* Right Column: Brief Content */}
          <div className="w-full lg:w-1/2 flex flex-col items-start">
            <div className="text-[24px] md:text-[32px] font-normal leading-[1.3] tracking-tight space-y-6 text-black opacity-90 max-w-[540px]">
              <p>
                Since 2025, we have been helping our clients find exceptional solutions for their businesses, creating memorable websites and digital products.
              </p>
              <p>
                Vestra Logics doesn't do cookie-cutter solutions and we build products exactly as they were during the design phase, no short cuts or simplifications.
              </p>
            </div>

            {/* Magnetic CTA Button */}
            <div className="mt-12 md:mt-16">
              <a
                ref={buttonRef}
                href="/services"
                onMouseMove={handleMouseMove}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                style={{
                  transform: `translate(${magneticPos.x}px, ${magneticPos.y}px)`,
                }}
                className="group relative inline-flex items-center justify-center h-[160px] w-[160px] md:h-[200px] md:w-[200px] rounded-full border border-black/10 overflow-hidden transition-transform duration-300 ease-out cursor-none"
              >
                {/* Ripple Effect Background */}
                <span
                  className={`absolute rounded-full bg-black transition-all duration-700 ease-out pointer-events-none transform -translate-x-1/2 -translate-y-1/2 ${ripplePos.active ? 'scale-[2.5] opacity-100' : 'scale-0 opacity-0'
                    }`}
                  style={{
                    left: ripplePos.x,
                    top: ripplePos.y,
                    width: '100%',
                    height: '100%',
                  }}
                />

                {/* Button Text */}
                <span
                  className={`relative z-10 text-[18px] font-medium transition-colors duration-300 pointer-events-none ${isHovered ? 'text-white' : 'text-black'
                    }`}
                >
                  <span className="block overflow-hidden h-[1.2em]">
                    <span
                      className={`block transition-transform duration-500 ease-in-out ${isHovered ? '-translate-y-full' : 'translate-y-0'
                        }`}
                      data-text="What we do"
                    >
                      What we do
                    </span>
                    <span
                      className={`block transition-transform duration-500 ease-in-out ${isHovered ? '-translate-y-full' : 'translate-y-0'
                        }`}
                    >
                      What we do
                    </span>
                  </span>
                </span>

                {/* Visual Border Shadow */}
                <span className="absolute inset-0 rounded-full border border-transparent group-hover:border-black/5 pointer-events-none transition-colors duration-300" />
              </a>
            </div>
          </div>

        </div>
      </div>

      <style jsx>{`
        @keyframes ripple {
          from {
            transform: scale(0);
            opacity: 1;
          }
          to {
            transform: scale(4);
            opacity: 1;
          }
        }
      `}</style>
    </section>
  );
}