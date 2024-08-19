"use client";

import { useState, useEffect, useRef } from "react";
import { Navbar, Sidebar } from "@/components/common";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { ImperativePanelHandle } from "react-resizable-panels";

interface Props {
  children: React.ReactNode;
}

const MainLayout = ({ children }: Props) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [sidebarWidth, setSidebarWidth] = useState<number>(20); // Initial width
  const sidebarRef = useRef<ImperativePanelHandle>(null);

  useEffect(() => {
    const savedMenuState = localStorage.getItem("isMenuOpen");
    if (savedMenuState !== null) {
      setIsMenuOpen(JSON.parse(savedMenuState));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("isMenuOpen", JSON.stringify(isMenuOpen));
    if (sidebarRef.current) {
      sidebarRef.current.resize(isMenuOpen ? sidebarWidth : 0);
    }
  }, [isMenuOpen, sidebarWidth]);

  return (
    <div>
      {/* Desktop View */}
      <div className="md:block hidden">
        <Navbar isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />
        <ResizablePanelGroup direction="horizontal">
          <ResizablePanel defaultSize={isMenuOpen ? 20 : 0} ref={sidebarRef}>
            <Sidebar isMenuOpen={isMenuOpen}/>
          </ResizablePanel>
          <ResizableHandle />
          <ResizablePanel>{children}</ResizablePanel>
        </ResizablePanelGroup>
      </div>

      {/* Mobile View */}
      <div className="md:hidden block h-screen overflow-auto">
        <Navbar isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />
        {isMenuOpen && <Sidebar isMenuOpen={isMenuOpen} mobile />}
        <div className="overflow-auto p-4 h-full">{children}</div>
      </div>
    </div>
  );
};

export default MainLayout;
