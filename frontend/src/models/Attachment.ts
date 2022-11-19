import MaterialModel from "@/models/MaterialModel";

export default interface AttachmentModel {
  id: number;
  name: string;
  material_id: number;
  file_url: string;
}
