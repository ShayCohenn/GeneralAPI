import { useRegisterMutation } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import { toast } from "react-toastify";

export default function useRegister() {
  const router = useRouter();
  const [register, { isLoading }] = useRegisterMutation();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const { username, email, password, confirmPassword } = formData;

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    register({ username, email, password })
      .unwrap()
      .then((a) => {        
        toast.success("Please Check your email to verify your account");
        router.push("/auth/login");
      })
      .catch((error) => {
        console.log(error);
        
        const errorMessage: string = error?.data?.detail || "Failed to register user."
        toast.error(errorMessage);
      });
  };

  return {
    username,
    email,
    password,
    confirmPassword,
    isLoading,
    onChange,
    onSubmit,
  };
}
