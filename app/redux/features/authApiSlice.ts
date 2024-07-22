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
      query: () => "get-api-key",
    }),
    resetApiKey: builder.mutation({
      query: () => ({
        url: "reset-api-key",
        method: "GET",
      }),
    }),
    googleAuth: builder.mutation({
      query: ({ code }) => ({
        url: `auth/google?code=${encodeURIComponent(code)}`,
        method: "POST",
      }),
    }),
    login: builder.mutation({
      query: ({ username, password }) => ({
        url: "login",
        method: "POST",
        body: { username, password },
      }),
    }),
    register: builder.mutation({
      query: ({ username, email, password }) => ({
        url: "register",
        method: "POST",
        body: { username, email, password },
      }),
    }),
    refresh: builder.mutation({
      query: () => ({
        url: "refresh",
        method: "GET",
      }),
    }),
    logout: builder.mutation({
      query: () => ({
        url: "logout",
        method: "POST",
      }),
    }),
    verify: builder.mutation({
      query: ({ token, uid }) => ({
        url: `verify-email?token=${token}&uid=${uid}`,
        method: "GET",
      }),
    }),
    forgotPassword: builder.mutation({
      query: (email) => ({
        url: "forgot-password",
        method: "POST",
        body: { email },
      }),
    }),
    confirmResetPassword: builder.mutation({
      query: ({ token, user, new_password }) => ({
        url: "confirm-reset-password",
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
