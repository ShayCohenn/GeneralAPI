"use client";

import { cn } from "@/lib/utils";
import { useLogoutMutation } from "@/redux/features/authApiSlice";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import { File, HomeIcon, LogIn, User } from "lucide-react";
import Link from "next/link";
import { logout as setLogout } from "@/redux/features/authSlice";
import { useRouter } from "next/navigation";

interface Props {
  isMenuOpen: boolean;
  mobile?: boolean;
  width?: number;
}

const Sidebar = ({ isMenuOpen, mobile, width }: Props) => {
  const dispatch = useAppDispatch();
  const router = useRouter();

  const [logout] = useLogoutMutation();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    logout(null)
      .unwrap()
      .then(() => {
        dispatch(setLogout());
      })
      .finally(() => {
        router.push("/");
      });
  };

  const authLinks = <div>logged in links</div>;

  const guestLinks = (
    <div>
      <Link
        href="#"
        className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
        prefetch={false}
      >
        <LogIn className="h-5 w-5" />
        Login
      </Link>
      <Link
        href="#"
        className="flex items-center gap-2 text-sm font-medium transition-colors hover:text-primary"
        prefetch={false}
      >
        <User className="h-5 w-5" />
        Register
      </Link>
    </div>
  );

  return (
    <div
      className={cn(
        "relative top-16 bg-background",
        mobile && "inset-0 z-50 fixed top-16"
      )}
    >
      <div
        className={cn(
          "transition-transform duration-300 ease-in-out",
          mobile && "h-[calc(100dvh-4rem)]",
          {
            "translate-x-0": isMenuOpen,
            "-translate-x-full": !isMenuOpen,
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
            <File className="h-5 w-5" />
            Documentation
          </Link>
          <hr />
          {isAuthenticated ? authLinks : guestLinks}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
