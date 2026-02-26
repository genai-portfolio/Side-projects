"use client";

import React, { useRef, useState, useEffect } from "react";

const OutroCTA: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const rippleRef = useRef<HTMLSpanElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  // Ripple effect logic for the button
  const handleMouseMove = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (!rippleRef.current) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    rippleRef.current.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%) scale(${isHovered ? 1 : 0})`;
  };

  return (
    <section className="cb-outro relative overflow-hidden bg-black text-white" data-cursor="-inverse">
      {/* Background Video Layer */}
      <div className="cb-outro-bg absolute inset-0 z-0 opacity-60">
        <div className="cb-outro-bg-media w-full h-full">
          <video
            autoPlay
            muted
            loop
            playsInline
            className="w-full h-full object-cover"
          >
            <source src="https://cuberto.com/assets/footer/ropes.mp4" type="video/mp4" />
            <source src="https://cuberto.com/assets/footer/ropes-sm.mp4?2" type="video/mp4" />
          </video>
        </div>
      </div>

      {/* Content Container */}
      <div className="cb-outro-content relative z-10 flex flex-col items-center justify-center min-h-screen text-center px-[5vw] py-[120px] md:py-[200px]">
        <div className="cb-outro-container max-w-[90vw] w-full flex flex-col items-center">
          
          {/* Header Typography */}
          <div className="cb-outro-header mb-12 sm:mb-20">
            <h2 
              className="text-[20vw] sm:text-[12vw] font-medium leading-[0.9] tracking-[-0.05em] uppercase sm:normal-case pointer-events-none"
              aria-label="Have an idea?"
            >
              <div className="overflow-hidden">
                <span className="block translate-y-0">Have</span>
              </div>
              <div className="overflow-hidden">
                <span className="block translate-y-0">an idea?</span>
              </div>
            </h2>
          </div>

          {/* Large CTA Button */}
          <div className="cb-outro-action">
            <a
              href="/contacts/"
              className="cb-btn cb-btn_cta group relative inline-flex items-center justify-center px-16 py-8 sm:px-32 sm:py-16 rounded-full border border-white/20 transition-all duration-700 ease-[cubic-bezier(0.7,0,0.3,1)] hover:border-transparent overflow-hidden"
              onMouseMove={handleMouseMove}
              onMouseEnter={() => setIsHovered(true)}
              onMouseLeave={() => setIsHovered(false)}
            >
              {/* Ripple Circle */}
              <span 
                ref={rippleRef}
                className="cb-btn_cta-ripple absolute top-0 left-0 w-[200%] aspect-square rounded-full bg-white transition-transform duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] pointer-events-none -z-10 scale-0"
              />
              
              {/* Button Text */}
              <span className="cb-btn_cta-title relative z-10">
                <span 
                  className="text-[1.5rem] sm:text-[3.5rem] font-normal leading-none tracking-tight transition-colors duration-500 group-hover:text-black uppercase"
                  data-text="Tell us"
                >
                  Tell us
                </span>
              </span>
            </a>
          </div>

        </div>
      </div>

      <style jsx global>{`
        .cb-outro {
          border-top-left-radius: 60px;
          border-top-right-radius: 60px;
        }

        @media (max-width: 768px) {
          .cb-outro {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
          }
        }
        
        .cb-btn_cta-title span {
          display: block;
          position: relative;
        }

        /* Subtle magnetic hover logic can be added here or via external script as per Cuberto style */
      `}</style>
    </section>
  );
};

export default OutroCTA;