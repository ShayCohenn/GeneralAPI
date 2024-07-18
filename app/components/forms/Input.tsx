import { ChangeEvent } from "react";

interface Props {
  labelId: string;
  type: string;
  children: React.ReactNode;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  required?: boolean;
  value: string;
}

const Input = ({
  labelId,
  type,
  children,
  onChange,
  required = false,
  value,
}: Props) => {
  return (
    <div>
      <label
        htmlFor={labelId}
        className="block text-sm font-medium leading-6 text-gray-900"
      >
        {children}
      </label>
      <div className="mt-2">
        <input
          id={labelId}
          name={labelId}
          type={type}
          required
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          onChange={onChange}
          value={value}
        />
      </div>
    </div>
  );
};

export default Input;
