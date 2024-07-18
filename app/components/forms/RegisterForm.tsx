"use client";

import { useRegister } from "@/hooks";
import { Form } from "@/components/forms";

const RegisterForm = () => {
  const {
    username,
    email,
    password,
    confirmPassword,
    isLoading,
    onChange,
    onSubmit,
  } = useRegister();

  const config = [
    {
      labelText: "Username",
      labelId: "username",
      type: "text",
      value: username,
      required: true,
    },
    {
      labelText: "Email",
      labelId: "email",
      type: "email",
      value: email,
      required: true,
    },
    {
      labelText: "Password",
      labelId: "password",
      type: "password",
      value: password,
      required: true,
    },
    {
      labelText: "Confirm Password",
      labelId: "confirmPassword",
      type: "password",
      value: confirmPassword,
      required: true,
    },
  ];
  return (
    <Form
      config={config}
      isLoading={isLoading}
      buttonText="Sign up"
      onChange={onChange}
      onSubmit={onSubmit}
    />
  );
};

export default RegisterForm;
