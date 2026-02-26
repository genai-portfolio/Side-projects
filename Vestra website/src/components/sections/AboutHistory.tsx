"use client";

import React from 'react';

const AboutHistory: React.FC = () => {
  return (
    <section
      className="cb-overview py-[150px] md:py-[200px] bg-background text-foreground"
      id="history"
    >
      <div className="container overflow-hidden">
        {/* Large Headline */}
        <div className="mb-[60px] md:mb-[80px]">
          <h2
            className="text-[clamp(48px,8vw,100px)] leading-[1] font-medium tracking-[-0.04em] mb-10"
            aria-label="Get to know us, see what's up"
          >
            <span>Get to know us,</span>
            <br />
            <span>see what's up</span>
          </h2>

          {/* Section Divider */}
          <div className="w-full h-[1px] bg-border mt-10" />
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-20">
          {/* Left Column: Caption */}
          <div className="md:col-span-1">
            <h3 className="text-[14px] font-bold uppercase tracking-[0.05em] leading-[1.2]">
              Get to know us,<br />see what's up
            </h3>
          </div>

          {/* Right Column: Detailed Text */}
          <div className="md:col-span-2 max-w-[800px]">
            <div className="space-y-12">
              <p className="text-[clamp(18px,2.2vw,28px)] leading-[1.4] font-normal">
                Two brothers, Hanzla and Bilal, founded the company in 2025. Starting as a dedicated team of freelancers specializing in web and mobile design, we have since evolved to embrace the forefront of artificial intelligence. Today, we focus on developing AI-powered applications, Large Language Models (LLMs), and cutting-edge digital solutions.
              </p>

              <div className="text-[clamp(18px,2.2vw,28px)] leading-[1.4] font-normal space-y-8">
                <p>
                  Today, Vestra has grown to a full-cycle agency with attested design expertise. We are in the TOP 10 design agencies according to the most popular design communities in the world, receive international awards for our exceptional products, work with large companies all over the world, teach our own design courses, and gladly share our expertise with you.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutHistory;