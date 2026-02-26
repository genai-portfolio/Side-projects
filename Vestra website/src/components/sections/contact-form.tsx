"use client";

import React, { useState, useRef, useEffect } from "react";
import { Paperclip } from "lucide-react";

/**
 * ContactForm Component
 * 
 * Clones the interactive contact form section from Cuberto, featuring:
 * - Multi-select pill buttons for interests and budget
 * - Minimal text inputs with animated underlines
 * - "Add attachment" link with icon
 * - "Send request" CTA with a magnetic/ripple fill effect
 */

const interests = [
  "Site from scratch",
  "UX/UI design",
  "Product design",
  "Webflow site",
  "Motion design",
  "Branding",
  "Mobile development",
];

const budgets = ["10-20k", "30-40k", "40-50k", "50-100k", "> 100k"];

export default function ContactForm() {
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [selectedBudget, setSelectedBudget] = useState<string>("");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    project: "",
  });

  const toggleInterest = (interest: string) => {
    setSelectedInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    );
  };

  const selectBudget = (budget: string) => {
    setSelectedBudget(budget === selectedBudget ? "" : budget);
  };

  return (
    <section className="bg-background py-[100px] md:py-[160px] px-5 sm:px-10 lg:px-[160px] font-sans">
      <div className="max-w-[1440px] mx-auto">
        {/* Hero Heading */}
        <div className="mb-[80px] md:mb-[120px] text-center">
          <h1 className="text-[3.5rem] sm:text-[5rem] lg:text-[7.5rem] leading-[1.0] font-semibold tracking-[-0.02em]">
            Hey! Tell us all <br className="hidden md:block" /> the things
          </h1>
        </div>

        <form className="max-w-[800px] mx-auto space-y-[60px] md:space-y-[80px]">
          {/* Interests Section */}
          <div className="space-y-[24px]">
            <div className="text-[1.25rem] md:text-[1.5rem] font-medium tracking-[-0.01em]">
              I&apos;m interested in...
            </div>
            <div className="flex flex-wrap gap-3">
              {interests.map((interest) => (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`px-8 py-5 rounded-full border text-[1.125rem] md:text-[1.4rem] transition-all duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] relative overflow-hidden group ${selectedInterests.includes(interest)
                    ? "bg-foreground text-background border-foreground"
                    : "bg-transparent text-foreground border-border hover:border-foreground"
                    }`}
                >
                  <span className="relative z-10">{interest}</span>
                  {!selectedInterests.includes(interest) && (
                    <div className="absolute inset-0 bg-foreground translate-y-[101%] group-hover:translate-y-0 transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)]" />
                  )}
                  <span className={`relative z-10 transition-colors duration-500 ${!selectedInterests.includes(interest) ? 'group-hover:text-background' : ''}`}>
                    {interest}
                  </span>
                  {/* Invisible spacer to maintain width since we use absolute overlay */}
                  <span className="invisible block h-0">{interest}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Text Inputs */}
          <div className="space-y-4">
            <div className="relative group">
              <input
                type="text"
                placeholder="Your name"
                className="w-full bg-transparent border-none border-b border-border py-4 text-[1.25rem] md:text-[1.5rem] outline-none transition-all placeholder:text-muted focus:placeholder:text-transparent"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
              <div className="absolute bottom-0 left-0 w-0 h-[2px] bg-foreground transition-all duration-500 group-focus-within:w-full" />
            </div>

            <div className="relative group">
              <input
                type="email"
                placeholder="Email"
                className="w-full bg-transparent border-none border-b border-border py-4 text-[1.25rem] md:text-[1.5rem] outline-none transition-all placeholder:text-muted focus:placeholder:text-transparent"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
              <div className="absolute bottom-0 left-0 w-0 h-[2px] bg-foreground transition-all duration-500 group-focus-within:w-full" />
            </div>

            <div className="relative group">
              <textarea
                placeholder="Tell us about your project"
                rows={1}
                className="w-full bg-transparent border-none border-b border-border py-4 text-[1.25rem] md:text-[1.5rem] outline-none transition-all resize-none placeholder:text-muted focus:placeholder:text-transparent"
                value={formData.project}
                onChange={(e) => {
                  setFormData({ ...formData, project: e.target.value });
                  e.target.style.height = 'auto';
                  e.target.style.height = e.target.scrollHeight + 'px';
                }}
              />
              <div className="absolute bottom-0 left-0 w-0 h-[2px] bg-foreground transition-all duration-500 group-focus-within:w-full" />
            </div>
          </div>

          {/* Budget Section */}
          <div className="space-y-[24px]">
            <div className="text-[1.25rem] md:text-[1.5rem] font-medium tracking-[-0.01em]">
              Project budget (USD)
            </div>
            <div className="flex flex-wrap gap-3">
              {budgets.map((budget) => (
                <button
                  key={budget}
                  type="button"
                  onClick={() => selectBudget(budget)}
                  className={`px-8 py-5 rounded-full border text-[1.125rem] md:text-[1.4rem] transition-all duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] relative overflow-hidden group ${selectedBudget === budget
                    ? "bg-foreground text-background border-foreground"
                    : "bg-transparent text-foreground border-border hover:border-foreground"
                    }`}
                >
                  <span className="relative z-10">{budget}</span>
                  {selectedBudget !== budget && (
                    <div className="absolute inset-0 bg-foreground translate-y-[101%] group-hover:translate-y-0 transition-transform duration-500 ease-[cubic-bezier(0.19,1,0.22,1)]" />
                  )}
                  <span className={`relative z-10 transition-colors duration-500 ${selectedBudget !== budget ? 'group-hover:text-background' : ''}`}>
                    {budget}
                  </span>
                  <span className="invisible block h-0">{budget}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Attachment Link */}
          <div className="pt-4">
            <label className="inline-flex items-center gap-2 cursor-pointer group">
              <input type="file" className="hidden" />
              <Paperclip className="w-5 h-5 -rotate-45 transition-transform group-hover:scale-110" />
              <span className="text-[1.25rem] font-medium relative py-1">
                Add attachment
                <span className="absolute bottom-0 left-0 w-full h-[1px] bg-foreground/20 group-hover:bg-foreground transition-colors" />
              </span>
            </label>
          </div>

          {/* Submit Button */}
          <div className="pt-10">
            <button
              type="submit"
              className="relative w-[210px] h-[74px] rounded-full border border-border overflow-hidden group outline-none"
              onClick={(e) => e.preventDefault()}
            >
              <div className="absolute inset-[-1px] bg-foreground translate-y-[101%] group-hover:translate-y-0 transition-transform duration-600 ease-[cubic-bezier(0.19,1,0.22,1)] rounded-full" />
              <span className="relative z-10 text-[1.25rem] text-foreground group-hover:text-background transition-colors duration-500">
                Send request
              </span>
            </button>
          </div>

          {/* Legal Footer */}
          <div className="text-[0.75rem] text-muted-foreground leading-relaxed pt-10">
            This site is protected by reCAPTCHA and the Google{" "}
            <a href="https://policies.google.com/privacy" className="underline hover:text-foreground">Privacy Policy</a>{" "}
            and{" "}
            <a href="https://policies.google.com/terms" className="underline hover:text-foreground">Terms of Service</a> apply.
          </div>
        </form>
      </div>

      <style jsx>{`
        button span.invisible {
          display: block;
          height: 0;
          visibility: hidden;
        }
        button span:not(.invisible) {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          width: 100%;
        }
      `}</style>
    </section>
  );
}