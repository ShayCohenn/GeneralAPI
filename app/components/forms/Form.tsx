import { ChangeEvent, FormEvent } from "react";
import { Input } from "@/components/forms";
import Spinner from "@/components/common/Spinner";

export interface Config {
  labelText: string;
  labelId: string;
  type: string;
  value: string;
  link?:{
    linkText: string;
    linkUrl: string;
  }
  required?: boolean;
}

interface Props {
  config: Config[];
  isLoading: boolean;
  buttonText: string;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
}

const Form = ({ config, isLoading, buttonText, onSubmit, onChange }: Props) => {
  return (
    <form className="space-y-6" onSubmit={onSubmit}>
      {config.map((input, key) => (
        <Input
          key={key}
          labelId={input.labelId}
          type={input.type}
          onChange={onChange}
          value={input.value}
          required={input.required}
          link={input.link}
        >
          {input.labelText}
        </Input>
      ))}

      <div>
        <button
          type="submit"
          className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          disabled={isLoading}
        >
          {isLoading ? <Spinner sm /> : buttonText}
        </button>
      </div>
    </form>
  );
};

export default Form;
