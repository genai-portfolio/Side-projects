"use client";

import React, { useRef, useState } from "react";
import { motion, useSpring, useTransform, useMotionValue } from "framer-motion";

export const MagneticLine = ({ className = "text-black/20 group-hover:text-black/40" }: { className?: string }) => {
    const pathRef = useRef<SVGPathElement>(null);
    const [isHovered, setIsHovered] = useState(false);

    // Mouse position relative to the line's center vertically
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    // Smooth springs for the "pinch" effect
    const springConfig = { damping: 20, stiffness: 150, mass: 0.5 };
    const smoothX = useSpring(mouseX, springConfig);
    const smoothY = useSpring(mouseY, springConfig);

    // We'll create a path string: "M 0 10 Q {mouseX} {mouseY} 1000 10"
    // But we need to keep it responsive. Let's use 100 as the viewBox width.
    const path = useTransform(
        [smoothX, smoothY],
        ([x, y]) => `M 0 10 Q ${x} ${y} 100 10`
    );

    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 20; // 20 is the height of our box

        mouseX.set(x);
        mouseY.set(y);
    };

    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => {
        setIsHovered(false);
        mouseX.set(50); // Reset to center
        mouseY.set(10); // Reset to baseline
    };

    return (
        <div
            className="relative w-full h-[60px] -my-[30px] flex items-center cursor-none group sticky-handle z-10"
            onMouseMove={handleMouseMove}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <svg
                viewBox="0 0 100 20"
                preserveAspectRatio="none"
                className="w-full h-20 pointer-events-none"
            >
                <motion.path
                    d={path}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="0.2"
                    className={`${className} transition-colors duration-300`}
                />
            </svg>
        </div>
    );
};
