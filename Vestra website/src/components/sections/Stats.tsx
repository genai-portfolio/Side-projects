"use client";

import React from 'react';

const Stats = () => {
  return (
    <section className="bg-white py-[100px] md:py-[150px] lg:py-[200px]" id="advantage">
      <div className="max-w-[1440px] mx-auto px-10 md:px-20 lg:px-40">
        {/* Large Section Header */}
        <div className="mb-12 lg:mb-20">
          <h2 className="text-[48px] md:text-[80px] lg:text-[100px] font-medium leading-[1] tracking-[-0.04em] text-black">
            Simply put, we dare<br className="hidden md:block" /> what others don't
          </h2>
        </div>

        {/* Horizontal Divider */}
        <div className="w-full h-[1px] bg-[#cccccc] mb-12 lg:mb-16"></div>

        {/* Two Column Grid Overview */}
        <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-10 md:gap-20">
          {/* Left Column: Caption */}
          <div>
            <h3 className="text-[14px] font-bold uppercase tracking-[0.05em] text-black leading-tight">
              Simply put, we dare<br className="hidden md:block" /> what others don't
            </h3>
          </div>

          {/* Right Column: Info and Counters */}
          <div>
            {/* Description Text */}
            <div className="mb-16 lg:mb-24">
              <p className="text-[20px] md:text-[24px] lg:text-[28px] leading-[1.4] text-black mb-10">
                We make things, and we're awesome at it. Vestra is a tight-knit team of experts who are ready to tackle the most intricate puzzles when it comes to websites and mobile apps development. We love what we do and we bet on the success of each and every project we undertake.
              </p>
              <p className="text-[20px] md:text-[24px] lg:text-[28px] leading-[1.4] text-black">
                Mainstream? No, thanks. Because it's not just work, it's passion. It's not just clients, it's people. Every project we take on is important to us, and every client is a big deal. We take care of your projects, your deadlines, and your nerves no matter what, and that’s a promise.
              </p>
            </div>

            {/* Counters */}
            <div className="flex flex-col md:flex-row gap-12 md:gap-16 lg:gap-24">
              {/* Stat Item 1 */}
              <div className="flex flex-col">
                <div className="flex items-baseline">
                  <span className="text-[40px] md:text-[54px] lg:text-[64px] font-medium leading-none text-black">40</span>
                  <span className="text-[32px] md:text-[40px] lg:text-[48px] font-medium leading-none text-black ml-1">+</span>
                </div>
                <span className="text-[14px] font-bold uppercase tracking-[0.05em] text-black mt-4">members</span>
              </div>

              {/* Stat Item 2 */}
              <div className="flex flex-col">
                <div className="flex items-baseline">
                  <span className="text-[40px] md:text-[54px] lg:text-[64px] font-medium leading-none text-black">300</span>
                  <span className="text-[32px] md:text-[40px] lg:text-[48px] font-medium leading-none text-black ml-1">+</span>
                </div>
                <span className="text-[14px] font-bold uppercase tracking-[0.05em] text-black mt-4">completed projects</span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Stats;