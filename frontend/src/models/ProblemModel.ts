import SubmitModel from '@/models/SubmitModel';
import { TutorialModel } from '@/models/TutorialModel';

export default interface ProblemModel extends TutorialModel {
  lesson: number;
  type: string;
  description: string;
  completed: boolean;
  manual: boolean;
  cats_id: number;
  cats_material_url: string;
  language: Array<string> | null; //Todo : fix this
  students?: {};
  submits?: Array<SubmitModel>;
}
