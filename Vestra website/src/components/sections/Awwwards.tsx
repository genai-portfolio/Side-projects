"use client";

import React from 'react';
import Image from 'next/image';

/**
 * AwwwardsSection Component
 * 
 * This component clones the award highlight section of the Cuberto website.
 * It includes the "Agency of the Year" headline, a descriptive paragraph, 
 * and the office atmosphere photo with soft interior lighting.
 */
const AwwwardsSection: React.FC = () => {
  return (
    <div className="bg-white">
      {/* Photo Section - Office Atmosphere */}
      <section className="cb-preview py-[80px] md:py-[120px] lg:py-[150px]">
        <div className="container px-5 md:px-10 max-w-[1440px] mx-auto">
          <div className="cb-preview-main max-w-[1100px] mx-auto">
            <div className="relative overflow-hidden rounded-[30px] md:rounded-[40px] aspect-[16/9] w-full">
              <Image
                src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/2-4.jpg"
                alt="Cuberto Office Atmosphere"
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 1100px"
                priority
              />
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};

export default AwwwardsSection;