import { redirect } from "next/navigation";

export default async function SignalDetailRedirectPage() {
  redirect("/gallery");
}
