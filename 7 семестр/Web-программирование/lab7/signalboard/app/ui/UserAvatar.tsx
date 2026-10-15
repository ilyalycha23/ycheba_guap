import { resolveAvatarUrl, type UserGender } from "@/app/lib/avatar";

type Props = {
  name: string;
  avatarUrl?: string | null;
  gender?: UserGender | string | null;
  className?: string;
  size?: number;
};

export default function UserAvatar({
  name,
  avatarUrl = null,
  gender = "male",
  className,
  size,
}: Props) {
  const src = resolveAvatarUrl(avatarUrl, gender);
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt={`Аватар ${name}`}
      className={className}
      width={size}
      height={size}
      decoding="async"
    />
  );
}
