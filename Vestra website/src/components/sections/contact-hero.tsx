"use client";

import React, { useEffect, useRef } from "react";
import { useInView } from "framer-motion";

/**
 * ContactHero component based on Cuberto's design.
 * Features a large, bold heading with split-text entrance animation.
 */
export default function ContactHero() {
  const containerRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(containerRef, { once: true, amount: 0.1 });

  const headingText = "Hey! Tell us all the things";
  const lines = [
    ["Hey!", "Tell", "us", "all"],
    ["the", "things"]
  ];

  return (
    <section 
      ref={containerRef}
      className="cb-contact bg-white pt-[160px] pb-[80px] md:pt-[240px] md:pb-[100px]"
    >
      <div className="container mx-auto px-[clamp(1.25rem,5vw,5rem)] max-w-[1440px]">
        <div className="cb-contact-header flex flex-col items-center justify-center text-center">
          <h1 
            aria-label={headingText}
            className="flex flex-col items-center justify-center m-0 p-0 leading-[1.0] font-semibold tracking-[-0.02em] text-black"
            style={{ fontSize: "clamp(3.5rem, 8vw, 7.5rem)" }}
          >
            {lines.map((line, lineIndex) => (
              <div 
                key={lineIndex} 
                className="overflow-hidden flex flex-wrap justify-center mb-0 md:last:mb-0"
              >
                {line.map((word, wordIndex) => (
                  <span
                    key={`${lineIndex}-${wordIndex}`}
                    className="inline-block relative whitespace-pre bg-inherit mr-[0.25em] last:mr-0"
                  >
                    <span
                      className="inline-block transition-transform duration-[1.2s] ease-[cubic-bezier(0.19,1,0.22,1)] will-change-transform"
                      style={{
                        transform: isInView ? "translateY(0)" : "translateY(110%)",
                        transitionDelay: `${(lineIndex * 4 + wordIndex) * 0.08}s`
                      }}
                    >
                      {word}
                    </span>
                  </span>
                ))}
                {lineIndex === 0 && <br className="hidden md:block" />}
              </div>
            ))}
          </h1>
        </div>
      </div>

      <style jsx global>{`
        /* Minimalist text reveal helpers */
        .cb-contact-header h1 {
          font-family: var(--font-display, "Inter", sans-serif);
        }
        
        @media (max-width: 768px) {
          .cb-contact {
            padding-top: 120px;
            padding-bottom: 60px;
          }
        }
      `}</style>
    </section>
  );
}