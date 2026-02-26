"use client";

import React, { useRef, useState, useEffect } from 'react';
import Image from 'next/image';

interface Project {
  id: string;
  title: string;
  description: string;
  image: string;
  video: string;
  href: string;
  size?: 'normal' | 'small' | 'undefined';
}

const projects: Project[] = [
  {
    id: 'puntopago',
    title: 'Punto Pago',
    description: 'The First Super-App in Latin America',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-1.jpg',
    video: 'https://cuberto.com/assets/projects/puntopago/cover.mp4',
    href: '/projects/puntopago/',
  },
  {
    id: 'kzero',
    title: 'Kelvin Zero',
    description: 'A digital product for passwordless authentication',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-7.jpg',
    video: 'https://cuberto.com/assets/projects/kzero/cover.mp4',
    href: '/projects/kzero/',
    size: 'undefined',
  },
  {
    id: 'daoway',
    title: 'DaoWay',
    description: 'Astrology planner app: plan, achieve, thrive',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-2.jpg',
    video: 'https://cuberto.com/assets/projects/daoway/cover.mp4',
    href: '/projects/daoway/',
    size: 'small',
  },
  {
    id: 'magma',
    title: 'Magma',
    description: 'The ultimate tool for building in the Web3 era',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-8.jpg',
    video: 'https://cuberto.com/assets/projects/magma/cover.mp4',
    href: '/projects/magma/',
  },
  {
    id: 'riyadh',
    title: 'Riyadh',
    description: "Official website of Riyadh, Saudi Arabia's capital",
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-3.jpg',
    video: 'https://cuberto.com/assets/projects/riyadh/cover.mp4',
    href: '/projects/riyadh/',
    size: 'small',
  },
  {
    id: 'flipaclip',
    title: 'FlipaClip',
    description: 'The best tool for stop-motion animation',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-9.jpg',
    video: 'https://cuberto.com/assets/projects/flipaclip/cover.mp4',
    href: '/projects/flipaclip/',
    size: 'small',
  },
  {
    id: 'qvino',
    title: 'Qvino',
    description: 'Wine marketplace with interactive learning',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-4.jpg',
    video: 'https://cuberto.com/assets/projects/qvino/cover.mp4',
    href: '/projects/qvino/',
  },
  {
    id: 'zelt',
    title: 'Zelt',
    description: 'Run HR, IT & Finance in one place',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-10.jpg',
    video: 'https://cuberto.com/assets/projects/zelt/cover.mp4',
    href: '/projects/zelt/',
  },
  {
    id: 'potion',
    title: 'Potion',
    description: 'Sales tool for increasing conversions',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-5.jpg',
    video: 'https://cuberto.com/assets/projects/potion/cover.mp4',
    href: '/projects/potion/',
    size: 'small',
  },
  {
    id: 'ferrumpipe',
    title: 'Ferrumpipe',
    description: 'Galvanized steel metal frame manufacturer',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-11.jpg',
    video: 'https://cuberto.com/assets/projects/ferrumpipe/cover.mp4',
    href: '/projects/ferrumpipe/',
    size: 'small',
  },
  {
    id: 'cisco',
    title: 'Cisco',
    description: 'Cloud based network management',
    image: 'https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-6.jpg',
    video: 'https://cuberto.com/assets/projects/cisco/cover.mp4',
    href: '/projects/cisco/',
    size: 'small',
  }
];

const ProjectCard = ({ project, index }: { project: Project; index: number }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isHovered, setIsHovered] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  // Simple parallax effect simulation
  const [offsetY, setOffsetY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      if (cardRef.current) {
        const rect = cardRef.current.getBoundingClientRect();
        const scrollPercent = (rect.top / window.innerHeight);
        setOffsetY(scrollPercent * 30 * (index % 2 === 0 ? 1 : -1));
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [index]);

  const handleMouseEnter = () => {
    setIsHovered(true);
    videoRef.current?.play().catch(() => { });
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    }
  };

  return (
    <div
      ref={cardRef}
      className={`mb-[8vw] md:mb-[12vw] transition-transform duration-700 ease-out`}
      style={{ transform: `translateY(${offsetY}px)` }}
    >
      <a
        href={project.href}
        className="group block"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <div className={`relative overflow-hidden rounded-[2.5rem] bg-[#1a1a1a] transition-all duration-500 ${project.size === 'small' ? 'aspect-[4/3] w-full' : 'aspect-[1/1.1] w-full'}`}>
          <div
            className="absolute inset-0 transition-transform duration-700 ease-[cubic-bezier(0.19,1,0.22,1)] group-hover:scale-105"
            suppressHydrationWarning
          >
            <Image
              src={project.image}
              alt={project.title}
              fill
              className={`object-cover transition-opacity duration-500 ${isHovered ? 'opacity-0' : 'opacity-100'}`}
              sizes="(max-width: 768px) 100vw, 50vw"
            />
            {isHovered && (
              <video
                ref={videoRef}
                src={project.video}
                autoPlay
                muted
                loop
                playsInline
                className="absolute inset-0 h-full w-full object-cover transition-opacity duration-500 opacity-100"
              />
            )}
          </div>
        </div>
        <div className="mt-6 font-sans">
          <span className="text-[1.2rem] font-bold text-white">{project.title}</span>
          <span className="text-[1.2rem] text-white/50"> – {project.description}</span>
        </div>
      </a>
    </div>
  );
};

const FeaturedProjects = () => {
  const leftColumnProjects = projects.filter((_, i) => i % 2 === 0);
  const rightColumnProjects = projects.filter((_, i) => i % 2 !== 0);

  return (
    <section className="bg-black text-white pt-[10vw] pb-[10vw] px-[5%] overflow-hidden">
      <div className="max-w-[1440px] mx-auto">
        <div className="mb-[8vw]">
          <h2 className="text-[clamp(2.5rem,6vw,6rem)] font-medium tracking-tight">
            Featured projects
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-[80px] items-start">
          {/* Left Column */}
          <div className="flex flex-col pt-0">
            {leftColumnProjects.map((project, idx) => (
              <ProjectCard key={project.id} project={project} index={idx * 2} />
            ))}
          </div>

          {/* Right Column - Asymmetrical offset */}
          <div className="flex flex-col pt-[15vw] md:pt-[25vw]">
            {rightColumnProjects.map((project, idx) => (
              <ProjectCard key={project.id} project={project} index={idx * 2 + 1} />
            ))}
          </div>
        </div>

        <div className="flex justify-center mt-[4vw]">
          <a
            href="/projects/"
            className="group relative inline-flex items-center justify-center px-10 py-4 border border-white/20 rounded-full text-white text-lg font-medium overflow-hidden transition-all duration-500 hover:text-black"
          >
            <span className="relative z-10 transition-colors duration-500">View all projects</span>
            <div className="absolute inset-0 bg-white translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)]" />
          </a>
        </div>
      </div>
    </section>
  );
};

export default FeaturedProjects;