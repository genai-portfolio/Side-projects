"use client";

import React, { useState, useRef } from "react";

const servicesData = [
  {
    title: "Brand Identity",
    description: "Strategic design that positions AI products for trust and clarity.",
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-12.png",
    video: "https://cuberto.com/assets/services/branding/cover.mp4?3",
    size: "large",
  },
  {
    title: "AI-enhanced UX/UI design",
    description: "Interfaces that adapt, predict, and respond intelligently.",
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-13.png",
    video: "https://cuberto.com/assets/services/design/cover.mp4",
    size: "small",
  },
  {
    title: "Custom development",
    description: "Frontend + backend + AI integrations — built for performance and scalability.",
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/cover-14.png",
    video: "https://cuberto.com/assets/services/development/cover.mp4",
    size: "small",
  },
];

const ServiceCard = ({ service }: { service: typeof servicesData[0] }) => {
  const [isHovered, setIsHovered] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleMouseEnter = () => {
    setIsHovered(true);
    if (videoRef.current) {
      videoRef.current.play().catch(() => {});
    }
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
      className="flex flex-col gap-6"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div 
        className={`relative overflow-hidden rounded-[2.5rem] bg-[#f5f5f5] transition-transform duration-700 ease-out cursor-pointer ${
          service.size === 'large' ? 'aspect-[4/5]' : 'aspect-square'
        } ${isHovered ? 'scale-[0.98]' : 'scale-100'}`}
      >
        {/* Background Image */}
        <img
          src={service.image}
          alt={service.title}
          className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-500 ${
            isHovered ? 'opacity-0' : 'opacity-100'
          }`}
        />
        
        {/* Hover Video */}
        <video
          ref={videoRef}
          src={service.video}
          muted
          loop
          playsInline
          className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-500 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}
        />
      </div>

      <div className="flex flex-col gap-2 px-2">
        <h3 className="text-[2.2rem] md:text-[2.8rem] font-medium tracking-tight leading-none text-black">
          {service.title}
        </h3>
        <p className="text-[1.125rem] md:text-[1.25rem] leading-[1.4] text-black max-w-[400px]">
          {service.description}
        </p>
      </div>
    </div>
  );
};

export default function OurServices() {
  return (
    <section id="services" className="bg-white py-24 md:py-40">
      <div className="container mx-auto px-[5%]">
        <div className="mb-20 md:mb-32">
          <h2 className="text-[clamp(3rem,8vw,6rem)] font-medium leading-[1.1] text-black mb-12">
            Our services
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-x-20 gap-y-24">
          {/* Left Column */}
          <div className="flex flex-col gap-24">
            <div className="max-w-[480px]">
              <p className="text-[clamp(1.5rem,3vw,2.2rem)] font-medium leading-[1.3] text-black">
                From motion design to AI-powered products — we design and build interfaces for the future.
              </p>
            </div>
            
            <ServiceCard service={servicesData[0]} />
          </div>

          {/* Right Column */}
          <div className="flex flex-col gap-24 lg:pt-32">
            <ServiceCard service={servicesData[1]} />
            <ServiceCard service={servicesData[2]} />
          </div>
        </div>

        {/* Action Button */}
        <div className="mt-24 md:mt-40 flex justify-center">
          <a
            href="/services/"
            className="group relative inline-flex items-center justify-center rounded-full border border-black/10 px-12 py-6 text-[1.125rem] font-medium transition-all duration-500 hover:bg-black hover:text-white"
          >
            <span className="relative z-10">View all services</span>
            <div className="absolute inset-x-0 bottom-0 h-0 w-full bg-black transition-all duration-500 ease-out group-hover:h-full group-hover:top-0" />
          </a>
        </div>
      </div>
    </section>
  );
}