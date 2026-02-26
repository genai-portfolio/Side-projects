"use client";

import React from 'react';
import Image from 'next/image';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay } from 'swiper/modules';

// Import Swiper styles
import 'swiper/css';

interface Testimonial {
  author: string;
  text: string;
}

const testimonials: Testimonial[] = [
  {
    author: "Potion",
    text: "Cuberto was engaged in developing our website and additional marketing materials, including theming and various creative assignments. Their efforts were highly satisfactory, and we were impressed with the Cuberto team's collaborative approach. Their team were amiable and accommodating to all of our requests, and also provided invaluable creative direction to the project."
  },
  {
    author: "Cisco - Tetration",
    text: "On behalf of the Cisco - Tetration team, I would like to thank Cuberto for the very successful collaboration and design contribution to our product. Our teams worked in sync, and we did not experience any discomfort in communication."
  },
  {
    author: "Zelt",
    text: "We have worked with Cuberto on our new image Zelt website. The team performed great in terms of creating a unique design style and developing complex 3D animations."
  },
  {
    author: "App Store User",
    text: "It was pleasure to work with Cuberto, we developed App together that has 4.8 rating in store and more than 100 000 installs. My recommendations!"
  }
];

const Testimonials: React.FC = () => {
  return (
    <section className="relative w-full bg-white pt-[150px] pb-[100px] md:pt-[200px] md:pb-[150px]">
      <div className="container mx-auto px-[40px] max-w-[1440px]">
        {/* Main Section Divider */}
        <div className="w-full h-[1px] bg-[#cccccc] mb-[60px] md:mb-[80px]"></div>

        {/* 2-Column Grid for Carousel */}
        <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-[40px] md:gap-[80px]">
          {/* Left Column: Heading */}
          <div className="flex flex-col">
            <h3 className="text-[14px] font-bold uppercase tracking-[0.05em] text-black">
              Feedback from<br />our clients
            </h3>
          </div>

          {/* Right Column: Swiper Carousel */}
          <div className="relative overflow-hidden">
            <Swiper
              modules={[Autoplay]}
              spaceBetween={50}
              slidesPerView={1}
              speed={800}
              autoplay={{
                delay: 5000,
                disableOnInteraction: false,
              }}
              loop={true}
              className="w-full"
            >
              {testimonials.map((item, index) => (
                <SwiperSlide key={index}>
                  <div className="flex flex-col">
                    {/* Author Marker */}
                    <div className="flex items-center gap-[15px] mb-[30px]">
                      <div className="w-[40px] h-[1px] bg-black"></div>
                      <span className="text-[18px] font-bold text-black uppercase">{item.author}</span>
                    </div>

                    {/* Testimonial Text */}
                    <div className="text-black mb-[40px]">
                      <p className="text-[22px] md:text-[28px] leading-[1.4] font-normal tracking-tight">
                        &quot;{item.text}&quot;
                      </p>
                    </div>

                    {/* CTA Button */}
                    <div className="mt-4">
                      <a 
                        href="#" 
                        className="inline-flex items-center justify-center px-[35px] py-4 rounded-full border border-black text-[18px] font-medium transition-all duration-500 hover:bg-black hover:text-white"
                      >
                        See the interview
                      </a>
                    </div>
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>
          </div>
        </div>

        {/* Dual-Image Collaboration Layout Below Carousel */}
        <div className="mt-24 md:mt-32 w-full">
          <div className="grid grid-cols-1 md:grid-cols-[1.2fr_1fr] gap-[40px] md:gap-[60px] items-start">
            {/* Left Image: Video/Code Focus */}
            <div className="relative w-full aspect-[4/3] rounded-[40px] overflow-hidden bg-[#f2f2f2]">
              <Image 
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/5-5.jpg"
                alt="Team working on code"
                fill
                className="object-cover transition-transform duration-700 hover:scale-105"
                sizes="(max-width: 768px) 100vw, 60vw"
              />
            </div>

            {/* Right Image: Interaction Focus, Offset Down */}
            <div className="relative w-full aspect-[4/3] rounded-[40px] overflow-hidden bg-[#f2f2f2] md:mt-[100px]">
              <Image 
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/6-6.jpg"
                alt="Collaborative meeting"
                fill
                className="object-cover transition-transform duration-700 hover:scale-105"
                sizes="(max-width: 768px) 100vw, 40vw"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;