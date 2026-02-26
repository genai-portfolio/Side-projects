"use client";

import React from 'react';

const Hero = () => {
  const headlineWords = [
    "Design",
    "agency",
    "focused",
    "on",
    "AI-driven",
    "products",
  ];

  const descriptionWords = [
    "Vestra",
    "Logics",
    "is",
    "a",
    "digital",
    "design",
    "and",
    "technology",
    "partner",
    "focused",
    "on",
    "smart",
    "interactions,",
    "delightful",
    "UX,",
    "and",
    "cutting-edge",
    "AI",
    "solutions.",
  ];

  return (
    <section className="cb-tophead relative pt-[clamp(5rem,12vw,15rem)] pb-[clamp(5rem,10vw,10rem)] bg-white overflow-hidden">
      <div className="cb-tophead-container -lg container max-w-[1600px] px-[5%] sm:px-[120px]">

        {/* Main Headline */}
        <div className="cb-tophead-title mb-[clamp(2rem,5vw,4rem)]">
          <h1
            className="text-hero font-medium tracking-[-0.03em] leading-[1.1] m-0 p-0 text-center"
            aria-label="Design agency focused on AI-driven products"
          >
            {headlineWords.map((word, index) => (
              <span
                key={index}
                className="inline-block overflow-hidden align-top mr-[0.2em] last:mr-0 pb-[0.1em]"
              >
                <span
                  className="inline-block animate-in fade-in slide-in-from-left-full duration-1000 ease-[cubic-bezier(0.19,1,0.22,1)] fill-mode-both"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  {word}
                </span>
              </span>
            ))}
          </h1>
        </div>

        {/* Sub-description */}
        <div className="cb-tophead-text w-full flex justify-center mt-[clamp(2rem,4vw,3rem)]">
          <div className="max-w-[900px] text-center">
            <p className="text-[clamp(1.1rem,2vw,1.4rem)] text-black leading-[1.6] m-0 p-0 font-normal opacity-85">
              {descriptionWords.map((word, index) => (
                <span
                  key={index}
                  className="inline-block overflow-hidden align-top mr-[0.3em] last:mr-0 pb-[0.1em]"
                >
                  <span
                    className="inline-block animate-in fade-in slide-in-from-left-full duration-700 ease-[cubic-bezier(0.19,1,0.22,1)] fill-mode-both"
                    style={{ animationDelay: `${0.6 + index * 0.03}s` }}
                  >
                    {word}
                  </span>
                </span>
              ))}
            </p>
          </div>
        </div>

      </div>

      {/* Visual background spacing matching high-level design if needed,
          but currently kept clean per the 'minimalist' instruction */}
    </section>
  );
};

export default Hero;