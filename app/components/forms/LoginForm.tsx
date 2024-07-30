"use client";

import { useLogin } from "@/hooks";
import Form from "./Form";

const LoginForm = () => {
  const { isLoading, onChange, onSubmit, password, username } = useLogin();

  const config = [
    {
      labelText: "Username",
      labelId: "username",
      type: "text",
      value: username,
      required: true,
    },
    {
      labelText: "Password",
      labelId: "password",
      type: "password",
      value: password,
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

export default LoginForm;
