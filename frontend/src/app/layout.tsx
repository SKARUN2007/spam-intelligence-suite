import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Spam Intelligence | AI Classifier",
  description: "Advanced spam detection using Machine Learning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
