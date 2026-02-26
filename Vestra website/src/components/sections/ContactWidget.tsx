"use client";

import React, { useRef, useState, useEffect } from "react";

const ContactWidget: React.FC = () => {
  const [isHovered, setIsHovered] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      if (isHovered) {
        videoRef.current.play().catch(() => {
          // Fallback if autoplay is blocked
        });
      } else {
        videoRef.current.pause();
        videoRef.current.currentTime = 0;
      }
    }
  }, [isHovered]);

  return (
    <a
      href="/contacts/"
      className="cb-intouch fixed right-[50px] bottom-[50px] z-[99] block h-[120px] w-[120px] select-none no-underline transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] hover:scale-110 active:scale-95 group"
      aria-label="Get in touch"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="cb-intouch-outline relative flex h-full w-full items-center justify-center">
        <svg
          viewBox="0 0 100 100"
          className="absolute inset-0 h-full w-full origin-center animate-[spin_10s_linear_infinite]"
        >
          <path
            id="circlePath"
            d="M 50, 50 m -37, 0 a 37,37 0 1,1 74,0 a 37,37 0 1,1 -74,0"
            fill="transparent"
          />
          <text className="fill-current text-foreground dark:text-white">
            <textPath
              href="#circlePath"
              startOffset="0%"
              className="text-[11px] font-medium uppercase tracking-[0.14em]"
              style={{ fontFamily: '"Suisse Intl", sans-serif' }}
            >
              contact-contact-contact-contact-contact-contact-contact-contact-
            </textPath>
          </text>
        </svg>
      </div>

      <div className="cb-intouch-video absolute inset-0 flex items-center justify-center overflow-hidden rounded-full p-[28%] pointer-events-none">
        <div className="relative h-full w-full overflow-hidden rounded-full bg-black">
          <video
            ref={videoRef}
            loop
            muted
            playsInline
            className="h-full w-full object-cover transition-opacity duration-300"
            poster="https://cuberto.com/assets/intouch/2.mp4"
          >
            <source src="https://cuberto.com/assets/intouch/2.mp4" type="video/mp4" />
          </video>
        </div>
      </div>

      {/* Tailwind specific animation for the rotation */}
      <style jsx global>{`
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </a>
  );
};

export default ContactWidget;