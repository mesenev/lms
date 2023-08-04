import type { MaterialModel } from "@/models/MaterialModel";

export interface AttachmentModel {
  id: number;
  name: string;
  material: number;
  file_url: FormData;
  file_format: string;
}
