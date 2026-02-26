"use client";

import React from 'react';
import Image from 'next/image';

/**
 * SplitShow Component
 * 
 * A dual-image showcase section featuring two offset images with rounded corners,
 * maintaining the specific spacing and aspect ratios as per the design instructions.
 */
const SplitShow: React.FC = () => {
  // Asset URLs from provided assets list
  const leftImage = "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/3-2.jpg";
  const rightImage = "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/2-3.jpg";

  return (
    <section className="cb-splitshow relative w-full overflow-hidden bg-white py-[80px] md:py-[120px] lg:py-[150px]">
      <div className="cb-splitshow-content mx-auto max-w-[1440px] px-10">
        <div className="cb-splitshow-container w-full">
          <div className="cb-splitshow-items flex flex-col md:flex-row md:items-start md:justify-between gap-10 md:gap-0">
            
            {/* Left Column - Image is smaller and positioned higher usually in such layouts or based on offset */}
            <div className="cb-splitshow-col -left w-full md:w-[45%] lg:w-[42%]">
              <div className="cb-splitshow-item transform transition-transform duration-700 ease-out hover:scale-[1.02]">
                <div className="cb-splitshow-preview rounded-[40px] overflow-hidden bg-[#f2f2f2] aspect-[3/4] relative">
                  <Image
                    src={leftImage}
                    alt="Creative process work session"
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, 45vw"
                    priority
                  />
                </div>
              </div>
            </div>

            {/* Right Column - Image is typically offset downwards for a dynamic feel */}
            <div className="cb-splitshow-col -right w-full md:w-[45%] lg:w-[48%] md:mt-[150px] lg:mt-[200px]">
              <div className="cb-splitshow-item transform transition-transform duration-700 ease-out hover:scale-[1.02]">
                <div className="cb-splitshow-preview rounded-[40px] overflow-hidden bg-[#f2f2f2] aspect-[4/5] relative">
                  <Image
                    src={rightImage}
                    alt="Team collaborative creative direction"
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, 50vw"
                    priority
                  />
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>
  );
};

export default SplitShow;