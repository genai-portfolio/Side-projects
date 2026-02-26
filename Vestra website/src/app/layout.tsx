import type { Metadata } from "next";
import "./globals.css";
import { VisualEditsMessenger } from "orchids-visual-edits";
import CustomCursor from "@/components/ui/CustomCursor";

export const metadata: Metadata = {
  title: "Vestra Logics — Design Agency",
  description: "Design agency focused on AI-driven products. Creating memorable websites and digital products since 2025.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased overflow-x-hidden cursor-none">
        {children}
        <CustomCursor />
        <VisualEditsMessenger />
      </body>
    </html>
  );
}
