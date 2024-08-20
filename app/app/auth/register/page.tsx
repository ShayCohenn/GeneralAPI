import Link from "next/link";
import { RegisterForm } from "@/components/forms";
import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "GeneralAPI | Register",
  description: "GeneralAPI's register page"
}

const page = () => {
  return (
    <main>
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-8 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <Image
            alt="GeneralAPI"
            src="/Logo.svg"
            className="mx-auto"
            height={150}
            width={150}
          />
          <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Sign up for an account
          </h2>
        </div>
        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <RegisterForm />
          <p className="mt-10 text-center text-sm text-gray-500">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
            >
              Login here
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
};

export default page;
