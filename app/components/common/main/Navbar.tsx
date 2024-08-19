import { Button } from "../../ui/button";
import { MenuIcon, MountainIcon } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

interface Props {
  isMenuOpen: boolean;
  setIsMenuOpen(value: boolean): void;
}

const Navbar = ({ isMenuOpen, setIsMenuOpen }: Props) => {
  return (
    <header className="bg-background fixed top-0 z-50 w-full border-b border-border">
      <div className="mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
          <Link href="/" className="flex items-center gap-2" prefetch={false}>
            <Image
              src={"/Logo.svg"}
              alt="GeneralAPI Logo"
              height={50}
              width={50}
            />
            <span className="text-lg font-bold">GeneralAPI</span>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
