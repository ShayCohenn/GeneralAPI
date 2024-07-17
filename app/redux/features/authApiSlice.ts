import { apiSlice } from "../services/apiSlice";

interface User {
  username: string;
  email: string;
}

interface CreateUserResponse {
  success: boolean;
  user: User;
}

const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getApiKey: builder.query({
      query: () => "/auth/get-api-key",
    }),
    resetApiKey: builder.mutation({
      query: () => ({
        url: "auth/reset-api-key",
        method: "GET",
      }),
    }),
    googleAuth: builder.mutation({
      query: ({ code }) => ({
        url: `/auth/auth/google?code=${encodeURIComponent(code)}`,
        method: "POST",
      }),
    }),
    login: builder.mutation({
      query: ({ username, password }) => ({
        url: "auth/login",
        method: "POST",
        body: { username, password },
      }),
    }),
    register: builder.mutation({
      query: ({ username, email, password }) => ({
        url: "auth/register",
        method: "POST",
        body: { username, email, password },
      }),
    }),
    refresh: builder.mutation({
      query: () => ({
        url: "auth/refresh",
        method: "GET",
      }),
    }),
    logout: builder.mutation({
      query: () => ({
        url: "auth/logout",
        method: "POST",
      }),
    }),
    verify: builder.mutation({
      query: ({ token }) => ({
        url: `auth/verify-email?token=${token}`,
        method: "GET",
      }),
    }),
    forgotPassword: builder.mutation({
      query: (email) => ({
        url: "auth/forgot-password",
        method: "POST",
        body: { email },
      }),
    }),
    confirmResetPassword: builder.mutation({
      query: ({ token, user, new_password }) => ({
        url: "auth/confirm-reset-password",
        method: "POST",
        body: { token, user, new_password },
      }),
    }),
  }),
});

export const {
  useGetApiKeyQuery,
  useResetApiKeyMutation,
  useGoogleAuthMutation,
  useLoginMutation,
  useRegisterMutation,
  useVerifyMutation,
  useLogoutMutation,
  useRefreshMutation,
  useForgotPasswordMutation,
  useConfirmResetPasswordMutation,
} = authApiSlice;
