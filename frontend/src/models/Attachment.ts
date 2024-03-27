import type { BaseModel } from "@/models/BaseModel";

export interface AttachmentModel extends BaseModel {
  material: number;
  file_url: FormData;
  file_format: string;
}
