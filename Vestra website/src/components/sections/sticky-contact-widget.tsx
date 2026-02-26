"use client";

import React, { useEffect, useRef, useState } from "react";

/**
 * StickyContactWidget - A pixel-perfect clone of Cuberto's floating "Get in touch" widget.
 * 
 * Features:
 * - Floating circular design with magnetic follow interaction.
 * - Rotating SVG text "contact-" around the perimeter.
 * - Video preview that plays on hover.
 * - Light theme compliant.
 */
export default function StickyContactWidget() {
  const containerRef = useRef<HTMLAnchorElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  // Magnetic interaction logic
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;

      const rect = containerRef.current.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      // Distance from cursor to center of widget
      const distX = e.clientX - centerX;
      const distY = e.clientY - centerY;
      
      // Threshold for magnetic effect
      const threshold = 100;
      const distance = Math.sqrt(distX * distX + distY * distY);

      if (distance < threshold) {
        // Apply magnetic pull (0.3 factor for subtle movement)
        const moveX = distX * 0.35;
        const moveY = distY * 0.35;
        setPosition({ x: moveX, y: moveY });
        if (!isHovered) setIsHovered(true);
      } else {
        setPosition({ x: 0, y: 0 });
        if (isHovered) setIsHovered(false);
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [isHovered]);

  // Video playback handle
  const handleMouseEnter = () => {
    setIsHovered(true);
    if (videoRef.current) {
      videoRef.current.play().catch(() => {
        /* Playback may be interrupted */
      });
    }
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    setPosition({ x: 0, y: 0 });
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
  };

  // Rotating text string construction
  const rotatingText = "contact - contact - contact - contact - ";

  return (
    <a
      ref={containerRef}
      href="/contacts/"
      className="fixed bottom-10 right-10 z-[100] flex items-center justify-center cursor-none pointer-events-auto"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        transform: `translate3d(${position.x}px, ${position.y}px, 0)`,
        transition: isHovered ? "transform 0.1s cubic-bezier(0.23, 1, 0.32, 1)" : "transform 0.6s cubic-bezier(0.19, 1, 0.22, 1)",
      }}
      aria-label="Get in touch"
    >
      <div className="relative w-[130px] h-[130px] lg:w-[150px] lg:h-[150px] flex items-center justify-center">
        {/* Rotating Circular Text */}
        <div className="absolute inset-0 animate-[spin_10s_linear_infinite]">
          <svg
            viewBox="0 0 200 200"
            className="w-full h-full overflow-visible"
          >
            <defs>
              <path
                id="circlePath"
                d="M 100, 100 m -80, 0 a 80,80 0 1,1 160,0 a 80,80 0 1,1 -160,0"
              />
            </defs>
            <text className="fill-current text-primary font-medium uppercase tracking-[0.1em]" style={{ fontSize: '14.5px' }}>
              <textPath xlinkHref="#circlePath">
                {rotatingText}
              </textPath>
            </text>
          </svg>
        </div>

        {/* Inner Video / Thumbnail Circle */}
        <div 
          className="relative w-[65%] h-[65%] rounded-full overflow-hidden bg-secondary border border-border transition-transform duration-500 ease-out"
          style={{ transform: isHovered ? 'scale(1.1)' : 'scale(1)' }}
        >
          <video
            ref={videoRef}
            src="https://cuberto.com/assets/intouch/2.mp4"
            loop
            muted
            playsInline
            className="w-full h-full object-cover"
          />
          {/* Static state overlay if needed, here we just show the first frame/muted video */}
          {!isHovered && (
            <div className="absolute inset-0 bg-transparent" />
          )}
        </div>
      </div>

      <style jsx global>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </a>
  );
}