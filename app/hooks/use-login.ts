import { useLoginMutation } from "@/redux/features/authApiSlice";
import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import { toast } from "react-toastify";

export default function useRegister() {
  const router = useRouter();
  const [login, { isLoading }] = useLoginMutation();
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });

  const { username, password} = formData;

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    login({ username, password })
      .unwrap()
      .then((a) => {        
        toast.success("Login Successfull!");
        router.push("/dashboard");
      })
      .catch((error) => {
        console.log(error);
        
        const errorMessage: string = error?.data?.detail || "Failed to log in."
        toast.error(errorMessage);
      });
  };

  return {
    username,
    password,
    isLoading,
    onChange,
    onSubmit,
  };
}
