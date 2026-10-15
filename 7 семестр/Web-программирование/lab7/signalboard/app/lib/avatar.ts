export type UserGender = "male" | "female";

export const PLACEHOLDER_AVATAR = {
  male: "/images/avatars/placeholder-male.jpg",
  female: "/images/avatars/placeholder-female.jpg",
} as const;

export function normalizeGender(value: unknown): UserGender | null {
  const raw = String(value ?? "").trim().toLowerCase();
  if (raw === "male" || raw === "female") return raw;
  return null;
}

export function resolveAvatarUrl(
  avatarUrl: string | null | undefined,
  gender: UserGender | string | null | undefined,
): string {
  if (avatarUrl) return avatarUrl;
  return gender === "female" ? PLACEHOLDER_AVATAR.female : PLACEHOLDER_AVATAR.male;
}

export function hasCustomAvatar(avatarUrl: string | null | undefined): boolean {
  return Boolean(avatarUrl);
}
