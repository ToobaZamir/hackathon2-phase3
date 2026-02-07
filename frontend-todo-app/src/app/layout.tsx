'use client';

import "./globals.css";
import { Inter } from "next/font/google";
import { ReactNode } from 'react';
import { AuthProvider } from '@/contexts/auth';

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-background">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}