import { cn } from "@/lib/utils";
import { ImSpinner2 } from "react-icons/im";

interface Props {
  sm?: boolean;
  md?: boolean;
  lg?: boolean;
}

const Spinner = ({ lg, md, sm }: Props) => {
  return (
    <div role="status">
      <ImSpinner2
        className={cn("animate-spin", {
          "w-4 h-4": sm,
          "w-6 h-6": md,
          "w-8 h-8": lg,
        })}
      />
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default Spinner;
