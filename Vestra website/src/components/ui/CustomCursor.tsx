"use client";

import React, { useEffect, useState } from 'react';
import { motion, useSpring } from 'framer-motion';

const CustomCursor = () => {
    const [isVisible, setIsVisible] = useState(false);

    // Smooth springs for tracking
    const springConfig = { damping: 25, stiffness: 250 };
    const cursorX = useSpring(0, springConfig);
    const cursorY = useSpring(0, springConfig);

    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            cursorX.set(e.clientX - 5);
            cursorY.set(e.clientY - 5);

            // Auto-detect visibility: Hide specifically on Showreel container
            const target = e.target as HTMLElement;
            const onVideo = target?.closest?.('.cb-preview-main');
            setIsVisible(!onVideo);
        };

        const handleMouseLeave = () => setIsVisible(false);
        const handleMouseEnter = () => setIsVisible(true);

        window.addEventListener('mousemove', handleMouseMove, { passive: true });
        document.addEventListener('mouseleave', handleMouseLeave);
        document.addEventListener('mouseenter', handleMouseEnter);

        // Initial check for visibility if mouse is already in window
        setIsVisible(true);

        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseleave', handleMouseLeave);
            document.removeEventListener('mouseenter', handleMouseEnter);
        };
    }, []);

    return (
        <motion.div
            className="fixed top-0 left-0 w-[10px] h-[10px] bg-white rounded-full pointer-events-none z-[9999999] mix-blend-difference shadow-[0_0_10px_rgba(255,255,255,0.8)]"
            initial={false}
            animate={{ opacity: isVisible ? 1 : 0 }}
            style={{
                x: cursorX,
                y: cursorY,
            }}
        />
    );
};

export default CustomCursor;
