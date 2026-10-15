"use client";

import ImageCropper from "@/app/ui/ImageCropper";

type Props = {
  file: File;
  onCancel: () => void;
  onConfirm: (blob: Blob) => void;
};

export default function AvatarCropper({ file, onCancel, onConfirm }: Props) {
  return (
    <ImageCropper
      file={file}
      onCancel={onCancel}
      onConfirm={onConfirm}
      aspect={1}
      shape="circle"
      title="Выберите область аватара"
      outputWidth={512}
    />
  );
}
