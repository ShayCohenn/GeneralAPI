"use client";

import { useLogin } from "@/hooks";
import Form, { Config } from "./Form";

const LoginForm = () => {
  const { isLoading, onChange, onSubmit, password, username } = useLogin();

  const config: Config[] = [
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
      link: {
        linkText:'Forgot Password?',
        linkUrl:'/password-reset'
      }
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
