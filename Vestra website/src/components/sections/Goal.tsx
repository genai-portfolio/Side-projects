"use client";

import React from 'react';

const Goal: React.FC = () => {
  return (
    <section 
      className="cb-overview py-[100px] md:py-[150px] lg:py-[200px]" 
      id="goal"
      style={{ backgroundColor: '#ffffff', color: '#000000' }}
    >
      <div className="cb-overview-content px-5 md:px-10 lg:px-[80px]">
        <div className="container-lg mx-auto max-w-[1440px]">
          <div className="grid-overview grid md:grid-cols-[1fr_2fr] gap-10 md:gap-20">
            {/* Left Column: Caption */}
            <div className="cb-overview-grid-col -left">
              <div className="cb-overview-caption">
                <h2 className="text-[32px] md:text-[48px] lg:text-[64px] font-medium leading-[1] tracking-[-0.04em] uppercase">
                  <span>Our</span> <br />
                  <span>goal</span>
                </h2>
              </div>
            </div>

            {/* Right Column: Body Text */}
            <div className="cb-overview-grid-col -right">
              <div className="cb-overview-info">
                <div className="cb-overview-text">
                  <p className="text-[20px] md:text-[24px] lg:text-[28px] leading-[1.4] font-normal tracking-tight text-black max-w-[800px]">
                    From the moment our company was founded, we have helped our clients 
                    find exceptional solutions for their businesses, creating memorable 
                    brands and digital products. Our expertise grows with each year, and 
                    our accumulated experience empowers us to develop products exactly 
                    as they should be.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .container-lg {
          width: 100%;
          margin-left: auto;
          margin-right: auto;
        }
        
        @media (min-width: 1024px) {
          .grid-overview {
            display: grid;
            grid-template-columns: 1fr 2fr;
          }
        }

        h2 span {
          display: inline-block;
        }

        p span {
          display: inline-block;
          margin-right: 0.2em;
        }
      `}</style>
    </section>
  );
};

export default Goal;