"use client";

import { makeStore } from "./store";
import { Provider } from "react-redux";

interface props {
  children: React.ReactNode;
}

const CustomProvider = ({ children }: props) => {
  return <Provider store={makeStore()}>{children}</Provider>;
};

export default CustomProvider;
