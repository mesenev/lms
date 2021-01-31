import SubmitModel from '@/models/SubmitModel';

export default interface ProblemModel {
  id: number;
  lesson: number;
  type: string;
  name: string;
  description: string;
  completed: boolean;
  manual: boolean;
  cats_id: number;
  cats_material_url: string;
  language: Array<string> | null; //Todo : fix this
  success_or_last_submits: Array<SubmitModel>;
}
