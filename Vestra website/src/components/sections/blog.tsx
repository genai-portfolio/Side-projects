"use client";

import React from 'react';
import Image from 'next/image';

/**
 * BlogSection Component
 * 
 * Clones the blog section from the Cuberto website.
 * Features:
 * - Inverse dark background (#000000)
 * - Large editorial heading "Blog"
 * - List of entries with thumbnails, categories, titles, and dates
 * - Smooth hover effects and pixel-perfect spacing based on computed styles
 */
export default function BlogSection() {
  const blogEntries = [
    {
      href: "/blog/how-make-ui-ux-website-development/",
      thumbnail: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/54299d9789b57642a5b0bd39efb37175_03a4f580f1_w1080-15.webp",
      alt: "How to Make UI/UX website // Frontend development",
      category: "Design Course",
      title: "How to Make UI/UX website // Frontend development",
      date: "10/23/2024"
    },
    {
      href: "/blog/how-cook-emotional-site-web-development/",
      thumbnail: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/0dc60d465222db37738a6e2222207dce_0175db0d83_w1080-16.webp",
      alt: "How to Cook an Emotional Site // Web Development",
      category: "Design Course",
      title: "How to Cook an Emotional Site // Web Development",
      date: "10/21/2024"
    },
    {
      href: "/blog/cuberto-mouse-follower/",
      thumbnail: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/016aefcc0949accfcd0c31034dec17d6_d25cd7a401_w1080-17.webp",
      alt: "Cuberto Mouse Follower",
      category: "Dev Source",
      title: "Cuberto Mouse Follower",
      date: "4/11/2022"
    }
  ];

  return (
    <section 
      id="blog" 
      className="bg-[#000000] text-[#FFFFFF] py-[160px] md:py-[200px] lg:py-[240px] relative overflow-hidden"
      style={{ fontFamily: '"Inter", sans-serif' }}
    >
      {/* Curved transition fill - if needed for the liquid scroll feel */}
      <div className="absolute top-0 left-0 w-full h-20 bg-gradient-to-b from-[#FFFFFF] to-transparent opacity-0 pointer-events-none" />

      <div className="container mx-auto px-[5%] max-w-[1440px]">
        {/* Section Header */}
        <div className="mb-16 md:mb-24">
          <h2 
            className="text-[80px] md:text-[100px] lg:text-[120px] font-medium leading-[0.9] tracking-[-0.03em]"
            aria-label="Blog"
          >
            Blog
          </h2>
        </div>

        {/* Blog Entries List */}
        <div className="flex flex-col gap-10 md:gap-14 lg:gap-20">
          {blogEntries.map((item, index) => (
            <div 
              key={index} 
              className="cb-summary-entry group animate-in fade-in slide-in-from-bottom-10 duration-1000 ease-out"
              style={{ animationDelay: `${index * 150}ms`, animationFillMode: 'both' }}
            >
              <a 
                href={item.href} 
                className="block no-underline"
              >
                <div className="grid grid-cols-1 md:grid-cols-[1.2fr_1.8fr] lg:grid-cols-[450px_1fr] gap-8 md:gap-12 lg:gap-20 items-center">
                  {/* Thumbnail Column */}
                  <div className="overflow-hidden rounded-[24px] md:rounded-[40px] aspect-[16/10] relative bg-[#1a1a1a]">
                    <Image
                      src={item.thumbnail}
                      alt={item.alt}
                      fill
                      sizes="(max-width: 768px) 100vw, 450px"
                      className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                      priority={index === 0}
                    />
                  </div>

                  {/* Info Column */}
                  <div className="flex flex-col">
                    <div className="mb-4">
                      <span className="inline-block text-[12px] uppercase tracking-wider border border-white/20 rounded-full px-4 py-1.5 font-medium">
                        {item.category}
                      </span>
                    </div>
                    <h3 className="text-[28px] md:text-[36px] lg:text-[44px] font-medium leading-[1.1] mb-6 transition-opacity duration-300 group-hover:opacity-80">
                      {item.title}
                    </h3>
                    <div className="text-[14px] text-white/50 font-medium">
                      {item.date}
                    </div>
                  </div>
                </div>
              </a>
            </div>
          ))}
        </div>

        {/* Action Button */}
        <div className="mt-20 md:mt-32">
          <a 
            href="/blog/" 
            className="pill-button border-white/20 hover:border-white group flex items-center gap-2 overflow-hidden"
            style={{ 
              borderRadius: '9999px',
              padding: '1rem 3rem',
              fontSize: '18px',
              width: 'max-content'
            }}
          >
            <span className="relative z-10 transition-colors duration-400 group-hover:text-black">
              Visit our blog
            </span>
            {/* Background ripple simulation via CSS class from globals */}
            <div className="absolute inset-0 bg-white translate-y-full transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] group-hover:translate-y-0" />
          </a>
        </div>
      </div>

      <style jsx>{`
        .pill-button {
          position: relative;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border: 1px solid rgba(255, 255, 255, 0.2);
          transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
        }
        .pill-button:hover {
          color: black;
          border-color: white;
        }
      `}</style>
    </section>
  );
}