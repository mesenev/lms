import MaterialModel from "@/models/MaterialModel";

export default interface AttachmentModel {
  id: number;
  name: string;
  material: number;
  file_url: FormData;
}
