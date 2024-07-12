import { configureStore } from "@reduxjs/toolkit";
import authSlice from "./features/authSlice"

export const makeStore = () =>
  configureStore({
    reducer: {
        auth: authSlice
    },
    devTools: process.env.NODE_ENV !== "production",
  });

export type AppStore = ReturnType<typeof makeStore>;
export type AppDispatch = AppStore["dispatch"];
export type RootState = ReturnType<AppStore["getState"]>;
