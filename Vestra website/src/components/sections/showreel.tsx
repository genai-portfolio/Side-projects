"use client";

import React, { useState, useRef, useEffect } from "react";
import { X } from "lucide-react";

const ShowreelSection = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setCursorPos({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
    }
  };

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
    if (!isModalOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  };

  useEffect(() => {
    return () => {
      document.body.style.overflow = "auto";
    };
  }, []);

  return (
    <>
      <section
        ref={containerRef}
        className="cb-preview relative w-full overflow-hidden"
        onMouseMove={handleMouseMove}
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
        onClick={toggleModal}
        id="showreel"
        style={{ padding: "0 5%" }}
      >
        <div className="cb-preview-container max-w-[1440px] mx-auto py-20 lg:py-40">
          <div 
            className="cb-preview-main relative cursor-none group"
            style={{ borderRadius: "2.5rem", overflow: "hidden" }}
          >
            {/* Custom Play Cursor */}
            <div
              className={`fixed pointer-events-none z-50 flex items-center justify-center transition-transform duration-300 ease-out bg-black rounded-full text-white font-medium text-sm tracking-tight ${
                isHovering ? "scale-100" : "scale-0"
              }`}
              style={{
                left: cursorPos.x + (containerRef.current?.getBoundingClientRect().left || 0),
                top: cursorPos.y + (containerRef.current?.getBoundingClientRect().top || 0),
                width: "100px",
                height: "100px",
                marginLeft: "-50px",
                marginTop: "-50px",
              }}
            >
              PLAY
            </div>

            <div className="cb-preview-media aspect-video w-full bg-neutral-100">
              <video
                autoPlay
                muted
                loop
                playsInline
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              >
                <source src="https://cuberto.com/assets/showreel/short.mp4" type="video/mp4" />
                <source src="https://cuberto.com/assets/showreel/short-sm.mp4" type="video/mp4" />
              </video>
            </div>
          </div>
        </div>
      </section>

      {/* Video Modal */}
      {isModalOpen && (
        <div 
          className="fixed inset-0 z-[100] flex items-center justify-center bg-white"
          style={{ animation: "fadeIn 0.5s cubic-bezier(0.19, 1, 0.22, 1) forwards" }}
        >
          {/* Close button Area / Custom Close Cursor */}
          <button 
            onClick={toggleModal}
            className="absolute top-8 right-8 z-[110] p-4 bg-black rounded-full text-white hover:scale-110 transition-transform"
          >
            <X size={24} />
          </button>

          <div className="w-full h-full p-4 lg:p-12 flex items-center justify-center">
            <div className="relative w-full h-full max-w-[1440px] rounded-[2.5rem] overflow-hidden bg-black shadow-2xl">
              <video
                autoPlay
                controls
                className="w-full h-full object-contain"
              >
                <source src="https://cuberto.com/assets/showreel/full-1440-60.mp4" type="video/mp4" />
                <source src="https://cuberto.com/assets/showreel/full-1080-60.mp4" type="video/mp4" />
              </video>
            </div>
          </div>
        </div>
      )}

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .cb-preview-main {
           transform: translateZ(0);
           -webkit-mask-image: -webkit-radial-gradient(white, black);
        }
      `}</style>
    </>
  );
};

export default ShowreelSection;