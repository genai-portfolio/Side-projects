"use client";

import React, { useEffect, useState } from "react";
import Image from "next/image";
import { X } from "lucide-react";

/**
 * Assets mapping from the provided list
 */
const EMOJI_ASSETS = {
  success: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/1F44D-1.png", // Thumbs up
  error: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/images/1F631-2.png", // Screaming face
  wink: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/1d36a954-389b-4c40-ac22-c1dd3f460c00-cuberto-com/assets/icons/1F609-1.png", // Wink emoji
};

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: "success" | "error";
}

export default function Modals({ isOpen, onClose, type }: ModalProps) {
  const [shouldRender, setShouldRender] = useState(isOpen);

  useEffect(() => {
    if (isOpen) {
      setShouldRender(true);
      document.body.style.overflow = "hidden";
    } else {
      const timer = setTimeout(() => setShouldRender(false), 400); // Wait for animation
      document.body.style.overflow = "unset";
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  if (!shouldRender) return null;

  const isSuccess = type === "success";

  return (
    <div
      className={`fixed inset-0 z-[100] flex items-center justify-center transition-opacity duration-500 ${
        isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
      }`}
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-sm cursor-none"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Dialog Container */}
      <div
        className={`relative w-full max-w-[1440px] px-[clamp(1.25rem,5vw,5rem)] transition-all duration-600 cubic-bezier(0.19, 1, 0.22, 1) transform ${
          isOpen ? "translate-y-0 scale-100 opacity-100" : "translate-y-10 scale-95 opacity-0"
        }`}
      >
        <div className="bg-white rounded-[2.5rem] p-[clamp(2rem,6vw,6rem)] max-w-[1100px] mx-auto shadow-2xl relative overflow-hidden">
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-8 right-8 p-4 text-black hover:opacity-50 transition-opacity"
            aria-label="Close modal"
          >
            <X size={32} />
          </button>

          <div className="flex flex-col items-start space-y-8">
            {/* Header with Large Emoji */}
            <div className="flex items-center gap-6 text-[clamp(2.5rem,6vw,5.5rem)] font-semibold leading-tight tracking-tight text-black">
              {isSuccess ? (
                <>
                  Thank you!{" "}
                  <div className="relative w-[1em] h-[1em]">
                    <Image
                      src={EMOJI_ASSETS.success}
                      alt="👍"
                      fill
                      className="object-contain"
                    />
                  </div>
                </>
              ) : (
                <>
                  Oops..{" "}
                  <div className="relative w-[1em] h-[1em]">
                    <Image
                      src={EMOJI_ASSETS.error}
                      alt="😱"
                      fill
                      className="object-contain"
                    />
                  </div>
                </>
              )}
            </div>

            {/* Content Text */}
            <div className="text-[clamp(1.25rem,2.5vw,2rem)] font-normal leading-[1.4] text-black max-w-[800px]">
              {isSuccess ? (
                <div className="flex flex-wrap items-center gap-x-3">
                  <p>Thanks for inquiry! We&apos;ll contact you shortly!</p>
                  <div className="relative w-[1.2em] h-[1.2em] inline-block -mb-1">
                    <Image
                      src={EMOJI_ASSETS.wink}
                      alt="😉"
                      fill
                      className="object-contain"
                    />
                  </div>
                </div>
              ) : (
                <p>
                  Something went wrong. Please check form data and try again or
                  send{" "}
                  <a
                    href="mailto:info@cuberto.com"
                    className="underline hover:opacity-60 transition-opacity decoration-1 underline-offset-4"
                  >
                    email
                  </a>{" "}
                  to us.
                </p>
              )}
            </div>

            {/* CTA Button to Close */}
            <div className="pt-6">
              <button
                onClick={onClose}
                className="group relative flex items-center justify-center bg-transparent border border-[#e0e0e0] hover:border-black rounded-full h-[60px] md:h-[80px] px-10 md:px-14 overflow-hidden transition-all duration-400"
              >
                <span className="relative z-10 text-[18px] md:text-[20px] font-medium transition-colors duration-400 group-hover:text-white">
                  {isSuccess ? "Back to site" : "Try again"}
                </span>
                <div className="absolute inset-0 bg-black translate-y-full group-hover:translate-y-0 transition-transform duration-600 cubic-bezier(0.19, 1, 0.22, 1)" />
              </button>
            </div>
          </div>
        </div>

        {/* Custom cursor following indicator (simplified for React) */}
        <div className="hidden lg:block fixed pointer-events-none z-[110] transform -translate-x-1/2 -translate-y-1/2 mix-blend-difference">
          {/* This would be handled by a global cursor component, but we add a placeholder design logic here if needed */}
        </div>
      </div>

      <style jsx global>{`
        .cubic-bezier {
          transition-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
        }
      `}</style>
    </div>
  );
}

/**
 * Usage Example:
 * 
 * const [modalState, setModalState] = useState({ open: false, type: 'success' });
 * 
 * <Modals 
 *   isOpen={modalState.open} 
 *   onClose={() => setModalState(prev => ({ ...prev, open: false }))} 
 *   type={modalState.type} 
 * />
 */