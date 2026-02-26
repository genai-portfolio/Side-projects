"use client";

import React, { useRef, useState, useEffect } from "react";

const Outro = () => {
  const [magneticPos, setMagneticPos] = useState({ x: 0, y: 0 });
  const buttonRef = useRef<HTMLAnchorElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!buttonRef.current) return;

    const rect = buttonRef.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const distanceX = e.clientX - centerX;
    const distanceY = e.clientY - centerY;

    // Only apply magnetic effect if mouse is relatively close
    const threshold = 300;
    if (Math.abs(distanceX) < threshold && Math.abs(distanceY) < threshold) {
      setMagneticPos({
        x: distanceX * 0.35,
        y: distanceY * 0.35,
      });
    } else {
      setMagneticPos({ x: 0, y: 0 });
    }
  };

  const handleMouseLeave = () => {
    setMagneticPos({ x: 0, y: 0 });
  };

  return (
    <section
      className="cb-outro relative min-h-screen bg-black flex flex-col justify-center overflow-hidden"
      data-cursor="-inverse"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {/* Background Video Layer */}
      <div className="cb-outro-bg absolute inset-0 z-0 opacity-60">
        <div className="cb-outro-bg-media w-full h-full">
          <video
            autoPlay
            loop
            muted
            playsInline
            className="w-full h-full object-cover"
          >
            <source src="https://cuberto.com/assets/footer/ropes.mp4" type="video/mp4" />
            <source src="https://cuberto.com/assets/footer/ropes-sm.mp4?2" type="video/mp4" />
          </video>
        </div>
      </div>

      {/* Content Layer */}
      <div className="cb-outro-content relative z-10 w-full">
        <div className="cb-outro-container container mx-auto px-4 md:px-10 flex flex-col items-center text-center">

          <div className="cb-outro-header mb-12 md:mb-20">
            <h2
              className="text-white font-medium leading-[0.9] tracking-[-0.03em]"
              style={{ fontSize: "clamp(5rem, 15vw, 12rem)" }}
              aria-label="Have an idea?"
            >
              <span className="block italic font-light">Have</span>
              <span className="block">an idea?</span>
            </h2>
          </div>

          <div className="cb-outro-action relative">
            <a
              ref={buttonRef}
              href="/contacts/"
              className="cb-btn cb-btn_cta -xl -inverse group relative inline-flex items-center justify-center rounded-full border border-white/30 text-white transition-all duration-300 ease-out hover:bg-white hover:text-black overflow-hidden"
              style={{
                width: "clamp(240px, 40vw, 480px)",
                height: "clamp(100px, 15vw, 180px)",
                transform: `translate3d(${magneticPos.x}px, ${magneticPos.y}px, 0)`,
                transition: magneticPos.x === 0 ? "transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)" : "none"
              }}
            >
              <span className="cb-btn_cta-ripple absolute inset-0 bg-white scale-y-0 origin-bottom transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] group-hover:scale-y-100"></span>

              <span className="cb-btn_cta-title relative z-10 font-medium uppercase tracking-widest text-[clamp(1.5rem,3vw,3.5rem)]">
                <span data-text="Tell us">Tell us</span>
              </span>
            </a>
          </div>

        </div>
      </div>

      {/* Styling for the section based on computed values */}
      <style jsx>{`
        .cb-outro {
          padding-top: 160px;
          padding-bottom: 160px;
        }
        
        @media (max-width: 768px) {
          .cb-outro {
            padding-top: 100px;
            padding-bottom: 100px;
          }
        }

        .cb-btn_cta-title span {
          display: block;
          position: relative;
          transition: transform 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        }

        .cb-btn_cta:hover .cb-btn_cta-title span {
          transform: translateY(0);
        }

        h2 span {
          display: block;
        }

        /* Magnetic smoothing */
        .cb-btn_cta {
          will-change: transform;
        }
      `}</style>
    </section>
  );
};

export default Outro;