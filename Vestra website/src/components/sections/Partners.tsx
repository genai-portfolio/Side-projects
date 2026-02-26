"use client";

import React from 'react';

const Partners = () => {
  const partners = [
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/raiffeisen-1.svg",
      alt: "Raiffeisen Bank",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/mapbox-2.svg",
      alt: "Mapbox",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/cisco-3.svg",
      alt: "Cisco",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/spark-4.svg",
      alt: "Spark",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/tradingview-5.svg",
      alt: "TradingView",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/tinkoff-6.svg",
      alt: "Tinkoff Bank",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/yandex-7.svg",
      alt: "Yandex",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/etihad-8.svg",
      alt: "Bank al Etihad",
    },
    {
      src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/svgs/euroauto-9.svg",
      alt: "EuroAuto",
    },
  ];

  return (
    <div className="bg-[#ffffff]">
      {/* Video Preview Section */}
      <section className="py-[100px] md:py-[150px]">
        <div className="container px-[40px] max-w-[1440px] mx-auto">
          <div className="rounded-[40px] overflow-hidden bg-[#f2f2f2] aspect-video w-full max-w-[1100px] mx-auto">
            <video
              className="w-full h-full object-cover"
              autoPlay
              muted
              loop
              playsInline
              src="https://cuberto.com/assets/about/screenshot/3.mp4"
            />
          </div>
        </div>
      </section>

      {/* Partners Logo Grid Section */}
      <section id="partners" className="pb-[150px]">
        <div className="container px-[40px] max-w-[1440px] mx-auto">
          <div className="flex flex-col gap-[80px]">
            {/* Header */}
            <h2
              className="text-[48px] md:text-[80px] lg:text-[100px] font-medium leading-[1] tracking-[-0.04em] max-w-[900px]"
              aria-label="We work with people from all over the world"
            >
              We work with<br className="hidden md:block" /> people from all<br className="hidden md:block" /> over the world
            </h2>

            {/* Logo Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-y-[100px] md:gap-y-[140px] gap-x-[40px]">
              {partners.map((partner, index) => (
                <div
                  key={index}
                  className="flex items-center justify-start md:justify-center grayscale hover:grayscale-0 transition-all duration-500 opacity-60 hover:opacity-100"
                >
                  <picture>
                    <img
                      src={partner.src}
                      alt={partner.alt}
                      className="h-[45px] md:h-[65px] w-auto object-contain"
                      loading="lazy"
                    />
                  </picture>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Partners;