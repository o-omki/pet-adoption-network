import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex items-center justify-center min-h-screen w-full bg-gray-100">
      {children}
    </div>
  );
}
