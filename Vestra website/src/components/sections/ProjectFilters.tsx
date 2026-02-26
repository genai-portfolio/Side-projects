"use client";

import React, { useState, useRef, useEffect } from "react";
import { cn } from "@/lib/utils";

interface FilterItemProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const FilterItem = ({ label, isActive, onClick }: FilterItemProps) => {
  const itemRef = useRef<HTMLAnchorElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (!itemRef.current) return;
    const { clientX, clientY } = e;
    const { left, top, width, height } = itemRef.current.getBoundingClientRect();
    const x = (clientX - (left + width / 2)) * 0.35;
    const y = (clientY - (top + height / 2)) * 0.35;
    setPosition({ x, y });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  return (
    <a
      ref={itemRef}
      onClick={(e) => {
        e.preventDefault();
        onClick();
      }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      href="#"
      className={cn(
        "relative block py-1 px-4 cursor-pointer transition-opacity duration-300",
        isActive ? "opacity-100" : "opacity-40 hover:opacity-100"
      )}
      style={{
        transform: `translate(${position.x}px, ${position.y}px)`,
        transition: position.x === 0 ? "transform 0.5s cubic-bezier(0.23, 1, 0.32, 1), opacity 0.3s ease" : "opacity 0.3s ease",
      }}
    >
      <span className="cb-entrylist-filter-title text-[14px] md:text-[16px] font-normal leading-tight tracking-tight relative">
        <span data-text={label}>{label}</span>
        {isActive && (
          <span 
            className="absolute -bottom-1 left-0 w-full h-[1px] bg-black"
            style={{ 
                transform: 'scaleX(1)',
                transition: 'transform 0.4s cubic-bezier(0.7, 0, 0.3, 1)'
            }}
          />
        )}
      </span>
    </a>
  );
};

const ProjectFilters = () => {
  const [activeFilter, setActiveFilter] = useState("all");

  const filters = [
    { id: "all", label: "All Projects" },
    { id: "web", label: "Websites" },
    { id: "app", label: "Applications" },
    { id: "branding", label: "Branding" },
  ];

  return (
    <div className="cb-entrylist-filters flex flex-wrap items-center justify-center gap-x-8 gap-y-4 py-8 md:py-12 select-none overflow-hidden">
      {filters.map((filter) => (
        <FilterItem
          key={filter.id}
          label={filter.label}
          isActive={activeFilter === filter.id}
          onClick={() => setActiveFilter(filter.id)}
        />
      ))}
      <style jsx global>{`
        .cb-entrylist-filters {
          margin-bottom: clamp(40px, 5vw, 80px);
        }
        
        /* Specific alignment and styles inherited from computed layout */
        .cb-entrylist-filter-title {
           font-family: var(--font-sans);
           display: inline-block;
        }

        @media (max-width: 768px) {
          .cb-entrylist-filters {
            gap: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default ProjectFilters;