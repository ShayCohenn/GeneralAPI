"use client"

import { useVerifyMutation } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "react-toastify";

interface Props {
  params: {
    uid: string
    token: string
  }
}

const Page = ({ params }: Props) => {
  const router = useRouter()
  const [verify] = useVerifyMutation()

  useEffect(() => {
    const verifyUser = async () => {
      try {
        await verify(params).unwrap();
        toast.success("User verified successfully");
      } catch {
        toast.error("Failed to verify user");
      } finally {
        router.push("/auth/login");
      }
    };

    verifyUser();
  }, [params, router, verify]);
  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm: w-full sm: max-w-sm">
        <h1 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          Activating Your Account          
        </h1>
      </div>
    </div>
  );
};

export default Page;
