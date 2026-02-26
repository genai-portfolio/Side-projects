"use client";

import { MagneticLine } from '../ui/MagneticLine';

/**
 * Solutions Component
 * This component clones the "Our solutions" section from the Cuberto services page.
 * It features a clean grid layout with service names on the left, 
 * detailed descriptions on the right, and interactive "Read more" buttons.
 * The layout is separated by interactive MagneticLine dividers.
 */
const Solutions: React.FC = () => {
    const solutionsData = [
        {
            id: 'websites',
            title: 'Websites and platforms',
            description: 'In our team, developers work alongside designers. This is crucial in creating a fast and responsive website that would excite the audience.',
            link: '/services/digital/'
        },
        {
            id: 'mobile',
            title: 'Mobile applications',
            description: "Cuberto doesn't do cookie-cutter solutions. Every mobile app involves stages of target audience research and prototype testing. The result? A product that’s perfectly suited to your users.",
            link: '/services/mobile/'
        },
        {
            id: 'branding',
            title: 'Strategy and branding',
            description: 'We identify your brand by developing a logo, corporate identity, user manuals, any mockups, and souvenir products. Whatever it takes to get your brand noticed.',
            link: '/services/branding/'
        }
    ];

    return (
        <section
            id="solutions"
            className="bg-white py-[160px] md:py-[120px] sm:py-[80px]"
            data-cursor="-inverse"
        >
            <div className="container mx-auto max-w-[1440px] px-[2.5rem] md:px-[1.5rem]">
                {/* Section Header */}
                <div className="mb-[60px] md:mb-[40px]">
                    <h2
                        className="text-[clamp(2.5rem,6vw,5rem)] font-medium tracking-[-0.02em] leading-[1.1] text-black"
                        aria-label="Our solutions"
                    >
                        Our solutions
                    </h2>
                </div>

                {/* Solutions List */}
                <div className="flex flex-col">
                    {solutionsData.map((item, index) => (
                        <div key={item.id} className="w-full">
                            {/* Interactive Divider */}
                            <MagneticLine />

                            {/* Grid Layout for each service */}
                            <div className="grid grid-cols-12 py-[60px] md:py-[40px] gap-y-8">
                                {/* Left Column: Title */}
                                <div className="col-span-12 md:col-span-4">
                                    <h3 className="text-[1.25rem] md:text-[1.5rem] font-medium leading-[1.2] uppercase tracking-[0.05em] text-black">
                                        {item.title}
                                    </h3>
                                </div>

                                {/* Right Column: Info and CTA */}
                                <div className="col-span-12 md:col-span-8 md:pl-[40px] lg:pl-[80px]">
                                    <div className="max-w-[600px]">
                                        <p className="text-[1.5rem] md:text-[1.25rem] sm:text-[1.125rem] leading-[1.5] font-normal text-black mb-[40px]">
                                            {item.description}
                                        </p>

                                        <div className="flex">
                                            <a
                                                href={item.link}
                                                className="group relative inline-flex items-center justify-center px-[40px] py-[18px] border border-black rounded-full overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.19,1,0.22,1)]"
                                            >
                                                {/* Ripple effect background */}
                                                <span className="absolute inset-0 bg-black translate-y-[101%] group-hover:translate-y-0 transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)]"></span>

                                                {/* Button Text */}
                                                <span
                                                    className="relative z-10 text-[0.875rem] font-medium uppercase tracking-[0.05em] text-black group-hover:text-white transition-colors duration-500"
                                                    data-text="Read more"
                                                >
                                                    Read more
                                                </span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                    {/* Final closing Divider */}
                    <MagneticLine />
                </div>
            </div>

            {/* Styles for specific typography and interactions not covered by global base */}
            <style jsx>{`
                h3 {
                    font-size: 0.875rem; /* Overriding local H3 to match the tiny caps in screenshot */
                    letter-spacing: 0.05em;
                }
                @media (min-width: 768px) {
                    h3 {
                        font-size: 0.875rem;
                    }
                }
            `}</style>
        </section>
    );
};

export default Solutions;