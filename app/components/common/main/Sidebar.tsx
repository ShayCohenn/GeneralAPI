"use client";

import { cn } from "@/lib/utils";
import { ContactIcon, HomeIcon, InfoIcon, ServerIcon } from "lucide-react";
import Link from "next/link";

interface Props {
  isMenuOpen: boolean;
  mobile?: boolean;
  width?: number;
}

const Sidebar = ({ isMenuOpen, mobile, width }: Props) => {
  return (
    <div className={cn("relative top-16" ,mobile && "inset-0 z-50 fixed top-16")}>
      <div
        className={cn(
          "transition-transform duration-300 ease-in-out bg-slate-700",
          mobile && "h-[calc(100dvh-4rem)]",
          {
            "translate-x-0": isMenuOpen,
            "-translate-x-full": !isMenuOpen
          }
        )}
      >
        <nav className="grid gap-4 px-4 py-6">
          <Link
            href="#"
            className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
            prefetch={false}
          >
            <HomeIcon className="h-5 w-5" />
            Home
          </Link>
          <Link
            href="#"
            className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
            prefetch={false}
          >
            <InfoIcon className="h-5 w-5" />
            About
          </Link>
          <Link
            href="#"
            className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
            prefetch={false}
          >
            <ServerIcon className="h-5 w-5" />
            Services
          </Link>
          <Link
            href="#"
            className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
            prefetch={false}
          >
            <ContactIcon className="h-5 w-5" />
            Contact
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
