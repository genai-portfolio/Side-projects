"use client";

import React from 'react';
import { Hexagon, Sparkles, Lock, CircleDot } from 'lucide-react';
import { MagneticLine } from '../ui/MagneticLine';

const benefitItems = [
  {
    icon: <Hexagon className="w-[32px] h-[32px] text-white stroke-[1.5]" />,
    title: "TIME ZONES AIN’T NO THING",
    description: "Wherever you are in the world, you’ll feel like we’re right around the corner. With 12 years of experience, our business processes are seamless and time differences don’t matter."
  },
  {
    icon: <Sparkles className="w-[32px] h-[32px] text-white stroke-[1.5]" />,
    title: "IMPOSSIBLE? WE’RE ON IT",
    description: "“Impossible” simply does not exist in our vocabulary. We develop products exactly as they were at the design stage, no simplifications, no shortcuts, no BS."
  },
  {
    icon: <Lock className="w-[32px] h-[32px] text-white stroke-[1.5]" />,
    title: "FLEXIBLE WORK TERMS",
    description: "Just like we stick to a fixed budget, we stay within a set Time and Materials framework. Whatever terms we agree to will depend on your project needs."
  },
  {
    icon: <CircleDot className="w-[32px] h-[32px] text-white stroke-[1.5]" />,
    title: "FULL SPECTRUM OF SERVICES",
    description: "Any solution your business needs, we’re on it: creating logos, development, interface design prior to development, technical support, and marketing."
  }
];

export default function Benefits() {
  return (
    <section className="bg-white py-10 md:py-20 overflow-hidden">
      <div className="container mx-auto px-5 md:px-10">
        <div className="bg-[#111111] rounded-[40px] md:rounded-[80px] p-10 md:p-24 lg:p-32 text-white">
          <div className="max-w-[1440px] mx-auto">
            {/* Heading */}
            <div className="mb-20 md:mb-32">
              <h2 className="text-[48px] md:text-[80px] lg:text-[100px] leading-[1] font-medium tracking-tight max-w-[800px]">
                Benefits of <br /> working with us
              </h2>
            </div>

            {/* Benefits List */}
            <div className="space-y-0">
              {benefitItems.map((benefit, index) => (
                <div key={index} className="group">
                  {/* Interactive Divider (Top) */}
                  <MagneticLine className="text-white/20 group-hover:text-white/40" />

                  <div className="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-10 py-12 md:py-20 items-start">
                    {/* Icon Col */}
                    <div className="md:col-span-2 flex items-center">
                      <div className="opacity-80 group-hover:opacity-100 transition-opacity duration-300">
                        {benefit.icon}
                      </div>
                    </div>

                    {/* Label Col */}
                    <div className="md:col-span-4 self-start">
                      <span className="text-[12px] md:text-[14px] font-bold tracking-[0.1em] uppercase block mb-4 text-white/60">
                        {benefit.title}
                      </span>
                    </div>

                    {/* Description Col */}
                    <div className="md:col-span-6">
                      <p className="text-[20px] md:text-[24px] lg:text-[28px] leading-[1.4] font-normal text-white/80 max-w-[580px]">
                        {benefit.description}
                      </p>
                    </div>
                  </div>
                  {index === benefitItems.length - 1 && (
                    /* Final Interactive Divider (Bottom) */
                    <MagneticLine className="text-white/20 group-hover:text-white/40" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}