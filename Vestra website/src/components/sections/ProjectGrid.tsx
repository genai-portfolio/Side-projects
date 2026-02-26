"use client";

import React, { useState, useEffect, useRef } from 'react';
import Image from 'next/image';

interface Project {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  categories: string[];
}

const projects: Project[] = [
  {
    id: "puntopago",
    title: "Punto Pago",
    description: "The First Super-App in Latin America",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-1.jpg",
    categories: ["app", "branding"],
  },
  {
    id: "kzero",
    title: "Kelvin Zero",
    description: "A digital product for passwordless authentication",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-2.jpg",
    categories: ["web"],
  },
  {
    id: "daoway",
    title: "DaoWay",
    description: "Astrology planner app: plan, achieve, thrive",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-3.jpg",
    categories: ["app"],
  },
  {
    id: "flipaclip",
    title: "FlipaClip",
    description: "The best tool for stop-motion animation",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-4.jpg",
    categories: ["web"],
  },
  {
    id: "riyadh",
    title: "Riyadh",
    description: "Official website of Riyadh, Saudi Arabia's capital",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-5.jpg",
    categories: ["web", "app"],
  },
  {
    id: "zelt",
    title: "Zelt",
    description: "Run HR, IT & Finance in one place",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-6.jpg",
    categories: ["web", "branding"],
  },
  {
    id: "potion",
    title: "Potion",
    description: "Sales tool for increasing conversions",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-7.jpg",
    categories: ["web"],
  },
  {
    id: "magma",
    title: "Magma",
    description: "The ultimate tool for building in the Web3 era",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-8.jpg",
    categories: ["web"],
  },
  {
    id: "cisco",
    title: "Cisco",
    description: "Cloud based network management",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-9.jpg",
    categories: ["branding"],
  },
  {
    id: "qvino",
    title: "Qvino",
    description: "Wine marketplace with interactive learning",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-10.jpg",
    categories: ["app"],
  },
  {
    id: "ferrumpipe",
    title: "Ferrumpipe",
    description: "Galvanized steel metal frame manufacturer",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-11.jpg",
    categories: ["web"],
  },
  {
    id: "nurseclub",
    title: "Nurse CE Club",
    description: "Website revamp with 3D graphics",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-12.jpg",
    categories: ["web", "branding"],
  },
  {
    id: "ulesson",
    title: "uLesson",
    description: "Online platform for distance learning",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-13.jpg",
    categories: ["web", "app"],
  },
  {
    id: "sleepiest",
    title: "Sleepiest",
    description: "Sleep app helps millions fall asleep every night",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-14.jpg",
    categories: ["app"],
  },
  {
    id: "euroauto",
    title: "EuroAuto",
    description: "Largest auto parts supplier in Russia",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-15.jpg",
    categories: ["app"],
  },
  {
    id: "genesis",
    title: "Genesis Vision",
    description: "Private trust management and trading platform",
    imageUrl: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-16.jpg",
    categories: ["app"],
  },
];

const categories = [
  { label: 'All Projects', id: 'all' },
  { label: 'Websites', id: 'web' },
  { label: 'Applications', id: 'app' },
  { label: 'Branding', id: 'branding' },
];

export default function ProjectGrid() {
  const [activeFilter, setActiveFilter] = useState('all');
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHoveringCard, setIsHoveringCard] = useState(false);
  const cursorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const filteredProjects = activeFilter === 'all' 
    ? projects 
    : projects.filter(p => p.categories.includes(activeFilter));

  return (
    <section className="relative w-full bg-white pt-[120px] pb-[120px] lg:pt-[200px] lg:pb-[200px]">
      {/* Custom Cursor */}
      <div 
        ref={cursorRef}
        className={`pointer-events-none fixed z-[9999] flex items-center justify-center rounded-full bg-black text-white transition-all duration-300 ease-[cubic-bezier(0.23,1,0.32,1)] ${
          isHoveringCard ? 'h-[100px] w-[100px] opacity-100 scale-100' : 'h-0 w-0 opacity-0 scale-0'
        }`}
        style={{
          left: mousePos.x,
          top: mousePos.y,
          transform: 'translate(-50%, -50%)',
        }}
      >
        <span className="text-[14px] font-medium tracking-tight">Explore</span>
      </div>

      <div className="container mx-auto px-[5vw]">
        {/* Header Section */}
        <div className="mb-[60px] lg:mb-[100px]">
          <h1 className="mb-8 text-[8.5vw] font-medium leading-[0.9] tracking-[-0.05em] text-black">
            Our projects
          </h1>
          <p className="max-w-[800px] text-[2.2rem] font-normal leading-[1.3] tracking-[-0.02em] text-black/80">
            We help bring ideas to life and create digital products that work.
          </p>
        </div>

        {/* Filters */}
        <div className="mb-[60px] flex flex-wrap gap-x-8 gap-y-4 lg:mb-[80px]">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveFilter(cat.id)}
              className={`cb-filter-item relative pb-1 text-[1.1rem] transition-all duration-300 ${
                activeFilter === cat.id ? 'active opacity-100 font-medium' : 'opacity-40 hover:opacity-100'
              }`}
            >
              <span className="block">{cat.label}</span>
              {activeFilter === cat.id && (
                <span className="absolute bottom-0 left-0 h-[1px] w-full bg-black" />
              )}
            </button>
          ))}
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 gap-x-[40px] gap-y-[40px] md:grid-cols-2 lg:gap-x-[40px] lg:gap-y-[60px]">
          {filteredProjects.map((project, index) => (
            <div 
              key={project.id}
              className={`group flex flex-col ${index % 2 !== 0 ? 'md:mt-[120px]' : ''}`}
            >
              <a 
                href={`/projects/${project.id}`}
                className="block cursor-none"
                onMouseEnter={() => setIsHoveringCard(true)}
                onMouseLeave={() => setIsHoveringCard(false)}
              >
                <div className="relative aspect-[4/5] overflow-hidden rounded-[30px] lg:rounded-[40px] bg-[#f0f0f0]">
                  <Image
                    src={project.imageUrl}
                    alt={project.title}
                    fill
                    className="object-cover transition-transform duration-[800ms] ease-[cubic-bezier(0.7,0,0.3,1)] group-hover:scale-105"
                    sizes="(max-width: 768px) 100vw, 45vw"
                    priority={index < 4}
                  />
                </div>
                <div className="mt-6 mb-8 lg:mt-8">
                  <p className="text-[1.1rem] leading-[1.4] text-[#212121]">
                    <span className="font-semibold text-black">{project.title}</span>
                    <span className="mx-2">–</span>
                    {project.description}
                  </p>
                </div>
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}