"use client";

import React, { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

/**
 * ProjectsHero component for the Projects page.
 * Features a large "Our projects" headline and a description with reveal animations.
 * 
 * Performance Note: Uses standard CSS transitions/animations as requested, 
 * but structured to allow for advanced GSAP animations if needed later.
 */
export default function ProjectsHero() {
  const sectionRef = useRef<HTMLElement>(null);

  // Define the text content as per the scraped data
  const mainTitle = "Our projects";
  const subText = "We help bring ideas to life and create digital products that work.";

  // Define categories for the filters
  const filters = [
    { id: "all", label: "All Projects", active: true },
    { id: "web", label: "Websites", active: false },
    { id: "app", label: "Applications", active: false },
    { id: "branding", label: "Branding", active: false },
  ];

  return (
    <section 
      ref={sectionRef}
      className="cb-entrylist relative bg-white pt-[clamp(120px,15vw,200px)] pb-20 overflow-hidden"
    >
      <div className="cb-entrylist-container -lg max-w-[90vw] mx-auto px-4 md:px-0 text-center">
        
        {/* Main Headline Section */}
        <div className="cb-entrylist-header mb-8 md:mb-12">
          <h1 
            className="text-[8.5vw] font-medium leading-[0.9] tracking-[-0.05em] text-black flex flex-wrap justify-center gap-x-[0.2em] overflow-hidden"
            aria-label={mainTitle}
          >
            {mainTitle.split(" ").map((word, idx) => (
              <span key={idx} className="relative inline-block overflow-hidden">
                <span className="inline-block animate-in slide-in-from-bottom duration-1000 ease-[cubic-bezier(0.7,0,0.3,1)]">
                  {word}
                </span>
              </span>
            ))}
          </h1>
        </div>

        {/* Description Text with word reveal effect */}
        <div className="cb-entrylist-text mb-12 md:mb-20 max-w-4xl mx-auto">
          <p className="cb-body-p text-[1.5rem] md:text-[2.2rem] font-normal leading-[1.3] tracking-[-0.02em] text-[#212121] flex flex-wrap justify-center gap-x-[0.3em]">
            {subText.split(" ").map((word, idx) => (
              <span key={idx} className="relative inline-block overflow-hidden py-[0.1em]">
                <span 
                  className="inline-block animate-in fade-in fill-mode-both"
                  style={{ 
                    animationDuration: '0.8s',
                    animationDelay: `${idx * 0.05 + 0.4}s`,
                    animationTimingFunction: 'cubic-bezier(0.7,0,0.3,1)'
                  }}
                >
                  {word}
                </span>
              </span>
            ))}
          </p>
        </div>

        {/* Project Filters */}
        <div className="cb-entrylist-filters flex flex-wrap justify-center items-center gap-6 md:gap-10 mt-10 md:mt-16">
          {filters.map((filter) => (
            <a
              key={filter.id}
              href={`#${filter.id}`}
              className={cn(
                "cb-filter-item group relative pb-1 cursor-pointer transition-opacity duration-300",
                filter.active ? "opacity-100" : "opacity-40 hover:opacity-100"
              )}
              data-filter-id={filter.id}
            >
              <span className="cb-entrylist-filter-title text-[1rem] md:text-[1rem] font-normal text-black block overflow-hidden">
                <span 
                  className="block transition-transform duration-500 group-hover:-translate-y-full"
                  data-text={filter.label}
                >
                  {filter.label}
                </span>
                <span 
                  className="absolute top-0 left-0 transition-transform duration-500 translate-y-full group-hover:translate-y-0 text-black font-medium"
                >
                  {filter.label}
                </span>
              </span>
              {/* Active Indicator Underline */}
              {filter.active && (
                <div className="absolute bottom-0 left-0 w-full h-[1px] bg-black origin-left scale-x-100 transition-transform duration-500" />
              )}
              {/* Hover Underline */}
              {!filter.active && (
                <div className="absolute bottom-0 left-0 w-full h-[1px] bg-black origin-right scale-x-0 group-hover:origin-left group-hover:scale-x-100 transition-transform duration-500" />
              )}
            </a>
          ))}
        </div>
      </div>

      {/* Structured Styles to match globals.css and specific requirements */}
      <style jsx>{`
        .cb-entrylist-header h1 span span {
          display: inline-block;
        }
        
        .cb-entrylist-filters {
          border-top: 0px solid rgba(0, 0, 0, 0.1);
        }

        @media (max-width: 768px) {
          .cb-entrylist-header h1 {
            font-size: 14vw;
            line-height: 1;
          }
          .cb-body-p {
            font-size: 1.25rem;
            line-height: 1.4;
          }
        }
      `}</style>
    </section>
  );
}