import { resolveAvatarUrl } from "@/app/lib/avatar";

export type SignalAuthorRecord = {
  id: string;
  name: string;
  gender: "male" | "female";
  avatarUrl: string | null;
};

export type SignalRecord = {
  id: string;
  slug: string;
  title: string;
  summary: string;
  category: string;
  location: string;
  image: string;
  imageAlt: string;
  latitude: { toString(): string } | number;
  longitude: { toString(): string } | number;
  createdAt: Date;
  archivedAt?: Date | null;
  author: SignalAuthorRecord;
};

export function toSignalDto(
  signal: SignalRecord,
  trackedIds: Set<string>,
  currentUserId?: string | null,
) {
  return {
    id: signal.id,
    slug: signal.slug,
    title: signal.title,
    summary: signal.summary,
    category: signal.category,
    location: signal.location,
    image: signal.image,
    imageAlt: signal.imageAlt,
    latitude: Number(signal.latitude),
    longitude: Number(signal.longitude),
    createdAt: signal.createdAt.toISOString(),
    archivedAt: signal.archivedAt ? signal.archivedAt.toISOString() : null,
    isTracked: trackedIds.has(signal.id),
    isOwn: Boolean(currentUserId && signal.author.id === currentUserId),
    author: {
      id: signal.author.id,
      name: signal.author.name,
      gender: signal.author.gender,
      avatarUrl: resolveAvatarUrl(signal.author.avatarUrl, signal.author.gender),
    },
  };
}

export const signalAuthorSelect = {
  id: true,
  name: true,
  gender: true,
  avatarUrl: true,
} as const;
