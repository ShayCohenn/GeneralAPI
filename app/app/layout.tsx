import "@/styles/globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Provider from "@/redux/provider";
import { Setup } from "@/components/utils";
import MainLayout from "@/components/common/main/MainLayout";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GeneralAPI",
  description: "General Purpose API",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Provider>
          <Setup />
          <MainLayout>
            <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8 my-8">
              {children}
            </div>
          </MainLayout>
        </Provider>
      </body>
    </html>
  );
}
